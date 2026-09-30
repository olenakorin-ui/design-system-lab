#!/usr/bin/env python3
import json
import sys
from pathlib import Path

Path(sys.argv[1]).write_text(json.dumps(json.load(sys.stdin)), encoding="utf-8")
