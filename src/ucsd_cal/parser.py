from __future__ import annotations

import yaml
from dataclasses import dataclass
from datetime import date, time
from pathlib import Path

DAY_MAP = {
    "Monday": "MO",
    "Tuesday": "TU",
    "Wednesday": "WE",
    "Thursday": "TH",
    "Friday": "FR",
    "Saturday": "SA",
    "Sunday": "SU",
}

ABBREV_MAP = {
    "Mo": "MO", "M": "MO",
    "Tu": "TU", "T": "TU",
    "We": "WE", "W": "WE",
    "Th": "TH",
    "Fr": "FR", "F": "FR",
    "Sa": "SA",
    "Su": "SU",
}


def _parse_day(d: str) -> str:
    if d in DAY_MAP:
        return DAY_MAP[d]
    if d in ABBREV_MAP:
        return ABBREV_MAP[d]
    raise ValueError(f"Unrecognized day: {d!r}. Use full names (Monday) or abbreviations (Mo, Tu, We, Th, Fr).")


def _parse_time(t: str) -> time:
    h, m = map(int, t.split(":"))
    return time(h, m)


@dataclass
class Class:
    name: str
    title: str
    days: list[str]
    start_time: time
    end_time: time
    location: str


@dataclass
class Schedule:
    quarter_start: date
    quarter_end: date
    classes: list[Class]


def load(path: Path) -> Schedule:
    with open(path) as f:
        data = yaml.safe_load(f)

    quarter_start = date.fromisoformat(data["quarter"]["start"])
    quarter_end = date.fromisoformat(data["quarter"]["end"])

    classes = []
    for cls_data in data.get("classes", []):
        days = [_parse_day(d) for d in cls_data["days"]]
        classes.append(Class(
            name=cls_data["name"],
            title=cls_data.get("title", ""),
            days=days,
            start_time=_parse_time(cls_data["start_time"]),
            end_time=_parse_time(cls_data["end_time"]),
            location=cls_data.get("location", ""),
        ))

    return Schedule(quarter_start=quarter_start, quarter_end=quarter_end, classes=classes)
