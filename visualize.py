import json
import folium

def visualize_aircraft(filename='aircraft_data.json'):
    with open(filename, 'r') as f:
        aircraft_list = json.load(f)
    
    # Center map on average position
    valid_aircraft = [a for a in aircraft_list if a['latitude'] and a['longitude']]
    avg_lat = sum(a['latitude'] for a in valid_aircraft) / len(valid_aircraft)
    avg_lon = sum(a['longitude'] for a in valid_aircraft) / len(valid_aircraft)
    
    flight_map = folium.Map(location=[avg_lat, avg_lon], zoom_start=3, tiles='CartoDB dark_matter')
    
    for a in valid_aircraft:
        # Color code: red for anonymous, blue for normal
        color = 'red' if not a['callsign'] or a['callsign'].strip() == '' else 'blue'
        
        popup_text = f"""
        ICAO24: {a['icao24']}<br>
        Callsign: {a['callsign'] if a['callsign'] else 'ANONYMOUS'}<br>
        Country: {a['country']}<br>
        Altitude: {a['altitude']}m<br>
        Velocity: {a['velocity']}m/s
        """
        
        folium.CircleMarker(
            location=[a['latitude'], a['longitude']],
            radius=5,
            popup=popup_text,
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.7
        ).add_to(flight_map)
    
    flight_map.save('aircraft_map.html')
    print(f"[+] Map saved to aircraft_map.html")
    print(f"[+] Plotted {len(valid_aircraft)} aircraft")
    print(f"[+] Red markers = anonymous flights (no callsign)")
    print(f"[+] Blue markers = normal flights")

if __name__ == "__main__":
    visualize_aircraft()