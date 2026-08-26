import fastf1
from datetime import datetime

today = datetime.now()
year = today.year


# find next gp
next_race = None

while next_race is None:

    schedule = fastf1.get_event_schedule(year)

    for _, race in schedule.iterrows():
        if (
            race["EventDate"].to_pydatetime() >= today
            and "Grand Prix" in race["EventName"]
        ):
            next_race = race
            break

    # no races left this year, move to next year
    if next_race is None:
        year += 1


race_name = next_race["EventName"].replace(
    " Grand Prix",
    " GP"
)

country = next_race["Country"]


# fetch dates
session_dates = [
    next_race["Session1Date"],
    next_race["Session2Date"],
    next_race["Session3Date"],
    next_race["Session4Date"],
    next_race["Session5Date"],
]

session_dates = [
    date.to_pydatetime()
    for date in session_dates
    if date is not None
]

weekend_start = min(session_dates)
weekend_end = max(session_dates)


# flag code - flagcdn
country_codes = {
    "Italy": "it",
    "Spain": "es",
    "Azerbaijan": "az",
    "Singapore": "sg",
    "Japan": "jp",
    "Australia": "au",
    "China": "cn",
    "United States": "us",
    "Mexico": "mx",
    "Brazil": "br",
    "Qatar": "qa",
    "United Arab Emirates": "ae",
    "Monaco": "mc",
    "Canada": "ca",
    "Austria": "at",
    "United Kingdom": "gb",
    "Belgium": "be",
    "Hungary": "hu",
    "Bahrain": "bh",
    "Netherlands": "nl",
}

country_code = country_codes.get(country)

if country_code is None:
    raise ValueError(f"No flag code found for {country}")


# date format
def ordinal(day):
    if 10 <= day % 100 <= 20:
        suffix = "th"
    else:
        suffix = {
            1: "st",
            2: "nd",
            3: "rd"
        }.get(day % 10, "th")

    return f"{day}{suffix}"


month = weekend_start.strftime("%b")
# make Sep → Sept
if month == "Sep":
    month = "Sept"

start = ordinal(weekend_start.day)
end = ordinal(weekend_end.day)
date_text = f"{month} {start}-{end}, {weekend_end.year}"

# html
html = f"""<table>
<tr>

<td valign="middle">
<img src="https://flagcdn.com/w80/{country_code}.png" width="50" style="border-radius:2px;"/>
</td>

<td align="left" valign="middle" style="padding-left:8px;">
<b style="font-size:0.85em;">{race_name}</b><br>
<span style="font-size:0.8em;">{date_text}</span><br>
<img src="https://img.shields.io/badge/F1-{year}-FF1801?style=flat-square&logo=formula1&logoColor=white" height="18"/>
</td>

</tr>
</table>"""


print(html)


# update README
readme_path = "../README.md"

with open(readme_path, "r", encoding="utf-8") as file:
    readme = file.read()

start_marker = "<!--f1-start-->"
end_marker = "<!--f1-end-->"

if start_marker not in readme:
    raise ValueError("F1 start marker not found in README.md")

if end_marker not in readme:
    raise ValueError("F1 end marker not found in README.md")

start = readme.index(start_marker) + len(start_marker)
end = readme.index(end_marker)

new_readme = (
    readme[:start]
    + "\n\n"
    + html
    + "\n\n"
    + readme[end:]
)

with open(readme_path, "w", encoding="utf-8") as file:
    file.write(new_readme)
