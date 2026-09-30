#!/usr/bin/env python3
"""Write MCP JSON response from stdin to staging path."""
from __future__ import annotations

import json
import sys
from pathlib import Path

Path(sys.argv[1]).write_text(json.dumps(json.load(sys.stdin)), encoding="utf-8")
