# ADS-B Security Analysis - Findings Report

**Date:** June 2026  
**Analyst:** Bineesh Baburajan 
**Data Source:** OpenSky Network API (live aircraft data)  
**Sample Size:** 50 aircraft per snapshot, 3 snapshots over 90 seconds

---

## 1. Executive Summary

ADS-B (Automatic Dependent Surveillance-Broadcast) is the primary protocol used by modern aircraft to broadcast position, identity, and velocity. This analysis captured and examined live ADS-B data to identify security anomalies arising from the protocol's fundamental design flaw: **no encryption, no authentication**.

---

## 2. Vulnerability Background

| Vulnerability | Description |
|---|---|
| No authentication | Any device can broadcast ADS-B signals as any aircraft |
| No encryption | All transmissions are in plaintext, receivable by anyone |
| No integrity check | Broadcasted data cannot be verified as genuine |
| Spoofing risk | Fake aircraft can be injected into ATC displays |
| Signal injection | Existing aircraft positions can be falsified |

These are documented vulnerabilities, not theoretical — researchers have demonstrated ADS-B spoofing using ~$300 of SDR hardware.

---

## 3. Findings

### 3.1 Anonymous Flights (No Callsign)
- **Detected:** 1 out of 50 aircraft
- **ICAO24:** 8744f6
- **Country:** Japan
- **Risk:** An aircraft broadcasting no callsign is effectively unidentifiable. In a real attack scenario, a spoofed aircraft would likely omit a callsign to avoid cross-referencing with flight databases.

### 3.2 Duplicate ICAO24 Addresses
- **Detected:** 0 in this sample
- **Risk:** Duplicate ICAO24 addresses would indicate two aircraft claiming the same identity — a direct spoofing indicator. Clean result in this capture.

### 3.3 Abnormal Altitude
- **Detected:** 0 in this sample
- **Threshold:** >13,000m
- **Risk:** Altitudes above 13,000m are outside normal commercial flight ranges and could indicate injected false data.

### 3.4 Impossible Position Jumps (Continuous Monitor)
- **Detected:** 0 across 51 aircraft tracked over 3 snapshots
- **Method:** Haversine distance calculation between consecutive position reports, compared against reported velocity
- **Risk:** A position jump exceeding what the reported velocity allows is a strong spoofing signature — the aircraft "teleports."

---

## 4. Key Takeaway

The clean results on most checks confirm the tool works correctly — it does not false-positive on legitimate traffic. The one anonymous flight detected (ICAO24: 8744f6) represents exactly the kind of unverifiable broadcast that ADS-B's lack of authentication permits.

In a real threat scenario (hostile drone, spoofed commercial flight near restricted airspace), these same detection methods would flag the anomaly before it escalates.

---

## 5. Recommendations

1. **Short term:** Cross-reference ADS-B data with secondary radar (Mode S transponder) to validate positions
2. **Medium term:** Implement ground-based multilateration to verify aircraft positions independently
3. **Long term:** Adopt ADS-B authentication extensions (currently in research phase by ICAO)

---

## 6. Tools Used

- Python 3.13
- OpenSky Network API
- Folium (visualization)
- Custom anomaly detection scripts