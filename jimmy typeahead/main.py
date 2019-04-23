from flask import Flask, render_template, Response, request, jsonify
import json, os
import pandas as pd
import numpy as np
from wtforms import TextField, Form
app = Flask(__name__)

# Global Variables
# Percentile df
percentile_df = None

# Route to home page
@app.route('/', methods=['GET', 'POST'])
def show_home():
	return render_template('search_page.html')

@app.route('/songSearchHandler', methods=['GET', 'POST'])
def songSearchHandler():
	song_id = request.json
	song_id = list(song_id.values())[0]
	print(song_id)
	print(type(song_id))
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	csv_url = os.path.join(SITE_ROOT, "static/", "songs_with_recommendations_and_2d_proj_60k.csv")
	csv_data = pd.read_csv(csv_url)
	if percentile_df is None:
		precompute_percentages(csv_data)
	
	df = get_relevant_points(song_id, csv_data)
	clustering_data = df.to_dict(orient='records')
	clustering_data = json.dumps(clustering_data, indent=2)

	statistics_df, song_name, artist = get_percentiles(song_id)
	statistics_df_t = statistics_df.T
	statistics_df_t['feature'] = statistics_df_t.index
	statistics_df_t.columns = ['value', 'feature']
	print(statistics_df_t)
	statistics_data = statistics_df_t.to_dict(orient = 'records')
	statistics_data = json.dumps(statistics_data, indent = 2)
	return json.dumps(
		{'id': song_id,
		'relevant_points': clustering_data,
		'percentile_data': statistics_data,
		'song_name': song_name,
		'artist': artist})


if __name__ == "__main__":
    app.run(debug=True)
