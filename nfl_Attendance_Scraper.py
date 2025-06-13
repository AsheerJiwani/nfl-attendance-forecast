import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

# Team code to canonical name mapping (expand as needed)
TEAM_CODE_MAP = {
    "lar": "Los Angeles Rams",
    "lac": "Los Angeles Chargers",
    "lv": "Las Vegas Raiders",
    "oak": "Oakland Raiders",
    "sd": "San Diego Chargers",
    "stl": "St. Louis Rams",
    # Add others as needed
}

def get_team_code(td):
    """Extract team code from the ESPN href or fallback to text."""
    a = td.find('a')
    if a and 'href' in a.attrs:
        # Example: .../name/lar/los-angeles-rams
        parts = a['href'].split('/')
        try:
            idx = parts.index('name')
            code = parts[idx + 1]
            return code
        except (ValueError, IndexError):
            pass
    # Fallback: Use the cell's text (stripped)
    return td.get_text(strip=True)

def get_team_name(code, fallback):
    """Return canonical name if code is in map, else fallback to text."""
    return TEAM_CODE_MAP.get(code, fallback)

def scrape_and_extract(year):
    url = f'https://www.espn.com/nfl/attendance/_/year/{year}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    data = []
    for row in rows[1:]:
        tds = row.find_all('td')
        # ESPN tables may have header or summary rows—skip these
        if not tds or len(tds) < 11:
            continue
        # Get team code and name
        team_code = get_team_code(tds[1])
        team_text = tds[1].get_text(strip=True)
        team = get_team_name(team_code, team_text)
        # Skip header/total/league rows and fake attendance rows
        if team.upper() in ['TEAM', 'TOTAL', 'LEAGUE AVERAGE'] or 'ATTENDANCE' in team.upper():
            continue
        # Exclude incomplete teams for 2006/2007
        if year in [2006, 2007] and team in ["Indianapolis", "Las Vegas Raiders", "Miami", "Minnesota"]:
            continue
        # Read and parse stats
        try:
            home_avg = float(tds[4].get_text().replace(',', ''))
        except ValueError:
            home_avg = None
        try:
            road_avg = float(tds[7].get_text().replace(',', ''))
        except ValueError:
            road_avg = None
        try:
            overall_avg = float(tds[10].get_text().replace(',', ''))
        except ValueError:
            overall_avg = None
        data.append({
            "team": team,
            "season": year,
            "home_avg": home_avg,
            "road_avg": road_avg,
            "overall_avg": overall_avg
        })
    return pd.DataFrame(data)

# Scrape and combine all years
all_years = []
for year in range(2006, 2025):
    print(f"Scraping {year}...")
    df = scrape_and_extract(year)
    all_years.append(df)
    time.sleep(1)

attendance_df = pd.concat(all_years, ignore_index=True)

# Final deduplication (shouldn't be needed but is safe)
attendance_df = attendance_df.drop_duplicates(subset=['team', 'season'])

# Save cleaned data
attendance_df.to_csv("data/nfl_attendance_2006_2024_final.csv", index=False)

# Show summary for sanity check
print(attendance_df['team'].value_counts())
print(attendance_df.head(10))

