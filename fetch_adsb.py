import requests
import json
from datetime import datetime

def fetch_aircraft_data():
    url = "https://opensky-network.org/api/states/all"
    
    print("[*] Fetching live ADS-B data from OpenSky Network...")
    response = requests.get(url, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        aircraft_list = []
        
        for state in data['states'][:50]:  # Get first 50 aircraft
            aircraft = {
                'icao24': state[0],
                'callsign': state[1],
                'country': state[2],
                'longitude': state[5],
                'latitude': state[6],
                'altitude': state[7],
                'velocity': state[9],
                'timestamp': datetime.now().isoformat()
            }
            aircraft_list.append(aircraft)
        
        with open('aircraft_data.json', 'w') as f:
            json.dump(aircraft_list, f, indent=4)
        
        print(f"[+] Successfully captured {len(aircraft_list)} aircraft")
        print(f"[+] Data saved to aircraft_data.json")
        return aircraft_list
    else:
        print(f"[-] Failed to fetch data: {response.status_code}")

if __name__ == "__main__":
    fetch_aircraft_data()