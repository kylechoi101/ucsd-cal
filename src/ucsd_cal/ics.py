from __future__ import annotations

from datetime import date, datetime, time, timedelta

from .parser import Class, Schedule

_DAY_ORDER = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]


def _first_occurrence(quarter_start: date, days: list) -> date:
    start_wd = quarter_start.weekday()  # Monday=0
    min_delta = min((_DAY_ORDER.index(d) - start_wd) % 7 for d in days)
    return quarter_start + timedelta(days=min_delta)


def _fmt_dt(dt: datetime) -> str:
    return dt.strftime("%Y%m%dT%H%M%S")


def _fmt_date_until(d: date) -> str:
    return d.strftime("%Y%m%dT235959")


def _build_vevent(cls: Class, schedule: Schedule) -> str:
    summary = f"{cls.name}: {cls.title}" if cls.title else cls.name
    first_day = _first_occurrence(schedule.quarter_start, cls.days)
    dtstart = _fmt_dt(datetime.combine(first_day, cls.start_time))
    dtend = _fmt_dt(datetime.combine(first_day, cls.end_time))
    byday = ",".join(cls.days)
    until = _fmt_date_until(schedule.quarter_end)
    lines = [
        "BEGIN:VEVENT",
        f"SUMMARY:{summary}",
        f"DTSTART:{dtstart}",
        f"DTEND:{dtend}",
        f"RRULE:FREQ=WEEKLY;UNTIL={until};BYDAY={byday}",
    ]
    if cls.location:
        lines.append(f"LOCATION:{cls.location}")
    lines.append("END:VEVENT")
    return "\r\n".join(lines)


def generate(schedule: Schedule) -> str:
    parts = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//ucsd-cal//EN",
        "X-WR-CALNAME:UCSD Schedule",
    ]
    for cls in schedule.classes:
        parts.append(_build_vevent(cls, schedule))
    parts.append("END:VCALENDAR")
    return "\r\n".join(parts) + "\r\n"
