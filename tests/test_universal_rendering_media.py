"""Observable artifacts, acquisition safety, offline receipts, and tamper checks."""
import binascii
from copy import deepcopy
import json
import socket
import struct
import xml.etree.ElementTree as ET
import zlib

import pytest

from scriptorium.engines.composition import media, renderers
from scriptorium.engines.composition.visuals import render_visuals, validate_svg


def png(width=2,height=2, *, scanline_filter=0):
    def chunk(kind,data):
        return struct.pack(">I",len(data))+kind+data+struct.pack(">I",binascii.crc32(kind+data)&0xffffffff)
    header = struct.pack(">IIBBBBB",width,height,8,2,0,0,0)
    raw = (bytes([scanline_filter])+bytes([255,0,0])*width)*height
    return b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",header)+chunk(b"IDAT",zlib.compress(raw))+chunk(b"IEND",b"")


def visual(**values):
    return {"id":"v1","concept":"c1","section":"Representation","objective":"Inspect the supplied relationship",
            "kind":"network","nodes":[{"id":"a","label":"Input"},{"id":"b","label":"Output"}],
            "edges":[{"source":"a","target":"b","label":"causes"}],**values}


def plan(value):
    return {"visuals":[value],"chapters":[{"id":"ch1","concepts":["c1"]}]}


def remote(**values):
    return visual(**{"kind":"source_figure","url":"https://example.org/figure.png","source":"https://example.org/paper",
                  "rights":"CC0 (supplied metadata)","alt":"Measured relationship","relevance":"Explains the stated objective",**values})


def test_twelve_families_share_real_backends_and_reject_mismatch():
    assert set(renderers.FAMILIES)=={f"R{i}" for i in range(1,13)}
    assert renderers.select_representation(visual(),available={"graph"})["renderer"]=="graph"
    with pytest.raises(ValueError,match="family"):
        renderers.select_representation(visual(family="R10"),available={"graph"})
    assert renderers.select_representation(visual(kind="intuition"),available=set())["status"]=="unavailable"


def test_source_only_policy_blocks_unsupplied_remote_media_before_network(tmp_path, monkeypatch):
    value = remote()
    subject = plan(value)
    subject['source_policy'] = 'strict'
    def no_network(*args, **kwargs):
        raise AssertionError('strict policy must prevent acquisition')
    monkeypatch.setattr(media, 'fetch_image', no_network)
    result = render_visuals(tmp_path, subject, {'ch1': '## Representation\n'})[1]['v1']
    assert result['status'] == 'failed' and 'Source-only' in result['failure_reason']


@pytest.mark.parametrize("kind",["network","circuit","algorithm","chronology","research"])
def test_graph_artifacts_preserve_nodes_and_edges_and_detect_tampering(tmp_path,kind):
    value=visual(kind=kind)
    bodies,results=render_visuals(tmp_path,plan(value),{"ch1":"## Representation\n"})
    result=results["v1"]
    assert result["status"]=="verified",result
    path=tmp_path/result["path"]
    root=ET.fromstring(path.read_text())
    assert len(root.findall("{http://www.w3.org/2000/svg}line"))==1
    assert "Input" in path.read_text() and "Output" in path.read_text()
    assert result["embed"] in bodies["ch1"]
    assert render_visuals(tmp_path,plan(value),bodies,execute=False)[1]["v1"]["status"]=="verified"
    path.write_text("altered")
    assert render_visuals(tmp_path,plan(value),bodies,execute=False)[1]["v1"]["status"]=="failed"


def test_arrow_tip_is_outside_opaque_target_and_self_loops_are_explicitly_unsupported():
    root=ET.fromstring(renderers.graph_svg(visual()))
    tip=root.find("{http://www.w3.org/2000/svg}polygon").get("points").split()[0]
    tip_x,tip_y=map(float,tip.split(","))
    target=root.findall("{http://www.w3.org/2000/svg}rect")[1]
    # A horizontal edge must finish to the left of the target, not behind it.
    assert tip_x < float(target.get("x"))
    assert float(target.get("y")) < tip_y < float(target.get("y"))+float(target.get("height"))
    with pytest.raises(ValueError,match="Self-loop"):
        renderers.graph_svg(visual(edges=[{"source":"a","target":"a"}]))


def test_coordinates_preserve_scale_and_reject_nonfinite_points(tmp_path):
    value=visual(kind="geometry",units="metres",nodes=[{"id":"a","label":"Origin","x":0,"y":0},{"id":"b","label":"Point","x":3,"y":4}])
    result=render_visuals(tmp_path,plan(value),{"ch1":"## Representation\n"})[1]["v1"]
    assert result["status"]=="verified",result
    assert "Equal axis scale" in (tmp_path/result["path"]).read_text()
    value["nodes"][0]["x"]=float("nan")
    with pytest.raises(ValueError,match="finite"):
        renderers.coordinate_svg(value)


@pytest.mark.parametrize("values",[{"nodes":[42]},{"nodes":[{"id":[],"label":"Invalid"}]},
                                  {"edges":[42]},{"nodes":{}},{"edges":None}])
def test_malformed_semantics_persist_failed_render_results(tmp_path,values):
    result=render_visuals(tmp_path,plan(visual(**values)),{"ch1":"## Representation\n"})[1]["v1"]
    assert result["status"]=="failed" and result["attempted"] and result["failure_reason"]


def test_native_mermaid_is_persisted_source_with_inert_labels(tmp_path):
    value=visual(kind="workflow")
    value["nodes"][0]["label"]='Input"]\nclick a "https://evil.test"'
    bodies,results=render_visuals(tmp_path,plan(value),{"ch1":"## Representation\n"})
    result=results["v1"]
    assert result["status"]=="verified",result
    assert result["path"].endswith(".mmd") and result["embed"].startswith("```mermaid")
    assert "\nclick" not in result["embed"]
    assert result["embed"] in bodies["ch1"]
    assert "not a raster" in result["validation"]["limits"]


def test_table_and_interactive_emit_actual_artifacts(tmp_path):
    value=visual(kind="table",table={"type":"definition","objective":"Compare definitions","interpretation":"The terms have distinct roles.",
                                   "rows":[{"term":"Input","meaning":"Initial state"},{"term":"Output","meaning":"Resulting state"}]})
    result=render_visuals(tmp_path,plan(value),{"ch1":"## Representation\n"})[1]["v1"]
    assert result["status"]=="verified" and "| Input | Initial state |" in result["embed"]
    value=visual(kind="interactive",frames=[{"label":"Start","state":"<script>alert(1)</script>"},{"label":"End","state":"2"}])
    result=render_visuals(tmp_path,plan(value),{"ch1":"## Representation\n"})[1]["v1"]
    assert result["status"]=="verified",result
    html=(tmp_path/result["path"]).read_text()
    assert "Content-Security-Policy" in html and "textContent" in html
    assert "<script>alert(1)</script>" not in html
    assert result["embed"].startswith("[Open interactive")


@pytest.mark.parametrize("fault",["signature","mime","truncated","checksum","filter","pixels","html","compressed"])
def test_png_requires_decodable_bounded_image_content(fault):
    raw,mime=png(),"image/png"
    if fault=="signature": raw=b"not image"
    if fault=="mime": mime="text/html"
    if fault=="truncated": raw=raw[:-8]
    if fault=="checksum": raw=raw[:40]+bytes([raw[40]^1])+raw[41:]
    if fault=="filter": raw=png(scanline_filter=5)
    if fault=="pixels":
        # Header is rejected before decoding its deliberately tiny data.
        header=struct.pack(">IIBBBBB",10000,10000,8,2,0,0,0)
        raw=raw[:16]+header+struct.pack(">I",binascii.crc32(b"IHDR"+header)&0xffffffff)+raw[33:]
    if fault=="html": raw=b"<html>fake image</html>"
    if fault=="compressed": raw=png()+b"trailing"
    with pytest.raises(ValueError): media.decode_png(raw,mime)


def test_png_is_reconstructed_and_all_filters_are_supported():
    for filtering in range(5):
        assert media.decode_png(png(scanline_filter=filtering))["width"]==2


@pytest.mark.parametrize("url",["http://example.org/image.png","https://user:password@example.org/image.png",
                                   "https://example.org:444/image.png","https://example.org/i.png#fragment",
                                   "https://example.org/i.png)\nmalicious"])
def test_media_rejects_unsafe_url_before_network(url,monkeypatch):
    monkeypatch.setattr(media.socket,"getaddrinfo",lambda *a,**k:pytest.fail("unexpected DNS"))
    with pytest.raises(ValueError): media.fetch_image(url)


@pytest.mark.parametrize("addresses",[["127.0.0.1"],["169.254.169.254"],["10.0.0.1"],["::1"],["93.184.216.34","192.168.1.3"]])
def test_media_rejects_nonpublic_and_mixed_dns_answers(monkeypatch,addresses):
    monkeypatch.setattr(media.socket,"getaddrinfo",lambda *a,**k:[(2,1,6,"",(address,443)) for address in addresses])
    monkeypatch.setattr(media,"_request_once",lambda *a:pytest.fail("unsafe socket connection"))
    with pytest.raises(ValueError,match="public"): media.fetch_image("https://example.org/i.png")


def test_redirects_are_validated_independently_and_ip_is_pinned(monkeypatch):
    calls=[]
    def dns(host,*a,**k):
        calls.append(host)
        return [(2,1,6,"",("93.184.216.34" if host=="example.org" else "127.0.0.1",443))]
    monkeypatch.setattr(media.socket,"getaddrinfo",dns)
    def request(url,host,address):
        assert host=="example.org" and address=="93.184.216.34"
        return 302,{"location":"https://internal.test/image.png"},b""
    monkeypatch.setattr(media,"_request_once",request)
    with pytest.raises(ValueError,match="public"): media.fetch_image("https://example.org/i.png")
    assert calls==["example.org","internal.test"]


def test_safe_redirect_and_png_mime_are_verified(monkeypatch):
    calls=[]
    monkeypatch.setattr(media,"_resolve_public",lambda host:["93.184.216.34"])
    def request(url,host,address):
        calls.append((url,host,address))
        if len(calls)==1:
            return 302,{"location":"https://cdn.example.org/actual.png"},b""
        return 200,{"content-type":"image/png; charset=binary"},png()
    monkeypatch.setattr(media,"_request_once",request)
    raw,receipt=media.fetch_image("https://example.org/figure")
    assert raw==png() and receipt["redirects"]==1
    assert receipt["final_url"]=="https://cdn.example.org/actual.png"
    assert calls[1][1:]==("cdn.example.org","93.184.216.34")


@pytest.mark.parametrize("fault",["loop","limit","mime","html","missing-location","status"])
def test_remote_acquisition_fails_on_bad_redirects_and_nonimages(monkeypatch,fault):
    monkeypatch.setattr(media,"_resolve_public",lambda host:["93.184.216.34"])
    def request(url,host,address):
        if fault=="loop": return 302,{"location":url},b""
        if fault=="limit": return 302,{"location":url+"x"},b""
        if fault=="missing-location": return 302,{},b""
        if fault=="status": return 404,{},b""
        if fault=="mime": return 200,{"content-type":"text/html"},png()
        return 200,{"content-type":"image/png"},b"<html>not an image</html>"
    monkeypatch.setattr(media,"_request_once",request)
    with pytest.raises(ValueError): media.fetch_image("https://example.org/i.png")


@pytest.mark.parametrize("fault",["length","encoding","timeout","oversize","truncated"])
def test_transport_bounds_headers_body_and_timeout(monkeypatch,fault):
    class Response:
        status=200
        sent=False
        def getheaders(self):
            if fault=="length": return [("Content-Length",str(media.MAX_BYTES+1))]
            if fault=="encoding": return [("Content-Encoding","gzip")]
            if fault=="truncated": return [("Content-Length","10")]
            return []
        def read1(self,size):
            if fault=="timeout": raise socket.timeout("timed out")
            if self.sent: return b""
            self.sent=True
            return b"x"*(media.MAX_BYTES+1) if fault=="oversize" else b"x"
    class Connection:
        sock=None
        closed=False
        def __init__(self,*a): pass
        def request(self,*a,**k): pass
        def getresponse(self): return Response()
        def close(self): self.closed=True
    monkeypatch.setattr(media,"_PinnedHTTPS",Connection)
    with pytest.raises((ValueError,socket.timeout)):
        media._request_once("https://example.org/i.png","example.org","93.184.216.34")


def test_pinned_transport_connects_to_validated_address_but_tls_uses_original_host(monkeypatch):
    connected,wrapped=[],[]
    class Raw:
        def close(self): pass
    class TLS:
        def wrap_socket(self,raw,server_hostname):
            wrapped.append(server_hostname)
            return raw
    monkeypatch.setattr(media.ssl,"create_default_context",lambda:TLS())
    monkeypatch.setattr(media.socket,"create_connection",lambda address,timeout:(connected.append(address) or Raw()))
    connection=media._PinnedHTTPS("images.example.org","93.184.216.34")
    connection.connect()
    assert connected==[("93.184.216.34",443)] and wrapped==["images.example.org"]


def test_verified_remote_snapshot_supports_offline_validation_and_detects_changes(tmp_path,monkeypatch):
    monkeypatch.setattr(media,"fetch_image",lambda url:(png(),{"mime":"image/png","final_url":url,"acquired_at":"test"}))
    value=remote(asset_policy="remote_allowed")
    bodies,results=render_visuals(tmp_path,plan(value),{"ch1":"## Representation\n"})
    result=results["v1"]
    assert result["status"]=="verified",result
    assert "](assets/scriptorium/" in result["embed"] and "Source:" in result["embed"]
    assert "](https://example.org/figure.png)" not in result["embed"]
    assert result["provenance"]["final_url"] == "https://example.org/figure.png"
    assert (tmp_path/result["path"]).read_bytes()==png()
    monkeypatch.setattr(media,"fetch_image",lambda *a:pytest.fail("offline validation fetched network"))
    assert render_visuals(tmp_path,plan(value),bodies,execute=False)[1]["v1"]["status"]=="verified"
    (tmp_path/result["path"]).write_bytes(b"altered")
    assert render_visuals(tmp_path,plan(value),bodies,execute=False)[1]["v1"]["status"]=="failed"


def test_explicit_fallback_and_offline_policy_never_silently_publish_remote(tmp_path,monkeypatch):
    (tmp_path/"fallback.png").write_bytes(png())
    monkeypatch.setattr(media,"fetch_image",lambda *a:(_ for _ in ()).throw(OSError("unreachable")))
    value=remote(local_fallback="fallback.png",asset_policy="remote_allowed")
    result=render_visuals(tmp_path,plan(value),{"ch1":"## Representation\n"})[1]["v1"]
    assert result["status"]=="verified" and result["provenance"]["fallback_used"]
    assert "unreachable" in result["provenance"]["remote_failure"]
    assert "](assets/scriptorium/" in result["embed"]
    monkeypatch.setattr(media,"fetch_image",lambda *a:pytest.fail("offline-only fetched network"))
    value=remote(local_fallback="fallback.png",asset_policy="offline_only")
    assert render_visuals(tmp_path,plan(value),{"ch1":"## Representation\n"})[1]["v1"]["status"]=="verified"


def test_remote_missing_metadata_and_snapshot_fail_closed(tmp_path,monkeypatch):
    monkeypatch.setattr(media,"fetch_image",lambda *a:pytest.fail("metadata should fail before acquisition"))
    value=remote(alt="")
    result=render_visuals(tmp_path,plan(value),{"ch1":"## Representation\n"})[1]["v1"]
    assert result["status"]=="failed" and "alt" in result["failure_reason"]
    value=remote()
    assert render_visuals(tmp_path,plan(value),{"ch1":"## Representation\n"},execute=False)[1]["v1"]["status"]=="failed"


def test_nested_chapter_links_resolve_to_actual_local_media_and_html(tmp_path,monkeypatch):
    (tmp_path/"fallback.png").write_bytes(png())
    value=remote(local_fallback="fallback.png",asset_policy="offline_only")
    collection=plan(value)
    collection["chapters"][0]["path"]="Full Notes/Topic/01 - Chapter.md"
    result=render_visuals(tmp_path,collection,{"ch1":"## Representation\n"})[1]["v1"]
    assert "](../../assets/scriptorium/" in result["embed"]
    value=visual(kind="interactive",frames=[{"label":"A","state":"1"},{"label":"B","state":"2"}])
    collection["visuals"]=[value]
    result=render_visuals(tmp_path,collection,{"ch1":"## Representation\n"})[1]["v1"]
    assert "](../../assets/scriptorium/" in result["embed"]


def test_svg_rejects_active_resources():
    assert validate_svg('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1"><style>@import "https://evil";</style></svg>')
    assert validate_svg('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1"><rect fill="url(https://evil)"/></svg>')
