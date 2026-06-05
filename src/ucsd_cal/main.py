from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import ics, parser

TEMPLATE = """\
# ucsd-cal schedule template
# Fill in your quarter dates and classes, then run:
#   ucsd-cal generate schedule.yaml -o calendar.ics

quarter:
  start: "2026-03-31"   # First day of instruction
  end:   "2026-06-07"   # Last day of instruction

classes:
  - name: "DSC 100"
    title: "Introduction to Data Management"
    days: [Monday, Wednesday, Friday]
    start_time: "10:00"
    end_time:   "10:50"
    location: "CENTR 115"

  - name: "DSC 140A"
    title: "Probabilistic Modeling"
    days: [Tuesday, Thursday]
    start_time: "14:00"
    end_time:   "15:20"
    location: "WLH 2005"
"""


def cmd_generate(args: argparse.Namespace) -> None:
    schedule_file = Path(args.schedule_file)
    output = Path(args.output)
    if not schedule_file.exists():
        print(f"Error: {schedule_file} not found.", file=sys.stderr)
        sys.exit(1)
    schedule = parser.load(schedule_file)
    calendar = ics.generate(schedule)
    output.write_text(calendar)
    print(f"Wrote {len(schedule.classes)} class(es) to {output}")
    print("Import the .ics file into Google Calendar via Settings → Import & Export.")


def cmd_template(args: argparse.Namespace) -> None:  # noqa: ARG001
    print(TEMPLATE, end="")


def main() -> None:
    p = argparse.ArgumentParser(
        description="Convert a UCSD class schedule into a Google Calendar ICS file."
    )
    sub = p.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="Generate an ICS calendar from a YAML schedule file.")
    gen.add_argument("schedule_file", help="Path to the YAML schedule file.")
    gen.add_argument("-o", "--output", default="calendar.ics", help="Output .ics file path.")
    gen.set_defaults(func=cmd_generate)

    tmpl = sub.add_parser("template", help="Print a template YAML schedule file to stdout.")
    tmpl.set_defaults(func=cmd_template)

    args = p.parse_args()
    args.func(args)
