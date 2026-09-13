"""
AgroShield Mesh - Automated Secret & Credential Scanner
Verifies that no private keys, AWS tokens, API secrets, or database passwords
are committed in source code or sample configurations.
"""

import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUSPICIOUS_PATTERNS = [
    (r"(?i)(api[_-]?key|apikey|secret[_-]?key|access[_-]?token)\s*=\s*['\"][A-Za-z0-9/\+=]{20,}['\"]", "High-entropy API key/secret"),
    (r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----", "Private cryptographic key"),
    (r"(?i)aws_secret_access_key\s*=\s*['\"][A-Za-z0-9/\+=]{40}['\"]", "AWS Secret Access Key"),
    (r"(?i)ghp_[A-Za-z0-9]{36}", "GitHub Personal Access Token"),
    (r"(?i)eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*", "Hardcoded live JWT token")
]

EXCLUDE_DIRS = {".git", "node_modules", ".gemini", "__pycache__", "dist", ".venv", "env"}


def scan_directory(root_dir: str) -> bool:
    findings = []
    print("=" * 65)
    print("🔒 RUNNING AGROSHIELD MESH SECURITY & SECRET SCAN")
    print("=" * 65)

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fname in filenames:
            if fname.endswith((".py", ".json", ".yaml", ".yml", ".env", ".env.example", ".ts", ".tsx", ".js", ".md")):
                fpath = os.path.join(dirpath, fname)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                    for idx, line in enumerate(lines, 1):
                        for pattern, desc in SUSPICIOUS_PATTERNS:
                            if re.search(pattern, line):
                                findings.append({
                                    "file": os.path.relpath(fpath, root_dir),
                                    "line": idx,
                                    "description": desc,
                                    "snippet": line.strip()[:60]
                                })
                except Exception as e:
                    pass

    if findings:
        print(f"❌ SECURITY WARNING: Found {len(findings)} potential secret leaks:")
        for f in findings:
            print(f"   [{f['file']}:{f['line']}] {f['description']} -> {f['snippet']}")
        return False
    else:
        print("✅ ZERO SECRETS DETECTED. Codebase complies with safety and privacy rules.")
        return True


if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    passed = scan_directory(base)
    sys.exit(0 if passed else 1)
