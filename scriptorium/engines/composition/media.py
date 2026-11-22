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
import xml.etree.ElementTree as ET
import zlib

from scriptorium.models import content_hash, slugify

MAX_BYTES = 8 * 1024 * 1024
MAX_PIXELS = 8_000_000
TIMEOUT = 10
MAX_REDIRECTS = 3
POLICIES = frozenset({"remote_allowed", "local_preferred", "offline_only"})
SUPPORTED_MIMES = {
    "image/png": "png",
    "image/svg+xml": "svg",
    "image/jpeg": "jpg",
    "image/webp": "webp",
}
PERMISSIVE_LICENSE_PATTERNS = (
    r"\bcc0\b",
    r"\bcc[\s-]*by(?:[\s-]*(?:sa|nc|nd))?\b",
    r"\bpublic\s+domain\b",
    r"\bmit\b",
    r"\bapache[\s-]*2(?:\.0)?\b",
    r"\bbsd\b",
    r"\bopen[\s-]+access\b",
    r"\bauthor[\s-]+permitted\b",
)
RESTRICTIVE_LICENSE_PATTERNS = (
    r"\ball\s+rights\s+reserved\b",
    r"\bunknown\b",
    r"\bunclear\b",
    r"\bunverified\b",
    r"\bno\s+redistribution\b",
)


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
        connection.request("GET",target,headers={"Host":parts.netloc,"Accept":"image/svg+xml, image/png, image/jpeg, image/webp","Accept-Encoding":"identity","User-Agent":"Scriptorium-Media/5.1 (https://github.com/AayushPandey2/Notes-skill)"})
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
        dimensions = validate_image_bytes(raw,mime)
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
            if depth != 8 or color not in {0, 2, 3, 4, 6} or compression or filtering or interlace not in {0, 1}:
                raise ValueError("PNG decoder supports 8-bit grayscale/RGB/indexed/alpha PNGs only")
            ihdr = (width, height, {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[color], interlace)
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
    width, height, channels, interlace = ihdr
    if interlace == 0:
        stride = width * channels
        expected = height * (stride + 1)
    else:
        # Adam7 7-pass interlace scanline byte count
        adam7 = ((0, 0, 8, 8), (4, 0, 8, 8), (0, 4, 4, 8), (2, 0, 4, 4), (0, 2, 2, 4), (1, 0, 2, 2), (0, 1, 1, 2))
        expected = 0
        for x0, y0, dx, dy in adam7:
            pw = (width - x0 + dx - 1) // dx if width > x0 else 0
            ph = (height - y0 + dy - 1) // dy if height > y0 else 0
            if pw > 0 and ph > 0:
                expected += ph * (pw * channels + 1)
    decoder = zlib.decompressobj()
    try:
        decoded = decoder.decompress(bytes(compressed), expected + 1)
    except zlib.error as exc:
        raise ValueError("Invalid PNG compressed data") from exc
    if len(decoded) != expected or not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
        raise ValueError("PNG decoded scanline length disagrees with dimensions")
    # Reconstruct each scanline rather than accepting signature/header bytes alone.
    if interlace == 0:
        previous = bytearray(width * channels)
        stride = width * channels
        for row_index in range(height):
            offset = row_index * (stride + 1)
            filtering = decoded[offset]
            row = bytearray(decoded[offset + 1:offset + stride + 1])
            if filtering > 4:
                raise ValueError("Invalid PNG scanline filter")
            for i, value in enumerate(row):
                left = row[i - channels] if i >= channels else 0
                above = previous[i]
                upper_left = previous[i - channels] if i >= channels else 0
                if filtering == 1: prediction = left
                elif filtering == 2: prediction = above
                elif filtering == 3: prediction = (left + above) // 2
                elif filtering == 4:
                    p = left + above - upper_left
                    distances = [abs(p - left), abs(p - above), abs(p - upper_left)]
                    prediction = [left, above, upper_left][distances.index(min(distances))]
                else: prediction = 0
                row[i] = (value + prediction) & 255
            previous = row
    else:
        pos = 0
        for x0, y0, dx, dy in ((0, 0, 8, 8), (4, 0, 8, 8), (0, 4, 4, 8), (2, 0, 4, 4), (0, 2, 2, 4), (1, 0, 2, 2), (0, 1, 1, 2)):
            pw = (width - x0 + dx - 1) // dx if width > x0 else 0
            ph = (height - y0 + dy - 1) // dy if height > y0 else 0
            if pw > 0 and ph > 0:
                p_stride = pw * channels
                for _ in range(ph):
                    if decoded[pos] > 4:
                        raise ValueError("Invalid PNG scanline filter")
                    pos += p_stride + 1
    return {"width":width,"height":height,"decoder":"bounded PNG scanline reconstruction"}


def decode_jpeg(raw: bytes, mime: str = "image/jpeg") -> dict:
    """Validate bounded JPEG SOI/SOF dimensions and EOI without external codecs."""
    if len(raw) > MAX_BYTES or mime not in {"image/jpeg", "image/jpg"} or not raw.startswith(b"\xff\xd8"):
        raise ValueError("Only valid JPEG with matching image/jpeg MIME is supported")
    pos = 2
    width = height = None
    while pos + 1 < len(raw):
        if raw[pos] != 0xFF:
            raise ValueError("Invalid JPEG marker stream")
        while pos < len(raw) and raw[pos] == 0xFF:
            pos += 1
        if pos >= len(raw):
            break
        marker = raw[pos]
        pos += 1
        if marker == 0xD9:  # EOI
            if width is None or height is None:
                raise ValueError("JPEG missing frame header")
            return {"width": width, "height": height, "decoder": "bounded JPEG SOF parser"}
        if marker in {0x00, 0x01} or 0xD0 <= marker <= 0xD7:
            continue
        if pos + 2 > len(raw):
            raise ValueError("Truncated JPEG segment")
        seg_len = struct.unpack(">H", raw[pos:pos + 2])[0]
        if seg_len < 2 or pos + seg_len > len(raw):
            raise ValueError("Invalid JPEG segment length")
        if marker in {0xC0, 0xC1, 0xC2}:
            if seg_len < 7:
                raise ValueError("Truncated JPEG SOF header")
            height, width = struct.unpack(">HH", raw[pos + 3:pos + 7])
            if not width or not height or width * height > MAX_PIXELS or max(width, height) > 10000:
                raise ValueError("JPEG exceeds bounded pixel dimensions")
        if marker == 0xDA:  # SOS: scan until EOI at end
            if raw.endswith(b"\xff\xd9") and width is not None and height is not None:
                return {"width": width, "height": height, "decoder": "bounded JPEG SOF parser"}
            raise ValueError("JPEG missing EOI or frame header")
        pos += seg_len
    raise ValueError("Incomplete JPEG")


def decode_webp(raw: bytes, mime: str = "image/webp") -> dict:
    """Validate bounded RIFF/WEBP container and VP8/VP8L/VP8X dimensions."""
    if len(raw) > MAX_BYTES or mime != "image/webp" or len(raw) < 25 or raw[:4] != b"RIFF" or raw[8:12] != b"WEBP":
        raise ValueError("Only valid WebP with matching image/webp MIME is supported")
    riff_size = struct.unpack("<I", raw[4:8])[0]
    if riff_size + 8 > len(raw):
        raise ValueError("Truncated WebP RIFF container")
    chunk = raw[12:16]
    width = height = None
    if chunk == b"VP8X" and len(raw) >= 30:
        width = 1 + int.from_bytes(raw[24:27], "little")
        height = 1 + int.from_bytes(raw[27:30], "little")
    elif chunk == b"VP8L" and len(raw) >= 25 and raw[20] == 0x2F:
        bits = struct.unpack("<I", raw[21:25])[0]
        width = (bits & 0x3FFF) + 1
        height = ((bits >> 14) & 0x3FFF) + 1
    elif chunk == b"VP8 " and len(raw) >= 30 and raw[23:26] == b"\x9d\x01\x2a":
        width = struct.unpack("<H", raw[26:28])[0] & 0x3FFF
        height = struct.unpack("<H", raw[28:30])[0] & 0x3FFF
    else:
        raise ValueError("Unsupported or malformed WebP bitstream")
    if not width or not height or width * height > MAX_PIXELS or max(width, height) > 10000:
        raise ValueError("WebP exceeds bounded pixel dimensions")
    return {"width": width, "height": height, "decoder": "bounded WebP header parser"}


def validate_svg_bytes(raw: bytes, mime: str = "image/svg+xml") -> dict:
    """Sanitize and validate downloaded SVG against active scripts and external refs."""
    from .visuals import validate_svg
    if len(raw) > MAX_BYTES or mime != "image/svg+xml":
        raise ValueError("Only bounded SVG with matching image/svg+xml MIME is supported")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("SVG must be valid UTF-8") from exc
    if re.search(r"<!DOCTYPE|<!ENTITY", text, re.I):
        raise ValueError("SVG DOCTYPE and XML entities are forbidden")
    issues = validate_svg(text)
    if issues:
        raise ValueError("; ".join(issues))
    root = ET.fromstring(text)
    return {"width": root.get("width") or "viewBox", "height": root.get("height") or "viewBox",
            "decoder": "bounded XML/SVG allowlist sanitizer"}


def validate_image_bytes(raw: bytes, mime: str) -> dict:
    """Validate downloaded or local image bytes according to declared MIME type."""
    normalized = mime.split(";", 1)[0].strip().lower()
    if normalized == "image/png":
        return decode_png(raw, normalized)
    if normalized == "image/svg+xml":
        return validate_svg_bytes(raw, normalized)
    if normalized in {"image/jpeg", "image/jpg"}:
        return decode_jpeg(raw, normalized)
    if normalized == "image/webp":
        return decode_webp(raw, normalized)
    raise ValueError(f"Unsupported image MIME type: {mime}")


def verify_license_and_rights(rights: str, *, require_permissive: bool = False) -> dict:
    """Verify supplied license metadata before local persistence or reuse."""
    text = (rights or "").strip()
    if not text:
        raise ValueError("Missing license or rights statement")
    lowered = text.casefold()
    if any(re.search(pat, lowered) for pat in RESTRICTIVE_LICENSE_PATTERNS):
        raise ValueError(f"License prohibits or leaves unclear local reuse: {text}")
    permissive = any(re.search(pat, lowered) for pat in PERMISSIVE_LICENSE_PATTERNS)
    if require_permissive and not permissive:
        raise ValueError(f"License is not an established permissive/open-access grant: {text}")
    return {"rights": text, "permissive": permissive, "local_copy_permitted": permissive or not require_permissive}


def _metadata(visual: dict) -> tuple[str,str,str,str]:
    fields = tuple(visual.get(k) for k in ("source","rights","alt","relevance"))
    if any(not isinstance(value,str) or not value.strip() or len(value)>2000 for value in fields):
        raise ValueError("Remote media needs source, rights, alt text and relevance rationale")
    policy = visual.get("asset_policy", "local_preferred")
    if policy != "offline_only":
        _url(visual["url"])
        _url(fields[0])
    elif visual.get("url"):
        _url(visual["url"])
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
        if visual.get("require_permissive_license"):
            verify_license_and_rights(rights, require_permissive=True)
        fallback = visual.get("local_fallback")
        if policy == "offline_only":
            if not fallback:
                raise ValueError("Offline-only media requires an explicit local_fallback image")
            fb_path = contained(vault,fallback)
            raw = fb_path.read_bytes()
            fb_mime = visual.get("fallback_mime") or {
                ".svg": "image/svg+xml", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"
            }.get(fb_path.suffix.lower(), "image/png")
            provenance = {"mime":fb_mime,**validate_image_bytes(raw, fb_mime),"acquisition":"explicit local fallback; network disabled"}
            fallback_used = True
        else:
            try:
                raw,provenance = fetch_image(visual["url"])
            except (OSError,ValueError,http.client.HTTPException) as exc:
                if not fallback:
                    raise ValueError(f"Remote image acquisition failed: {exc}") from exc
                fb_path = contained(vault,fallback)
                raw = fb_path.read_bytes()
                fb_mime = visual.get("fallback_mime") or {
                    ".svg": "image/svg+xml", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"
                }.get(fb_path.suffix.lower(), "image/png")
                provenance = {"mime":fb_mime,**validate_image_bytes(raw, fb_mime),"acquisition":"explicit local fallback",
                              "remote_failure":str(exc)}
                fallback_used = True
        mime = provenance.get("mime", "image/png")
        validate_image_bytes(raw, mime)
        ext = SUPPORTED_MIMES.get(mime, "png")
        digest_hex = content_hash(raw)
        collection = visual.get("collection_slug")
        label = visual.get("asset_name") or visual.get("id")
        if collection and label:
            relative = f"assets/scriptorium/{slugify(collection)}/{slugify(label)}-{digest_hex[:12]}.{ext}"
        else:
            relative = f"assets/scriptorium/{digest_hex}.{ext}"
        path = contained(vault,relative)
        if path.exists() and path.read_bytes()!=raw:
            raise ValueError("Content-addressed image was altered")
        if not path.exists():
            _write_immutable(path,raw)
        receipt = {**provenance,"input_hash":digest,"hash":digest_hex,"path":relative,
                   "source":source,"rights":rights,"alt":alt,"relevance":relevance,"asset_policy":policy,
                   "fallback_used":fallback_used,"rights_verification":"supplied rights statement; independently verify before redistribution"}
        _write_immutable(receipt_path,json.dumps(receipt,sort_keys=True,indent=2).encode("utf-8"))
    # Local-first embedding: local_preferred and offline_only always reference local vault assets.
    target = receipt.get("final_url") if policy == "remote_allowed" and not receipt.get("fallback_used") else receipt["path"]
    if target.startswith("https:"):
        _url(target)
    clean_alt = re.sub(r"([\\\[\]*_`])",r"\\\1",alt).replace("\n"," ").replace("\r"," ")
    clean_rights = re.sub(r"([\\\[\]*_`])",r"\\\1",escape(rights)).replace("\n"," ").replace("\r"," ")
    if not target.startswith("https:") and visual.get("embed_style") == "wikilink":
        embed = f"![[{target}]]\n\n*Figure: {escape(clean_alt)}*\n\n*Source: [original publication]({source}); rights: {clean_rights}*"
    else:
        embed = f"![{escape(clean_alt)}]({target})\n\n*Source: [original publication]({source}); rights: {clean_rights}*"
    return {"path":receipt["path"],"hash":receipt["hash"],"embed":embed,"provenance":receipt,
            "media_receipt":receipt_relative,"cached":cached,"validation":{"result":"pass",
              "method":"validate bounded image bytes (PNG/SVG/JPEG/WebP), compare snapshot SHA-256 and specification-bound acquisition receipt",
              "limits":"Live availability established only at acquisition; image relevance and supplied rights need editorial review."}}
