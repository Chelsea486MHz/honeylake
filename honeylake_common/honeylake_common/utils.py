import hashlib
import base64
from typing import Dict


def compute_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encode_base64(data: bytes) -> str:
    return base64.b64encode(data).decode('utf-8')


def decode_base64(data: str) -> bytes:
    return base64.b64decode(data)


def get_real_client_ip(headers: Dict[str, str], remote_addr: str) -> str:
    real_ip = headers.get('X-Real-IP')
    if real_ip:
        return real_ip.strip()

    forwarded_for = headers.get('X-Forwarded-For')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()

    return remote_addr
