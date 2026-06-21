import json
import time
from datetime import datetime
from fetch_adsb import fetch_aircraft_data

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance in km between two lat/lon points"""
    from math import radians, sin, cos, sqrt, atan2
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def monitor(snapshots=3, interval_seconds=30):
    """
    Capture multiple snapshots over time and detect 'teleporting' aircraft -
    a classic ADS-B spoofing signature where an aircraft's position jumps
    further than physically possible given its reported velocity.
    """
    print("="*50)
    print("ADS-B CONTINUOUS ANOMALY MONITOR")
    print("="*50)
    print(f"[*] Taking {snapshots} snapshots, {interval_seconds}s apart\n")

    history = {}  # icao24 -> list of (timestamp, lat, lon, velocity)

    for i in range(snapshots):
        print(f"[*] Snapshot {i+1}/{snapshots}...")
        aircraft_list = fetch_aircraft_data()

        for a in aircraft_list:
            if a['latitude'] and a['longitude']:
                history.setdefault(a['icao24'], []).append({
                    'time': datetime.now(),
                    'lat': a['latitude'],
                    'lon': a['longitude'],
                    'velocity': a['velocity'] or 0,
                    'callsign': a['callsign']
                })

        if i < snapshots - 1:
            time.sleep(interval_seconds)

    print("\n" + "="*50)
    print("ANALYSIS: Checking for impossible position jumps")
    print("="*50)

    flagged = 0
    for icao24, records in history.items():
        if len(records) < 2:
            continue

        for j in range(1, len(records)):
            prev, curr = records[j-1], records[j]
            dt_seconds = (curr['time'] - prev['time']).total_seconds()
            if dt_seconds <= 0:
                continue

            distance_km = haversine_distance(prev['lat'], prev['lon'], curr['lat'], curr['lon'])
            max_possible_km = (curr['velocity'] * dt_seconds) / 1000 * 1.5  # 50% margin

            if distance_km > max_possible_km and distance_km > 5:
                flagged += 1
                print(f"\n[!] SUSPICIOUS: {icao24} ({curr['callsign']})")
                print(f"    Jumped {distance_km:.1f}km in {dt_seconds:.0f}s")
                print(f"    Reported velocity only allows ~{max_possible_km:.1f}km")
                print(f"    Possible spoofing or data anomaly")

    print(f"\n[+] Monitoring complete. {flagged} suspicious jump(s) flagged out of {len(history)} aircraft tracked.")

if __name__ == "__main__":
    monitor(snapshots=3, interval_seconds=30)