from __future__ import annotations

from datetime import date, datetime, time, timedelta

from icalendar import Calendar, Event

from .parser import Class, Schedule

_DAY_ORDER = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]


def _first_occurrence(quarter_start: date, days: list[str]) -> date:
    """Return the first date >= quarter_start that falls on one of the given weekdays."""
    start_wd = quarter_start.weekday()  # Monday=0 … Sunday=6
    min_delta = min((_DAY_ORDER.index(d) - start_wd) % 7 for d in days)
    return quarter_start + timedelta(days=min_delta)


def _build_event(cls: Class, schedule: Schedule) -> Event:
    event = Event()

    summary = f"{cls.name}: {cls.title}" if cls.title else cls.name
    event.add("summary", summary)

    first_day = _first_occurrence(schedule.quarter_start, cls.days)
    event.add("dtstart", datetime.combine(first_day, cls.start_time))
    event.add("dtend", datetime.combine(first_day, cls.end_time))

    if cls.location:
        event.add("location", cls.location)

    until = datetime.combine(schedule.quarter_end, time(23, 59, 59))
    event.add("rrule", {
        "FREQ": "WEEKLY",
        "BYDAY": cls.days,
        "UNTIL": until,
    })

    return event


def generate(schedule: Schedule) -> Calendar:
    cal = Calendar()
    cal.add("prodid", "-//ucsd-cal//EN")
    cal.add("version", "2.0")
    cal.add("x-wr-calname", "UCSD Schedule")

    for cls in schedule.classes:
        cal.add_component(_build_event(cls, schedule))

    return cal
