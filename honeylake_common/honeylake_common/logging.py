import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List, Union

from .utils import compute_sha256, encode_base64


logger = logging.getLogger(__name__)


def save_exploit_sample(
    cve: str,
    client_ip: str,
    headers: Dict[str, str],
    body: bytes,
    samples_dir: Path = Path('/samples'),
    honeypot: Optional[str] = None,
    client_port: Optional[int] = None,
    method: Optional[str] = None,
    path: Optional[str] = None,
    query_string: Optional[str] = None,
    protocol: Optional[str] = None,
    extracted_payloads: Optional[List[str]] = None,
    attack_type: Optional[str] = None,
    confidence: Optional[str] = None,
    **extra_metadata
) -> Path:
    samples_dir = Path(samples_dir)
    samples_dir.mkdir(exist_ok=True, parents=True)

    timestamp_dt = datetime.utcnow()
    timestamp = timestamp_dt.isoformat() + 'Z'

    timestamp_safe = timestamp_dt.strftime('%Y%m%d-%H%M%S-') + str(timestamp_dt.microsecond).zfill(6)

    client_ip_safe = client_ip.replace('.', '_').replace(':', '_')

    body_checksum = compute_sha256(body)
    body_encoded = encode_base64(body)

    sample_data = {
        "version": "1.0",
        "metadata": {
            "timestamp": timestamp,
            "cve": cve,
            "client_ip": client_ip,
        }
    }

    if honeypot:
        sample_data["metadata"]["honeypot"] = honeypot
    if client_port:
        sample_data["metadata"]["client_port"] = client_port

    sample_data["metadata"].update(extra_metadata)

    if method or path or headers:
        sample_data["request"] = {}
        if method:
            sample_data["request"]["method"] = method
        if path:
            sample_data["request"]["path"] = path
        if query_string:
            sample_data["request"]["query_string"] = query_string
        if protocol:
            sample_data["request"]["protocol"] = protocol
        if headers:
            sample_data["request"]["headers"] = dict(headers)

    sample_data["body"] = {
        "raw": body_encoded,
        "checksum": {
            "algorithm": "sha256",
            "value": body_checksum
        },
        "size": len(body)
    }

    if extracted_payloads or attack_type or confidence:
        sample_data["analysis"] = {}
        if extracted_payloads:
            sample_data["analysis"]["extracted_payloads"] = extracted_payloads
        if attack_type:
            sample_data["analysis"]["attack_type"] = attack_type
        if confidence:
            sample_data["analysis"]["confidence"] = confidence

    filename = f"{client_ip_safe}-{timestamp_safe}.json"
    filepath = samples_dir / filename

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved exploit sample: {filename}")
        return filepath

    except Exception as e:
        logger.error(f"Failed to save exploit sample: {e}")
        raise


def load_exploit_sample(filepath: Path) -> Dict[str, Any]:
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
