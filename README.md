# ucsd-cal

A command-line tool that converts a UCSD class schedule into an ICS file you can import directly into Google Calendar (or any calendar app that supports the ICS format). Define your classes once in a simple YAML file and generate a recurring-event calendar in seconds.

## Installation

```bash
uv add "git+https://github.com/kylechoi101/ucsd-cal.git"
```

## Usage

### 1. Create a schedule file

Generate a template to fill in:

```bash
ucsd-cal template > schedule.yaml
```

Edit `schedule.yaml` to match your courses:

```yaml
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
```

Days can be written as full names (`Monday`) or two-letter abbreviations (`Mo`, `Tu`, `We`, `Th`, `Fr`).

### 2. Generate the ICS file

```bash
ucsd-cal generate schedule.yaml -o calendar.ics
```

### 3. Import into Google Calendar

1. Open [Google Calendar](https://calendar.google.com)
2. Go to **Settings** → **Import & Export**
3. Click **Import**, select `calendar.ics`, and choose a calendar
4. Click **Import**

Your classes will appear as weekly recurring events for the entire quarter.
