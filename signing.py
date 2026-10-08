"""ช่วยเซ็นไฟล์ด้วย Ed25519 — อ่านกุญแจลับจากตัวแปรสภาพแวดล้อม SIGNING_KEY"""
import base64
import os
import sys
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def load_key() -> Ed25519PrivateKey:
    b64 = os.environ.get("SIGNING_KEY", "").strip()
    if not b64:
        sys.exit("ไม่พบ SIGNING_KEY (ตั้งเป็น GitHub Secret หรือ environment variable)")
    return Ed25519PrivateKey.from_private_bytes(base64.b64decode(b64))


def sign_file(path, key) -> None:
    sig = key.sign(Path(path).read_bytes())
    Path(str(path) + ".sig").write_text(base64.b64encode(sig).decode())
