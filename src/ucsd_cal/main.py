from __future__ import annotations

from pathlib import Path

import typer

from . import ics, parser

app = typer.Typer(help="Convert a UCSD class schedule into a Google Calendar ICS file.")

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


@app.command()
def generate(
    schedule_file: Path = typer.Argument(..., help="Path to the YAML schedule file."),
    output: Path = typer.Option(Path("calendar.ics"), "-o", "--output", help="Output .ics file path."),
) -> None:
    """Generate an ICS calendar from a YAML schedule file."""
    if not schedule_file.exists():
        typer.echo(f"Error: {schedule_file} not found.", err=True)
        raise typer.Exit(1)

    schedule = parser.load(schedule_file)
    calendar = ics.generate(schedule)
    output.write_bytes(calendar.to_ical())
    typer.echo(f"Wrote {len(schedule.classes)} class(es) to {output}")
    typer.echo("Import the .ics file into Google Calendar via Settings → Import & Export.")


@app.command()
def template() -> None:
    """Print a template YAML schedule file to stdout."""
    typer.echo(TEMPLATE, nl=False)


def main() -> None:
    app()
