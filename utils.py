import pandas as pd
import plotly.express as px
import base64

def fetch_usage_data():
    data = [
        {"user": "alice", "tool": "ChatGPT", "timestamp": "2025-07-01T10:00:00"},
        {"user": "bob", "tool": "DALL-E", "timestamp": "2025-07-01T11:00:00"},
        {"user": "alice", "tool": "ChatGPT", "timestamp": "2025-07-02T09:00:00"},
        {"user": "charlie", "tool": "ChatGPT", "timestamp": "2025-07-02T14:00:00"},
    ]
    return pd.DataFrame(data)

def fetch_survey_data():
    data = [
        {"user": "alice", "satisfaction": 4, "comments": "Very helpful"},
        {"user": "bob", "satisfaction": 3, "comments": "Good but slow"},
        {"user": "charlie", "satisfaction": 5, "comments": "Excellent tool"},
    ]
    return pd.DataFrame(data)

def dynamic_join(usage_df, survey_df, join_key="user", how="inner"):
    return pd.merge(usage_df, survey_df, on=join_key, how=how)

def analyze_usage(df):
    usage_counts = df['tool'].value_counts().to_dict()
    avg_satisfaction = df['satisfaction'].mean()
    insights = []

    for tool, count in usage_counts.items():
        insights.append(f"{tool} used {count} times.")

    insights.append(f"Average satisfaction score: {avg_satisfaction:.2f}")

    return {
        "usage_counts": usage_counts,
        "average_satisfaction": avg_satisfaction,
        "insights": insights
    }

def generate_usage_chart(df, chart_type="bar"):
    usage_counts = df['tool'].value_counts().reset_index()
    usage_counts.columns = ['tool', 'count']

    if chart_type == "bar":
        fig = px.bar(usage_counts, x='tool', y='count', title="AI Tool Usage Count")
    elif chart_type == "pie":
        fig = px.pie(usage_counts, names='tool', values='count', title="AI Tool Usage Distribution")
    elif chart_type == "line":
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        daily_usage = df.groupby(['date', 'tool']).size().reset_index(name='count')
        fig = px.line(daily_usage, x='date', y='count', color='tool', title="Daily AI Tool Usage")
    else:
        fig = px.bar(usage_counts, x='tool', y='count', title="AI Tool Usage Count")

    img_bytes = fig.to_image(format="png")
    img_b64 = base64.b64encode(img_bytes).decode('utf-8')
    return img_b64
