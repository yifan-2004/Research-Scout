#!/usr/bin/env python3
"""Find obvious credential shapes without printing any credential values.

This heuristic is a content check, not a guarantee that all secrets are absent.
Git history is deliberately excluded; only the current source snapshot is checked.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', '.next'}
PATTERNS = {
    'langsmith': re.compile(r'lsv2_(?:pt|sk)_[A-Za-z0-9_\-]{20,}'),
    'openai': re.compile(r'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_\-]{28,}'),
    'github': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})'),
    'aws-access': re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    'tavily': re.compile(r'\btvly-[A-Za-z0-9_\-]{20,}'),
    'google': re.compile(r'\bAIza[A-Za-z0-9_\-]{30,}'),
    'private-key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'slack': re.compile(r'\bxox[baprs]-[A-Za-z0-9\-]{20,}'),
}


def main():
    found = []
    scanned = 0
    for path in ROOT.rglob('*'):
        relative = path.relative_to(ROOT)
        if any(part in EXCLUDE for part in relative.parts) or not path.is_file() or path.is_symlink():
            continue
        if path.stat().st_size > 10_000_000:
            continue
        try:
            content = path.read_text()
        except (UnicodeDecodeError, OSError):
            continue
        scanned += 1
        for label, pattern in PATTERNS.items():
            if pattern.search(content):
                found.append((relative, label))
    for path, label in found:
        print(f'REVIEW: {path} ({label})')
    print(f'Scanned {scanned} current text files; credential-pattern candidate paths: {len(found)}.')
    print('Values are never printed; history, binary files and files over 10 MB are excluded.')
    return bool(found)


if __name__ == '__main__':
    sys.exit(main())
