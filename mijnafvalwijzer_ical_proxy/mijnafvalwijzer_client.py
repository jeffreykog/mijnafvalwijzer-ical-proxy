from datetime import date, datetime
from typing import List

import aiohttp
from bs4 import BeautifulSoup

from mijnafvalwijzer_ical_proxy.const import DATE_RE, MONTHS


class PickupMoment:

    waste_type: str
    pickup_date: date
    description: str

    def __init__(self, waste_type: str, pickup_date: date, description: str):
        self.waste_type = waste_type
        self.pickup_date = pickup_date
        self.description = description


async def fetch_pickup_moments(postal_code: str, number: str, suffix: str = "") -> List[PickupMoment]:
    result = []

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.mijnafvalwijzer.nl/nl/{postal_code}/{number}/{suffix}") as response:
            parser = BeautifulSoup(await response.text(), "html.parser")

            for item in parser.find_all("a", "wasteInfoIcon textDecorationNone"):
                waste_type = item["href"].replace("#", "").replace("waste-", "")
                if waste_type == "" or waste_type == "javascript:void(0);":
                    if item.p.has_attr("class"):
                        waste_type = item.p["class"][0]

                description = item.find("span", {"class": "afvaldescr"}).text.replace("\\,", ",")
                print(description)

                result.append(PickupMoment(
                    waste_type=waste_type,
                    pickup_date=_convert_date(item.find("span", {"class": "span-line-break"}).text),
                    description=item.find("span", {"class": "afvaldescr"}).text.replace("\\,", ","),
                ))

    return result


def _convert_date(date_input: str) -> date:
    pattern = DATE_RE.match(date_input)
    return date(datetime.now().year, MONTHS.get(pattern.group(3), 0), int(pattern.group(2)))
