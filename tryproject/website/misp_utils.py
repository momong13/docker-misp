import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from pymisp import PyMISP
from flask import current_app

MISP_URL = "https://192.168.100.76"
MISP_KEY = "vKw9eWvfCil5HcSt0Q5nsJs0fOpmTCt5modKEsUp"
VERIFY_CERT = False

def fetch_recent_threats(limit=10):
    try:
        misp = PyMISP(MISP_URL, MISP_KEY, VERIFY_CERT)

        # Fetch events without filtering by 'last' to check for all available events
        events = misp.search(controller='events', limit=limit)
        print(events)  # Debugging raw response

        # Check if events were found
        if not events:
            print("⚠️ No threats found in MISP response.")
            return []

        threats = []
        for event in events:  # Iterate directly over the list of events
            event_data = event['Event']  # Access the 'Event' dictionary
            threats.append({
                'id': event_data['id'],
                'info': event_data['info'],
                'threat_level': int(event_data['threat_level_id']),
                'date': event_data['date']
            })

        print(f"Fetched threats: {threats}")  # Debugging output
        return threats

    except Exception as e:
        print(f"❌ Error connecting to MISP: {e}")
        return []

def calculate_risk(impact, likelihood):
    risk_matrix = {
        (1, 1): 'Low', (1, 2): 'Low', (1, 3): 'Moderate',
        (2, 1): 'Low', (2, 2): 'Moderate', (2, 3): 'High',
        (3, 1): 'Moderate', (3, 2): 'High', (3, 3): 'Critical'
    }
    return risk_matrix.get((impact, likelihood), 'Unknown')
