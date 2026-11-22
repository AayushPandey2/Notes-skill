"""Bounded remote PNG acquisition with pinned public DNS and offline receipts.

The dependency-free decoder deliberately supports noninterlaced 8-bit grayscale,
RGB and alpha PNGs. Other raster encodings require an explicit decoder adapter.
"""
from __future__ import annotations

import binascii
from html import escape
from datetime import datetime, timezone
import http.client
import ipaddress
import json
import os
from pathlib import Path
import re
import socket
import ssl
import struct
import tempfile
import time
from urllib.parse import urljoin, urlsplit, urlunsplit
import zlib

from scriptorium.models import content_hash

MAX_BYTES = 8 * 1024 * 1024
MAX_PIXELS = 4_000_000
TIMEOUT = 10
MAX_REDIRECTS = 3
POLICIES = frozenset({"remote_allowed", "local_preferred", "offline_only"})


def _url(value: str):
    if not isinstance(value,str) or re.search(r"[\s\x00-\x1f\x7f<>()\\]",value):
        raise ValueError("Image URL contains unsafe characters")
    parts = urlsplit(value)
    if parts.scheme != "https" or not parts.hostname or parts.username or parts.password or parts.port not in {None,443} or parts.fragment:
        raise ValueError("Media requires direct HTTPS without credentials, fragments or alternate ports")
    return parts


def _resolve_public(host: str) -> list[str]:
    addresses = list(dict.fromkeys(info[4][0] for info in socket.getaddrinfo(host,443,type=socket.SOCK_STREAM)))
    if not addresses or any(not ipaddress.ip_address(address).is_global for address in addresses):
        raise ValueError("Image host must resolve exclusively to public global addresses")
    return addresses


class _PinnedHTTPS(http.client.HTTPSConnection):
    def __init__(self, host: str, address: str):
        super().__init__(host,443,timeout=TIMEOUT,context=ssl.create_default_context())
        self._address = address

    def connect(self):
        # DNS is not resolved again after validation. TLS authenticates the hostname.
        raw = socket.create_connection((self._address,443),self.timeout)
        try:
            self.sock = self._context.wrap_socket(raw,server_hostname=self.host)
        except BaseException:
            raw.close()
            raise


def _request_once(url: str, host: str, address: str) -> tuple[int, dict, bytes]:
    parts = _url(url)
    connection = _PinnedHTTPS(host,address)
    target = urlunsplit(("","",parts.path or "/",parts.query,""))
    try:
        deadline = time.monotonic()+TIMEOUT
        connection.request("GET",target,headers={"Host":parts.netloc,"Accept":"image/png","Accept-Encoding":"identity","User-Agent":"Scriptorium-Media/5"})
        response = connection.getresponse()
        headers = {k.lower():v for k,v in response.getheaders()}
        if response.status in {301,302,303,307,308}:
            return response.status,headers,b""
        if response.status != 200:
            raise ValueError(f"Image HTTP status {response.status}")
        if headers.get("content-encoding", "identity").lower() not in {"identity",""}:
            raise ValueError("Compressed HTTP content encoding is not supported")
        length = headers.get("content-length")
        if length is not None and (not length.isdigit() or int(length) > MAX_BYTES):
            raise ValueError("Image exceeds the byte limit or has invalid content length")
        chunks, count = [], 0
        while count <= MAX_BYTES:
            remaining = deadline-time.monotonic()
            if remaining <= 0:
                raise ValueError("Image acquisition exceeded timeout")
            if connection.sock is not None:
                connection.sock.settimeout(remaining)
            chunk = response.read1(min(65536,MAX_BYTES+1-count))
            if not chunk:
                break
            chunks.append(chunk)
            count += len(chunk)
        raw = b"".join(chunks)
        if len(raw) > MAX_BYTES:
            raise ValueError("Image exceeds the byte limit")
        if length is not None and len(raw) != int(length):
            raise ValueError("Image response is truncated")
        return response.status,headers,raw
    finally:
        connection.close()


def fetch_image(url: str) -> tuple[bytes,dict]:
    """Validate DNS and pin the socket for every redirect; proxies are not used."""
    current, seen = url, set()
    for step in range(MAX_REDIRECTS+1):
        if current in seen:
            raise ValueError("Image redirect loop")
        seen.add(current)
        parts = _url(current)
        address = _resolve_public(parts.hostname)[0]
        status,headers,raw = _request_once(current,parts.hostname,address)
        if status in {301,302,303,307,308}:
            if step == MAX_REDIRECTS or not headers.get("location"):
                raise ValueError("Image redirect limit or missing location")
            current = urljoin(current,headers["location"])
            continue
        if status != 200:
            raise ValueError(f"Image HTTP status {status}")
        mime = headers.get("content-type", "").split(";",1)[0].strip().lower()
        dimensions = decode_png(raw,mime)
        return raw,{"url":url,"final_url":current,"mime":mime,"bytes":len(raw),**dimensions,
                    "redirects":step,"acquired_at":datetime.now(timezone.utc).isoformat(),
                    "availability":"observed at acquisition; not a continuing availability guarantee"}
    raise ValueError("Image redirect limit")


def decode_png(raw: bytes, mime: str = "image/png") -> dict:
    if len(raw) > MAX_BYTES or mime != "image/png" or not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("Only decoded PNG with matching image/png MIME is supported")
    position, compressed, ihdr, ended, idat_closed = 8, bytearray(), None, False, False
    while position < len(raw):
        if len(raw)-position < 12:
            raise ValueError("Truncated PNG chunk")
        length = struct.unpack(">I",raw[position:position+4])[0]
        kind = raw[position+4:position+8]
        end = position+12+length
        if end > len(raw) or length > MAX_BYTES:
            raise ValueError("Invalid PNG chunk length")
        payload = raw[position+8:position+8+length]
        crc = struct.unpack(">I",raw[position+8+length:end])[0]
        if not re.fullmatch(rb"[A-Za-z]{4}",kind) or binascii.crc32(kind+payload)&0xffffffff != crc:
            raise ValueError("Invalid PNG chunk checksum or type")
        if ihdr is None and kind != b"IHDR":
            raise ValueError("PNG must begin with IHDR")
        if kind == b"IHDR":
            if ihdr is not None or length != 13:
                raise ValueError("Invalid duplicate PNG header")
            width,height,depth,color,compression,filtering,interlace = struct.unpack(">IIBBBBB",payload)
            if not width or not height or width*height > MAX_PIXELS or max(width,height)>10000:
                raise ValueError("PNG exceeds bounded pixel dimensions")
            if depth != 8 or color not in {0,2,4,6} or compression or filtering or interlace:
                raise ValueError("PNG decoder supports noninterlaced 8-bit grayscale/RGB/alpha only")
            ihdr = (width,height,{0:1,2:3,4:2,6:4}[color])
        elif kind == b"IDAT":
            if idat_closed:
                raise ValueError("PNG IDAT chunks must be consecutive")
            compressed.extend(payload)
        elif kind == b"IEND":
            if length or not compressed or end != len(raw):
                raise ValueError("Invalid PNG end or trailing bytes")
            ended = True
            break
        else:
            if compressed:
                idat_closed = True
            if kind not in {b"PLTE"} and not kind[0]&32:
                raise ValueError("Unsupported critical PNG chunk")
        position = end
    if not ended or ihdr is None:
        raise ValueError("Incomplete PNG")
    width,height,channels = ihdr
    stride = width*channels
    expected = height*(stride+1)
    decoder = zlib.decompressobj()
    try:
        decoded = decoder.decompress(bytes(compressed),expected+1)
    except zlib.error as exc:
        raise ValueError("Invalid PNG compressed data") from exc
    if len(decoded) != expected or not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
        raise ValueError("PNG decoded scanline length disagrees with dimensions")
    # Reconstruct each scanline rather than accepting signature/header bytes alone.
    previous = bytearray(stride)
    for row_index in range(height):
        offset = row_index*(stride+1)
        filtering = decoded[offset]
        row = bytearray(decoded[offset+1:offset+stride+1])
        if filtering > 4:
            raise ValueError("Invalid PNG scanline filter")
        for i,value in enumerate(row):
            left = row[i-channels] if i >= channels else 0
            above = previous[i]
            upper_left = previous[i-channels] if i >= channels else 0
            if filtering == 1: prediction = left
            elif filtering == 2: prediction = above
            elif filtering == 3: prediction = (left+above)//2
            elif filtering == 4:
                p = left+above-upper_left
                distances = [abs(p-left),abs(p-above),abs(p-upper_left)]
                prediction = [left,above,upper_left][distances.index(min(distances))]
            else: prediction = 0
            row[i] = (value+prediction)&255
        previous = row
    return {"width":width,"height":height,"decoder":"bounded PNG scanline reconstruction"}


def _metadata(visual: dict) -> tuple[str,str,str,str]:
    fields = tuple(visual.get(k) for k in ("source","rights","alt","relevance"))
    if any(not isinstance(value,str) or not value.strip() or len(value)>2000 for value in fields):
        raise ValueError("Remote media needs source, rights, alt text and relevance rationale")
    _url(visual["url"])
    _url(fields[0])
    return fields


def _write_immutable(path: Path, raw: bytes):
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent,prefix=".media-",delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary,path)
        except FileExistsError:
            if path.read_bytes()!=raw:
                raise ValueError("Content-addressed media changed during acquisition")
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def media_artifact(vault: Path, visual: dict, digest: str, *, execute: bool) -> dict:
    from . import contained
    source,rights,alt,relevance = _metadata(visual)
    policy = visual.get("asset_policy","local_preferred")
    if policy not in POLICIES:
        raise ValueError("Unknown media asset policy")
    receipt_relative = f"assets/scriptorium/{digest}.media.json"
    receipt_path = contained(vault,receipt_relative)
    cached, fallback_used = receipt_path.is_file(), False
    if cached:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        if not isinstance(receipt,dict) or receipt.get("input_hash") != digest:
            raise ValueError("Media receipt does not bind its specification")
        path = contained(vault,receipt["path"])
        raw = path.read_bytes()
        if receipt.get("hash") != content_hash(raw):
            raise ValueError("Media snapshot changed since acquisition")
        decode_png(raw,receipt.get("mime"))
    else:
        if not execute:
            raise ValueError("Verified media snapshot and receipt are missing")
        fallback = visual.get("local_fallback")
        if policy == "offline_only":
            if not fallback:
                raise ValueError("Offline-only media requires an explicit local_fallback PNG")
            raw = contained(vault,fallback).read_bytes()
            provenance = {"mime":"image/png",**decode_png(raw),"acquisition":"explicit local fallback; network disabled"}
            fallback_used = True
        else:
            try:
                raw,provenance = fetch_image(visual["url"])
            except (OSError,ValueError,http.client.HTTPException) as exc:
                if not fallback:
                    raise ValueError(f"Remote image acquisition failed: {exc}") from exc
                raw = contained(vault,fallback).read_bytes()
                provenance = {"mime":"image/png",**decode_png(raw),"acquisition":"explicit local fallback",
                              "remote_failure":str(exc)}
                fallback_used = True
        decode_png(raw,provenance.get("mime"))
        relative = f"assets/scriptorium/{content_hash(raw)}.png"
        path = contained(vault,relative)
        if path.exists() and path.read_bytes()!=raw:
            raise ValueError("Content-addressed image was altered")
        if not path.exists():
            _write_immutable(path,raw)
        receipt = {**provenance,"input_hash":digest,"hash":content_hash(raw),"path":relative,
                   "source":source,"rights":rights,"alt":alt,"relevance":relevance,"asset_policy":policy,
                   "fallback_used":fallback_used,"rights_verification":"supplied rights statement; independently verify before redistribution"}
        _write_immutable(receipt_path,json.dumps(receipt,sort_keys=True,indent=2).encode("utf-8"))
    # Remote embedding requires an acquired URL, never a fallback. Parentheses are
    # rejected in URLs, and Markdown label metacharacters are escaped.
    target = receipt.get("final_url") if policy == "remote_allowed" and not receipt.get("fallback_used") else receipt["path"]
    if target.startswith("https:"):
        _url(target)
    clean_alt = re.sub(r"([\\\[\]*_`])",r"\\\1",alt).replace("\n"," ").replace("\r"," ")
    clean_rights = re.sub(r"([\\\[\]*_`])",r"\\\1",escape(rights)).replace("\n"," ").replace("\r"," ")
    embed = f"![{escape(clean_alt)}]({target})\n\n*Source: [original publication]({source}); rights: {clean_rights}*"
    return {"path":receipt["path"],"hash":receipt["hash"],"embed":embed,"provenance":receipt,
            "media_receipt":receipt_relative,"cached":cached,"validation":{"result":"pass",
              "method":"decode PNG, compare snapshot SHA-256 and specification-bound acquisition receipt",
              "limits":"Live availability established only at acquisition; image relevance and supplied rights need editorial review."}}
