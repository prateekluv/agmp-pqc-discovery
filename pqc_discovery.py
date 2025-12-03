#!/usr/bin/env python3
"""
AGMP PQC Discovery Toolkit — v0.1

Basic cryptographic discovery helper:
- TLS endpoint scanner
- Source code crypto usage scanner
- CBOM-style output (CSV + JSON)

Author: AGMP Consulting
"""

import argparse
import csv
import json
import os
import re
import socket
import ssl
from datetime import datetime
from typing import List, Dict, Any


# -----------------------------
# TLS SCANNING
# -----------------------------

def scan_tls_endpoint(host: str, port: int = 443, timeout: int = 5) -> Dict[str, Any]:
    """Connects to a TLS endpoint and returns crypto properties."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    result = {
        "host": host,
        "port": port,
        "protocol": None,
        "cipher_suite": None,
        "cert_subject": None,
        "cert_issuer": None,
        "cert_not_before": None,
        "cert_not_after": None,
        "error": None,
    }

    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cipher = ssock.cipher()
                result["protocol"] = ssock.version()
                result["cipher_suite"] = cipher[0] if cipher else None

                cert = ssock.getpeercert()
                if cert:
                    subject = dict(x[0] for x in cert.get("subject", []))
                    issuer = dict(x[0] for x in cert.get("issuer", []))
                    result["cert_subject"] = subject.get("commonName")
                    result["cert_issuer"] = issuer.get("commonName")
                    result["cert_not_before"] = cert.get("notBefore")
                    result["cert_not_after"] = cert.get("notAfter")
    except Exception as e:
        result["error"] = str(e)

    return result


def scan_tls_file(targets_file: str) -> List[Dict[str, Any]]:
    """Reads host:port entries from a file and scans each."""
    results = []
    with open(targets_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            host, port = (line.split(":", 1) + ["443"])[:2]
            port = int(port)

            print(f"[TLS] Scanning {host}:{port} ...")
            results.append(scan_tls_endpoint(host, port))
    return results


# -----------------------------
# SOURCE CODE SCANNING
# -----------------------------

DEFAULT_EXTENSIONS = [".py", ".js", ".ts", ".java", ".go", ".cs"]

CRYPTO_PATTERNS = {
    "python": [
        r"\bimport\s+cryptography\b",
        r"\bfrom\s+cryptography\b",
        r"\bimport\s+Crypto\b",
        r"\bfrom\s+Crypto\b",
        r"\bimport\s+OpenSSL\b",
        r"\bFernet\b",
    ],
    "javascript": [
        r"\brequire\(['\"]crypto['\"]\)",
        r"\bwindow\.crypto\b",
        r"\bcrypto\.subtle\b",
        r"\bjsonwebtoken\b",
    ],
    "java": [
        r"\bjavax\.crypto\b",
        r"\bjava\.security\b",
        r"\bKeyPairGenerator\b",
        r"\bCipher\.getInstance\b",
    ],
    "go": [
        r"\bcrypto/(rsa|ecdsa|x509|tls)\b",
    ],
    "csharp": [
        r"\bSystem\.Security\.Cryptography\b",
    ],
}

EXT_LANG_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "javascript",
    ".java": "java",
    ".go": "go",
    ".cs": "csharp",
}


def scan_codebase(root_dir: str) -> List[Dict[str, Any]]:
    """Walk directories & scan files for crypto patterns."""
    findings = []

    for dirpath, _, filenames in os.walk(root_dir):
        for fn in filenames:
            _, ext = os.path.splitext(fn)
            if ext.lower() not in DEFAULT_EXTENSIONS:
                continue

            lang = EXT_LANG_MAP.get(ext.lower())
            patterns = CRYPTO_PATTERNS.get(lang, [])

            full_path = os.path.join(dirpath, fn)

            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception:
                continue

            for pattern in patterns:
                for match in re.finditer(pattern, content):
                    snippet_start = max(0, match.start() - 60)
                    snippet_end = min(len(content), match.end() + 60)
                    snippet = content[snippet_start:snippet_end].replace("\n", " ")

                    findings.append({
                        "file_path": full_path,
                        "language": lang,
                        "pattern": pattern,
                        "snippet": snippet[:200],
                    })
    return findings


# -----------------------------
# OUTPUT HELPERS
# -----------------------------

def write_csv(path: str, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        print(f"[OUT] No data for {path}")
        return
    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[OUT] Wrote CSV → {path}")


def write_json(path: str, rows: List[Dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)
    print(f"[OUT] Wrote JSON → {path}")


# -----------------------------
# CLI ENTRY POINT
# -----------------------------

def main():
    parser = argparse.ArgumentParser(description="AGMP PQC Discovery Toolkit")
    parser.add_argument("--tls-targets", help="File containing host:port list")
    parser.add_argument("--code-root", help="Directory to scan for crypto")
    parser.add_argument(
        "--out-prefix",
        default=f"cbom_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        help="Prefix for output files"
    )

    args = parser.parse_args()

    if not args.tls_targets and not args.code_root:
        parser.error("You must specify at least --tls-targets or --code-root")

    if args.tls_targets:
        tls_results = scan_tls_file(args.tls_targets)
        write_csv(f"{args.out_prefix}_tls.csv", tls_results)
        write_json(f"{args.out_prefix}_tls.json", tls_results)

    if args.code_root:
        code_results = scan_codebase(args.code_root)
        write_csv(f"{args.out_prefix}_code.csv", code_results)
        write_json(f"{args.out_prefix}_code.json", code_results)


if __name__ == "__main__":
    main()
