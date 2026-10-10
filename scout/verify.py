#!/usr/bin/env python3
"""Offline content contract check; never imports the agent or calls providers."""
import ast
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_README_SHA256 = 'a626a979f449e5fd0917b23209dbdbc1e7afbea5d2b38bacd4d86dee667929e7'


def verify():
    templates = json.loads((ROOT / 'frontend/scout-workflows.json').read_text())
    assert len(templates) == 2
    assert len({item['id'] for item in templates}) == len(templates)
    enum_tree = ast.parse((ROOT / 'gpt_researcher/utils/enum.py').read_text())
    enums = {}
    for node in enum_tree.body:
        if isinstance(node, ast.ClassDef):
            enums[node.name] = {child.value.value for child in node.body if isinstance(child, ast.Assign) and isinstance(child.value, ast.Constant)}
    for item in templates:
        assert item['report_type'] in enums['ReportType']
        assert item['report_source'] in enums['ReportSource']
        assert re.findall(r'\{\{[^{}]+\}\}', item['task']), 'Each template needs fillable variables'
        document = ROOT / 'scout' / (item['id'] + '.md')
        assert item['task'] in document.read_text(), f'Template/document drift: {item["id"]}'
    html = (ROOT / 'frontend/index.html').read_text()
    assert 'id="scout-workflow"' in html and '/site/scout-templates.js' in html
    assert 'id="task"' in html
    assert 'https://github.com/assafelovic/gpt-researcher' in html
    assert 'Apache License' in (ROOT / 'LICENSE').read_text()
    assert hashlib.sha256((ROOT / 'docs/UPSTREAM_README.md').read_bytes()).hexdigest() == UPSTREAM_README_SHA256
    for path in (ROOT / '.github/workflows').glob('*.yml'):
        if path.name == 'scout-checks.yml':
            continue
        source = path.read_text()
        event_block = source.split('\non:', 1)[1].split('\n', 1)[1] if '\non:' in source else source.split('on:',1)[1]
        event_block = re.split(r'\n[^\s#]', event_block, maxsplit=1)[0]
        assert 'workflow_dispatch:' in event_block, path.name
        assert not re.search(r'^\s+(push|pull_request|schedule|release|workflow_run):', event_block, re.M), path.name
    print('PASS: 2 workflow templates, fillable variables, upstream enum values, UI wiring, README snapshot, license, inherited manual-only workflows')
    print('Scope: offline content checks only; no provider calls or full engine validation.')


if __name__ == '__main__':
    verify()
