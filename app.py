import streamlit as st
import pandas as pd
import plotly.graph_objs as go

st.set_page_config(page_title="NFL Attendance Forecasts", layout="wide")

# Custom CSS for black/gold/white theme
custom_css = """
<style>
body { background-color: #000 !important; }
section.main { background-color: #000 !important; }
h1, .title { color: #FFD700 !important; font-family: 'Roboto', sans-serif; display: inline; }
.cerebro {
    color: #000;
    background: #FFD700;
    font-weight: bold;
    font-size: 2.1rem;
    font-family: 'Roboto', sans-serif;
    letter-spacing: 0.09em;
    border-radius: 7px;
    padding: 0.2rem 1.1rem;
    margin-left: 2.5rem;
    vertical-align: middle;
    display: inline;
}
.stRadio > div, .stSelectbox > div, label, span, .stMarkdown { color: #FFF !important; font-family: 'Roboto', sans-serif; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Inline title, cerebro, and logo using columns
col1, col2, col3 = st.columns([0.40, 0.17, 0.15])

with col1:
    st.markdown("<h1 class='title'>NFL Team Attendance: 2006–2029</h1>", unsafe_allow_html=True)
with col2:
    st.markdown("<span class='cerebro'>CEREBRO</span>", unsafe_allow_html=True)
with col3:
    st.image("cerebro_logo.png", width=70)  # Change path/width as you need


st.markdown(
    """
    <span style="color:#FFF">
    <b>Explore 20 years of historical and projected NFL team attendance with interactive gold-on-black visuals.</b>
    </span>
    """,
    unsafe_allow_html=True,
)

# Load data
DATA_FILE = "data/nfl_attendance_forecasts_2006_2029_no2020.csv"
df = pd.read_csv(DATA_FILE)

# Team & metric selectors
teams = sorted(df['team'].unique())
team = st.selectbox("Select a team", teams)
metric_labels = {"home_avg": "Home Attendance", "road_avg": "Road Attendance", "overall_avg": "Overall Attendance"}
metric = st.radio("Attendance type", list(metric_labels.keys()), format_func=lambda x: metric_labels[x])

# Filter and split data
team_metric_df = df[(df['team'] == team) & (df['metric'] == metric)].sort_values('season')
hist = team_metric_df[team_metric_df['type'] == 'historical']
fcast = team_metric_df[team_metric_df['type'] == 'forecast']

# Plotly chart, larger and styled
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=hist['season'], y=hist['attendance'],
    mode='lines+markers+text',
    name='Historical',
    line=dict(color='#FFD700', width=3),
    marker=dict(size=8, color='#FFD700'),
    text=None,  # Remove data labels for clarity; re-enable if you want
    hoverlabel=dict(font_color="white", bgcolor="black")
))
fig.add_trace(go.Scatter(
    x=fcast['season'], y=fcast['attendance'],
    mode='lines+markers+text',
    name='Forecast',
    line=dict(color='#FFF', width=3, dash='dash'),
    marker=dict(size=8, color='#FFF', symbol='diamond'),
    text=None,
    hoverlabel=dict(font_color="white", bgcolor="black")
))
if 'lower' in fcast and 'upper' in fcast:
    fig.add_trace(go.Scatter(
        x=list(fcast['season']) + list(fcast['season'])[::-1],
        y=list(fcast['upper']) + list(fcast['lower'])[::-1],
        fill='toself',
        fillcolor='rgba(255,215,0,0.18)',  # faint gold
        line=dict(color='rgba(255,125,255,130)'),
        hoverinfo="skip",
        showlegend=True,
        name="Forecast Interval"
    ))

fig.update_layout(
    plot_bgcolor='#000',
    paper_bgcolor='#000',
    font=dict(color='#FFD700', family='Roboto'),
    title=f"<b style='color:#FFD700'>{team}</b> – <span style='color:white'>{metric_labels[metric]}</span> <span style='color:#FFD700'>(2006–2029)</span>",
    xaxis=dict(
        title="Season", color="#FFD700", tickfont=dict(color="#FFD700"), showgrid=False, linecolor="#FFD700", tickformat='d'
    ),
    yaxis=dict(
        title="Attendance", color="#FFD700", tickfont=dict(color="#FFD700"), showgrid=False, linecolor="#FFD700"
    ),
    legend=dict(
        x=1, y=.7, xanchor='right', yanchor='top',
        font=dict(color='#FFD700', size=20), bgcolor='rgba(0,0,0,0)'
    ),
    hovermode="x unified",
    height=500,  # Larger height
    width=1100   # Larger width
)
st.plotly_chart(fig, use_container_width=True)

# Proper notes with gold and white, always visible
st.markdown(
    """
    <div style="margin-top: 1rem; padding: 1rem; background-color: #111; border-radius: 9px;">
    <span style="color:#FFD700">
    <b>Notes:</b>
    </span>
    <span style="color:#FFF">
    <ul>
      <li>2020 is shown as missing/NaN for most teams due to COVID-19.</li>
      <li>Forecasts (2025–2029) are based on exponential smoothing models, excluding 2020 as an outlier.</li>
      <li><span style="color:#FFD700">Gold lines = historical, white lines = forecast, shaded band = model confidence.</span></li>
    </ul>
    </span>
    </div>
    """,
    unsafe_allow_html=True,
)
