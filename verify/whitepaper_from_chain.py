"""Extract the whitepaper from the Bitcoin block chain and hash it.

The canonical PDF was embedded in mainnet transaction
  54e48e5f5c656b26c3bca14a8c95aa583d07ebe84dde3b7dd4a78f4e4186e713
as 946 bare-multisig outputs whose "public keys" are really PDF bytes -- 945 holding three 65-byte
pushes each, plus one holding the 33-byte tail. (The transaction has 948 outputs in total; the last
two are ordinary P2PKH.) Reassembling them gives back the file byte for byte.

Why this matters to this lab's grading: it is the ONLY copy of any whitepaper version carrying a
CHAIN-class anchor. Proof-of-work cannot be backdated, so this fixes the canonical text to the block
that confirmed it -- 2013, not 2008. It says nothing about October 2008, and it is not offered as if
it did. It does mean the file we ship cannot have been altered since that block.

Reproducible from any node with txindex (`bitcoin-cli getrawtransaction <txid> 1`) or, as here, from
a public API so it can be checked without one.

THE CONTAINER FORMAT IS SPECIFIED BY THE CHAIN, NOT BY US
  [4-byte length, little-endian][4-byte CRC32, little-endian][body][zero padding to fill the last push]

  This is not our inference. The DOWNLOADER that reads these transactions was itself embedded,
  three hours earlier, in tx 6c53cd987119ef797d5adccd76241247988a0a5ef783572a9972e7371c5fb0cc
  (block 229,991), and its own code reads:

      length   = struct.unpack('<L', data[0:4])[0]
      checksum = struct.unpack('<L', data[4:8])[0]
      data     = data[8:8+length]
      if checksum != crc32(data): abort

  => So the length is READ, never hardcoded. An earlier version of this script carried a literal
     184292. That constant was correct, but a tool that asserts its own constant cannot tell you
     that the chain disagrees with it -- and a carve that ended one byte early (at %%EOF, dropping
     the trailing newline) produced a confident non-matching digest that looked like a finding
     about the artifact and was really a finding about the tool.

WHY BOTH CHECKS, AND WHAT EACH ONE IS FOR
  The CRC32 is the ENCODER's own claim about its payload; the SHA-256 is OUR claim about which file
  that payload should be. They fail for different reasons and the pair is diagnostic:

      CRC32    SHA-256   MEANING
      ok       ok        the canonical whitepaper, intact. Both parties agree.
      ok       FAIL      the carve is sound and the chain holds a DIFFERENT file. A real finding.
      FAIL     --        the carve or the transport is broken. Says NOTHING about the chain, and
                         no conclusion about the artifact may be drawn from it.

  A single check cannot separate the middle row from the last one, which is the whole point.
"""
import urllib.request, json, sys, hashlib, re, struct, datetime
from binascii import crc32

sys.stdout.reconfigure(encoding="utf-8")
TXID = "54e48e5f5c656b26c3bca14a8c95aa583d07ebe84dde3b7dd4a78f4e4186e713"
UA = {"User-Agent": "obl-archive/1.0 (provenance check)"}
OUT = sys.argv[1] if len(sys.argv) > 1 else "chain-bitcoin.pdf"

# TXID IS DELIBERATELY FIXED AND THIS SCRIPT TAKES NO TRANSACTION ARGUMENT. It is a
# verifier for one known artifact, not a general-purpose chain-data extractor, and
# refusing the parameter is the cheapest way to keep it that way no matter who runs it.
# Do not add a --txid flag.
CANON = "b1674191a88ec5cdd733e4240a81803105dc412d6c6708d53ab94fc248f4f553"


def get(u, t=120):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t).read()


tx = json.loads(get(f"https://blockstream.info/api/tx/{TXID}"))
when = datetime.datetime.fromtimestamp(tx["status"]["block_time"], datetime.timezone.utc)
print(f"  tx      {TXID}")
print(f"  block   {tx['status']['block_height']}   {tx['status'].get('block_hash','')[:32]}...")
print(f"  time    {when:%Y-%m-%d %H:%M:%S} UTC")
print(f"  outputs {len(tx['vout'])}")

chunks = []
for o in tx["vout"]:
    asm = o.get("scriptpubkey_asm", "")
    if "OP_CHECKMULTISIG" not in asm:
        continue                      # vout[946..947] are ordinary P2PKH change, not data
    # Bare multisig: the "public keys" carry file bytes. Keep them WHOLE -- the 0x04 prefixes are
    # part of the stream, not framing; stripping them corrupts the file. 945 outputs hold three
    # 65-byte keys each; vout[945] is a 1-of-1 holding the 33-byte tail.
    #
    # The 33 is not a special case we invented either: the on-chain ENCODER (tx 4b72a223..., same
    # block as the downloader) pads a short final chunk to 33 bytes if it is under 33, and to 65
    # otherwise. Requiring 65 here silently drops the tail of any file whose length lands in that
    # window -- which is what happened, and it cost the last 25 bytes of this PDF.
    chunks += re.findall(r"OP_PUSHBYTES_(?:65|33) ([0-9a-f]+)", asm)

raw = bytes.fromhex("".join(chunks))
if len(raw) < 8:
    sys.exit(f"\n  ABORT: only {len(raw)} byte(s) carved; the 8-byte header is not present. "
             "Nothing can be concluded about the artifact from this.")
length, checksum = struct.unpack("<II", raw[:8])
pdf = raw[8:8 + length]

print(f"  data pushes {len(chunks)}, {len(raw):,} bytes carved")
print(f"  header declares length {length:,} and crc32 {checksum:#010x}")
if len(pdf) != length:
    sys.exit(f"\n  ABORT: header declares {length:,} bytes but only {len(pdf):,} were carved.")

crc_ok = (crc32(pdf) & 0xffffffff) == checksum
print(f"  starts {pdf[:8]!r}   ends {pdf[-16:]!r}")
print(f"\n  crc32   {crc32(pdf) & 0xffffffff:#010x}   MATCH: {crc_ok}   (the encoder's own check)")

open(OUT, "wb").write(pdf)

h = hashlib.sha256(pdf).hexdigest()
sha_ok = h == CANON
print(f"  sha256  {h}")
print(f"  canonical b1674191...f4f553")
print(f"  MATCH: {sha_ok}")

if crc_ok and sha_ok:
    print("\n  => the canonical whitepaper, intact, anchored to block "
          f"{tx['status']['block_height']}.")
elif crc_ok:
    print("\n  => CARVE IS SOUND AND THE FILE DIFFERS. This is a finding about the chain.")
else:
    print("\n  => CARVE OR TRANSPORT IS BROKEN. Draw no conclusion about the artifact from this.")
sys.exit(0 if (crc_ok and sha_ok) else 1)
