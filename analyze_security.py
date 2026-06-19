import json

def analyze_security(filename='aircraft_data.json'):
    with open(filename, 'r') as f:
        aircraft_list = json.load(f)
    
    print("="*50)
    print("ADS-B SECURITY ANALYSIS REPORT")
    print("="*50)
    
    # Check 1: No callsign (anonymous flights)
    no_callsign = [a for a in aircraft_list if not a['callsign'] or a['callsign'].strip() == '']
    print(f"\n[!] Aircraft with no callsign (anonymous): {len(no_callsign)}")
    for a in no_callsign[:5]:
        print(f"    ICAO24: {a['icao24']} | Country: {a['country']}")

    # Check 2: Duplicate ICAO24 (spoofing indicator)
    icao_list = [a['icao24'] for a in aircraft_list]
    duplicates = [i for i in icao_list if icao_list.count(i) > 1]
    print(f"\n[!] Duplicate ICAO24 addresses (spoofing risk): {len(set(duplicates))}")
    for d in set(duplicates):
        print(f"    ICAO24: {d}")

    # Check 3: Abnormal altitude
    abnormal_alt = [a for a in aircraft_list if a['altitude'] and a['altitude'] > 13000]
    print(f"\n[!] Aircraft at abnormal altitude (>13000m): {len(abnormal_alt)}")
    for a in abnormal_alt:
        print(f"    Callsign: {a['callsign']} | Altitude: {a['altitude']}m")

    # Check 4: Zero velocity at high altitude (spoofing indicator)
    suspicious = [a for a in aircraft_list if a['altitude'] and a['altitude'] > 5000 and a['velocity'] and a['velocity'] < 10]
    print(f"\n[!] Suspicious: High altitude but near-zero velocity: {len(suspicious)}")
    for a in suspicious:
        print(f"    Callsign: {a['callsign']} | Alt: {a['altitude']}m | Velocity: {a['velocity']}m/s")

    print("\n" + "="*50)
    print(f"Total aircraft analyzed: {len(aircraft_list)}")
    print("ADS-B has NO encryption and NO authentication.")
    print("All findings above are potential security vulnerabilities.")
    print("="*50)

if __name__ == "__main__":
    analyze_security()