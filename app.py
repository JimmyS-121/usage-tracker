from flask import Flask, jsonify, request
from utils import fetch_usage_data, fetch_survey_data, dynamic_join, analyze_usage, generate_usage_chart

app = Flask(__name__)

@app.route("/api/data")
def get_combined_data():
    usage_df = fetch_usage_data()
    survey_df = fetch_survey_data()
    join_key = request.args.get("join_key", "user")
    join_type = request.args.get("join_type", "inner")
    combined_df = dynamic_join(usage_df, survey_df, join_key=join_key, how=join_type)
    return jsonify(combined_df.to_dict(orient="records"))

@app.route("/api/analysis")
def get_analysis():
    usage_df = fetch_usage_data()
    survey_df = fetch_survey_data()
    join_key = request.args.get("join_key", "user")
    join_type = request.args.get("join_type", "inner")
    combined_df = dynamic_join(usage_df, survey_df, join_key=join_key, how=join_type)
    analysis = analyze_usage(combined_df)
    return jsonify(analysis)

@app.route("/api/chart")
def get_chart():
    usage_df = fetch_usage_data()
    survey_df = fetch_survey_data()
    join_key = request.args.get("join_key", "user")
    join_type = request.args.get("join_type", "inner")
    chart_type = request.args.get("chart_type", "bar")
    combined_df = dynamic_join(usage_df, survey_df, join_key=join_key, how=join_type)
    chart_b64 = generate_usage_chart(combined_df, chart_type=chart_type)
    return jsonify({"chart_image_base64": chart_b64, "chart_type": chart_type})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
