# app/analysis.py

from sqlalchemy.orm import Session
from .models import UsageRecord
from datetime import datetime, timedelta

def get_latest_analysis(db: Session):
    """
    Analyze usage records from the past 7 days and generate recommendations.
    """
    week_ago = datetime.utcnow() - timedelta(days=7)
    records = db.query(UsageRecord).filter(UsageRecord.timestamp >= week_ago).all()

    usage_summary = {}
    for rec in records:
        usage_summary.setdefault(rec.tool_name, 0)
        usage_summary[rec.tool_name] += rec.usage_time

    recommendations = []
    for tool, total_time in usage_summary.items():
        if total_time < 10:
            recommendations.append(f"Encourage more use of {tool}.")
        else:
            recommendations.append(f"{tool} usage is sufficient.")

    return {
        "usage_summary": usage_summary,
        "recommendations": recommendations
    }
