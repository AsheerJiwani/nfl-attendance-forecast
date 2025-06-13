# NFL Attendance Forecasting with Exponential Smoothing

A data science project for scraping, cleaning, forecasting, and visualizing 20 years of NFL team attendance, with an interactive gold-and-black Streamlit dashboard.

---

## **Project Structure**

/scraper.py # Script to scrape and clean ESPN attendance data
/forecast.py # Script to train models and generate forecasts
/app.py # Streamlit dashboard
/data/ # Contains raw and processed CSVs
/README.md # This file
/requirements.txt # Python dependencies

---

## **How to Run the Project**

### **1. Set up your environment**

- Install Python 3.8+ (recommended: use a virtual environment)
- Install requirements:

    ```bash
    pip install -r requirements.txt
    ```

### **2. Scrape and Clean the Data**

- Run the scraper script to download and process all years of attendance data:
    ```bash
    python scraper.py
    ```
    - Output: `data/nfl_attendance_2006_2024_final.csv`

### **3. Generate Forecasts**

- Run the forecast/modeling script:
    ```bash
    python forecast.py
    ```
    - Output: `data/nfl_attendance_forecasts_2006_2029_no2020.csv`

### **4. Launch the Dashboard**

- Start the Streamlit dashboard:
    ```bash
    streamlit run app.py
    ```
    - Use the dropdown and toggles to view historical and forecast attendance for any NFL team.

---

## **Design & Technical Notes**

- **Data Source:** [ESPN NFL Attendance](https://www.espn.com/nfl/attendance/_/year/2024)
- **Seasons:** 19 Seasons: 2006–2024 (2005 and before too incomplete, 2020 retained for transparency but not modeled, 2008-2024 data was used for Indianapolis, Las Vegas, Minnesota, and Miami due to incomplete data from data source)
- **Metrics:** Home average, road average, overall average attendance per team per year
- **Model:** Exponential Smoothing with trend (`statsmodels`), COVID-affected 2020 excluded from modeling but retained for reference
- **Forecast Horizon:** 2025–2029 (5 years out)
- **Team Name Handling:** All historical relocations/renames (LA Rams/Chargers, etc.) unified for continuity

---

## Additional Variables for Enhanced Forecasting

If future versions of this project aimed to further improve NFL attendance forecasting, the following variables could be integrated into the modeling pipeline:

- **Team Performance**  
  Win-loss record, playoff runs, and overall franchise momentum have strong impacts on fan interest.

- **Star Player Presence**  
  Attendance often spikes for games featuring star players (home or away), or for major player debuts/returns.

- **Game Schedule Features**
  - **Day of the Week:** Sunday, Monday Night Football (MNF), Thursday Night Football (TNF), Saturday games, etc.
  - **Time of Day:** Afternoon vs. evening kickoffs.
  - **Holiday Games:** Thanksgiving, Christmas, New Year’s.

- **Opponent Quality**
  - **Rivalry Games:** Division rivals and historic matchups typically draw higher attendance.
  - **Visiting Team Draw:** Teams with national/international fanbases (e.g., Cowboys, Packers) boost attendance on the road.

- **Weather**
  - Outdoor stadiums may see attendance dips during poor weather forecasts (rain, snow, cold).

- **Promotions & Giveaways**
  - Special events, fan appreciation days, or giveaways can increase single-game attendance.

- **Stadium Factors**
  - **Stadium Capacity:** Renovations or temporary seating changes.
  - **Location/Access:** Changes in public transit, parking, or stadium moves.

- **Economic Factors**
  - Local unemployment rates, ticket prices, and city population trends.

- **COVID-19 or Health Policies**
  - Attendance restrictions, mask/vaccine mandates, etc.

- **Television Broadcast Factors**
  - Nationally televised games (MNF/SNF/TNF) may affect in-person attendance (sometimes positively, sometimes negatively).

- **Local Competing Events**
  - Major concerts, local festivals, or other sporting events scheduled at the same time.

**Incorporating these features could enable more granular, game-level and team-level forecasting, making the model even more predictive and useful for NFL franchises or analysts.**

- **How to Incorporate**
  - Many of these features could be collected by scraping official NFL schedules, leveraging public APIs (such as weather or economic data), and tracking team and player performance from reputable sports databases. Feature engineering would also involve merging game-level attendance with these variables to enable fine-grained, context-aware predictions.

---

## **Gold/Black Dashboard Theme**

- All charts and text use a gold (`#FFD700`), white, and black color scheme matching CEREBRO website and logo colors
- The "CEREBRO" brand is displayed in the top right.

---

## **Daily Log**

- **Day 1:** Researched ESPN attendance page structure and planned scraper logic.
- **Day 2:** Built and tested web scraping code; handled inconsistent ESPN HTML and extracted all teams’ attendance data for 2006–2024.
- **Day 3:** Cleaned dataset, handled team name changes and missing years; analyzed early years for completeness.
- **Day 4:** Developed forecasting code (Exponential Smoothing), filtered out COVID-2020 for modeling, checked forecasts for plausibility, and validated confidence intervals.
- **Day 5:** Built the Streamlit dashboard with gold/black/white theming; tested with several teams and refined chart layout and notes. Final testing, cleaned code, added README and requirements.txt, and packaged project for delivery.

---

## **How to Use or Modify**

- To re-run forecasts with new data, update the ESPN years in `scraper.py` and rerun steps 2–4.
- To change dashboard colors or layout, modify the CSS and Plotly code in `app.py`.

---

## **Requirements**

- Python 3.8 or higher
- `pandas`, `beautifulsoup4`, `requests`, `statsmodels`, `plotly`, `streamlit`, `tqdm`
  - All included in `requirements.txt`


