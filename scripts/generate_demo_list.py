#!/usr/bin/env python3
"""Generate initial demo-list.md file"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from opendemo.core.demo_list_updater import DemoListUpdater

output_dir = Path(__file__).parent.parent / "opendemo_output"
demo_list_path = Path(__file__).parent.parent / "demo-list.md"

print(f"Output directory: {output_dir}")
print(f"Demo list path: {demo_list_path}")

updater = DemoListUpdater(output_dir, demo_list_path)
success = updater.update()

if success:
    print(f"Success: {updater.get_summary()}")
else:
    print("Failed to generate demo-list.md")
