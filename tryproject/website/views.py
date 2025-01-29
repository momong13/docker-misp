from flask import Blueprint, render_template, request, jsonify
from .models import Risk, Asset
from .misp_utils import fetch_recent_threats, calculate_risk
import plotly.graph_objs as go
import plotly.utils
import json
import numpy as np
from bson.json_util import dumps

main = Blueprint('main', __name__)

@main.route('/')
def index():
    risks = Risk.get_all()
    return render_template('index.html', risks=risks)

@main.route('/add_risk', methods=['POST'])
def add_risk():
    data = request.json
    risk_id = Risk.create(data)
    return jsonify({"message": "Risk added successfully", "id": str(risk_id.inserted_id)})

@main.route('/fetch_risks', methods=['GET'])
def fetch_risks():
    risks = Risk.get_all()
    return dumps(risks)  # Convert MongoDB data to JSON format

@main.route('/add_asset', methods=['POST'])
def add_asset():
    data = request.json
    asset_id = Asset.create(data)
    return jsonify({"message": "Asset added successfully", "id": str(asset_id.inserted_id)})

@main.route('/fetch_assets')
def fetch_assets():
    assets = Asset.get_all()
    return dumps(assets)

@main.route('/recent_threats')
def recent_threats():
    threats = fetch_recent_threats(limit=10)
    
    for threat in threats:
        threat['threat_actor'] = "Cyber Criminal"
        threat['threat_scenario'] = f"Exploited {threat['info']}"
        threat['risk_impact_area'] = "Financial Loss"
        threat['likelihood'] = "Moderate" if threat["threat_level"] == 2 else "High"
        threat['risk_level'] = "Moderate" if threat["threat_level"] == 2 else "High"
    
    return render_template('recent_threats.html', threats=threats)

@main.route('/assess_risk', methods=['POST'])
def assess_risk():
    data = request.json
    impact = int(data['impact'])
    likelihood = int(data['likelihood'])

    risk_level = calculate_risk(impact, likelihood)

    risk_data = {
        'asset': data['asset'],
        'threat_actor': data['threat_actor'],
        'threat_scenario': data['threat_scenario'],
        'risk_impact_area': data['risk_impact_area'],
        'impact': impact,
        'likelihood': likelihood,
        'risk_level': risk_level
    }

    Risk.create(risk_data)

    return jsonify({'risk_level': risk_level})

@main.route('/visualize_risks')
def visualize_risks():
    risks = Risk.get_all()
    
    if not risks:
        return jsonify({'data': [], 'layout': {}})
    
    impact_labels = ['Low', 'Moderate', 'High']
    likelihood_labels = ['Low', 'Moderate', 'High']
    
    risk_matrix = np.zeros((3, 3))
    
    for risk in risks:
        impact = int(risk['impact']) - 1
        likelihood = int(risk['likelihood']) - 1
        risk_matrix[impact, likelihood] += 1
    
    fig = go.Figure(data=go.Heatmap(
        z=risk_matrix,
        x=likelihood_labels,
        y=impact_labels[::-1],
        colorscale='YlOrRd',
        hoverongaps=False
    ))
    
    fig.update_layout(
        title='Risk Matrix (Octave Allegro)',
        xaxis_title='Likelihood',
        yaxis_title='Impact'
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
