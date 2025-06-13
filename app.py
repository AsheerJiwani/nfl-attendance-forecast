import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# --- PAGE & GLOBAL STYLE ---
st.set_page_config(page_title="NFL Attendance Forecasts", page_icon=":football:", layout="wide")

# --- CUSTOM CSS: Full Professional Styling ---
st.markdown("""
<link href="https://fonts.googleapis.com/css?family=Montserrat:700,400|Roboto+Slab:400,700&display=swap" rel="stylesheet">
<style>
html, body, .stApp {
    background-color: #0A0A0A !important;
    color: #FFD700 !important;
    font-family: 'Montserrat', 'Roboto Slab', sans-serif !important;
}
.stApp {
    padding-top: 0 !important;
}
.header-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: linear-gradient(90deg, #181818 70%, #FFD700 250%);
    padding: 24px 32px 18px 32px;
    margin-bottom: 20px;
    border-bottom: 2px solid #FFD700;
    box-shadow: 0 4px 16px 0 rgba(0,0,0,0.13);
}
h1, .headline {
    color: #FFD700 !important;
    font-family: 'Montserrat', sans-serif;
    font-size: 2.7rem !important;
    letter-spacing: 0.025em;
    margin-bottom: 0;
    margin-top: 0.1em;
    font-weight: 700;
    display: inline-block;
}
.cerebros-tag {
    color: #181818;
    background: #FFD700;
    font-weight: bold;
    font-size: 2.1rem;
    font-family: 'Montserrat', sans-serif;
    letter-spacing: 0.09em;
    border-radius: 12px;
    padding: 0.18em 1.4em;
    vertical-align: middle;
    margin-left: 2rem;
    margin-right: 1rem;
    box-shadow: 0 3px 8px 0 rgba(255,215,0,0.10);
    display: inline-block;
}
.cerebros-logo {
    height: 58px;
    margin-left: 0.9em;
    margin-bottom: -12px;
    vertical-align: middle;
}
.stSelectbox, .stRadio {
    background: #181818 !important;
    color: #FFD700 !important;
    border-radius: 10px !important;
    padding: 0.6em 1.1em !important;
    margin-bottom: 1.2em !important;
}
.stButton>button {
    background-color: #FFD700 !important;
    color: #111 !important;
    font-weight: bold !important;
    border-radius: 8px !important;
    font-size: 1.08em !important;
    transition: background 0.18s;
}
.stButton>button:hover {
    background-color: #ffe066 !important;
    color: #181818 !important;
}
hr {
    border: 0;
    border-top: 1.5px solid #FFD700;
    margin: 24px 0 36px 0;
}
.card {
    background: #181818;
    border-radius: 18px;
    padding: 2.5em 2.8em 2.2em 2.8em;
    margin-bottom: 1.5em;
    box-shadow: 0 2px 15px 0 rgba(255,215,0,0.07), 0 1.5px 16px 0 rgba(0,0,0,0.17);
}
.section-title {
    color: #FFD700;
    font-family: 'Montserrat', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    margin-bottom: 10px;
    letter-spacing: 0.03em;
}
.stMarkdown {
    color: #FFF !important;
    font-family: 'Montserrat', 'Roboto Slab', sans-serif;
}
footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background: #181818;
    color: #FFD700;
    text-align: center;
    padding: 9px;
    font-size: 1em;
    letter-spacing: 0.05em;
    z-index: 10000;
}
a, a:visited { color: #FFD700; text-decoration: underline; }
a:hover { color: #fff38e; }
</style>
""", unsafe_allow_html=True)

# --- HEADER BAR ---
st.markdown(
    """
    <div class="header-bar">
        <div style="display: flex; align-items: center;">
            <h1 class="headline" style="margin-bottom:0;">NFL Team Attendance: 2006–2029</h1>
        </div>
        <div style="display: flex; align-items: center;">
            <span class="cerebros-tag">CEREBROS</span>
            <img src="cerebros_logo.png" class="cerebros-logo">
        </div>
    </div>
    """, unsafe_allow_html=True
)

# --- MAIN CARD: Intro ---
st.markdown('<hr>', unsafe_allow_html=True)
with st.container():
    st.markdown(
        """
        <div class="card">
            <div class="section-title">Explore Attendance</div>
            <span style="color:#FFF; font-size:1.11em;">
                View 20 years of historical and projected NFL team attendance in an interactive, visually-rich dashboard.<br>
                Select a team and metric below to see dynamic gold-on-black visualizations and five-year forecasts.
            </span>
        </div>
        """, unsafe_allow_html=True
    )

# --- LOAD DATA (ADAPT PATH AS NEEDED) ---
df = pd.read_csv("data/nfl_attendance_forecasts_2006_2029_no2020.csv")

metric_labels = {"home_avg": "Home Attendance", "road_avg": "Road Attendance", "overall_avg": "Overall Attendance"}

# --- CARD: Team & Metric Selection ---
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Team & Metric Selection</div>', unsafe_allow_html=True)
    teams = sorted(df['team'].unique())
    team = st.selectbox("Select a team", teams, help="Choose an NFL team to view its attendance data.")
    metric = st.radio("Attendance type", list(metric_labels.keys()), format_func=lambda x: metric_labels[x], help="Select the attendance metric.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- DATA FILTERING FOR CHART ---
team_metric_df = df[(df['team'] == team) & (df['metric'] == metric)].sort_values('season')
hist = team_metric_df[team_metric_df['type'] == 'historical']
fcast = team_metric_df[team_metric_df['type'] == 'forecast']

# --- CHART SECTION ---
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Attendance Trends & Forecast</div>', unsafe_allow_html=True)
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=hist['season'], y=hist['attendance'],
        mode='lines+markers',
        name='Historical',
        line=dict(color='#FFD700', width=3, shape='spline'),
        marker=dict(size=7, color='#FFD700'),
        hoverlabel=dict(font_color="white", bgcolor="black")
    ))
    fig.add_trace(go.Scatter(
        x=fcast['season'], y=fcast['attendance'],
        mode='lines+markers',
        name='Forecast',
        line=dict(color='#FFF', width=3, dash='dash', shape='spline'),
        marker=dict(size=7, color='#FFF', symbol='diamond'),
        hoverlabel=dict(font_color="white", bgcolor="black")
    ))
    # Confidence interval
    if 'lower' in fcast and 'upper' in fcast:
        fig.add_trace(go.Scatter(
            x=list(fcast['season']) + list(fcast['season'])[::-1],
            y=list(fcast['upper']) + list(fcast['lower'])[::-1],
            fill='toself',
            fillcolor='rgba(255,215,0,0.18)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=True,
            name="Forecast Interval"
        ))

    fig.update_layout(
        plot_bgcolor='#000',
        paper_bgcolor='#000',
        font=dict(color='#FFD700', family='Montserrat'),
        title=f"<b style='color:#FFD700'>{team}</b> – <span style='color:white'>{metric_labels[metric]}</span> <span style='color:#FFD700'>(2006–2029)</span>",
        xaxis=dict(
            title="Season", color="#FFD700", tickfont=dict(color="#FFD700"), showgrid=False, linecolor="#FFD700", tickformat='d'
        ),
        yaxis=dict(
            title="Attendance", color="#FFD700", tickfont=dict(color="#FFD700"), showgrid=False, linecolor="#FFD700"
        ),
        legend=dict(
            x=1, y=1.04, xanchor='right', yanchor='bottom',
            font=dict(color='#FFD700', size=14), bgcolor='rgba(0,0,0,0)'
        ),
        hovermode="x unified",
        height=800,
        width=None,
        margin=dict(l=30, r=30, t=75, b=30)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- NOTES/EXPLANATION CARD ---
st.markdown(
    """
    <div class="card" style="background:#111; margin-top:1.5em;">
    <span class="section-title" style="color:#FFD700;">Notes</span>
    <span style="color:#FFF;">
    <ul>
      <li><b>2020</b> is shown as missing/NaN for most teams due to COVID-19 restrictions.</li>
      <li><b>Forecasts (2025–2029)</b> use exponential smoothing models, omitting 2020 as an outlier.</li>
      <li><span style="color:#FFD700"><b>Gold lines</b> = historical • <b>White lines</b> = forecast • <b>Gold band</b> = model confidence interval.</span></li>
    </ul>
    </span>
    </div>
    """, unsafe_allow_html=True
)

# --- FOOTER ---
st.markdown(
    """<footer>© 2024 <b>CEREBROS</b> • NFL Attendance Forecast Dashboard</footer>""",
    unsafe_allow_html=True
)
