from datetime import timedelta, datetime

from icalendar import Calendar, Alarm, Event

from mijnafvalwijzer_ical_proxy.mijnafvalwijzer_client import fetch_pickup_moments


async def generate_ical(postal_code: str, number: str, suffix: str = ""):
    moments = await fetch_pickup_moments(postal_code, number, suffix)

    cal = Calendar()
    cal.add("prodid", "-//mijnafvalwijzer-ical-proxy//NL")
    cal.add("version", "2.0")
    cal.add("name", "Afvalkalender")
    cal.add("x-wr-calname", "Afvalkalender")
    cal.add("x-wr-timezone", "Europe/Amsterdam")

    alarm = Alarm()
    alarm.add("action", "DISPLAY")
    alarm.add("trigger", value=timedelta(hours=-5))

    now = datetime.now()

    for moment in moments:
        event = Event()
        event.add("uid", f"{moment.pickup_date.isoformat()}-{moment.waste_type}")
        event.add("dtstamp", now)
        event.add("dtstart", moment.pickup_date)
        event.add("dtend", moment.pickup_date + timedelta(days=1))
        event.add("summary", f"Afvalinzameling - {moment.description}")
        event.add("description", moment.description)
        event.add_component(alarm)

        cal.add_component(event)

    return cal.to_ical()
