from parser import parse_log_file
from network_parser import parse_network_log
from database import create_database, save_alert
from zeek_parser import parse_zeek_conn_log

BRUTE_FORCE_THRESHOLD = 5


def detect_brute_force(events):
    ip_counts = {}

    for event in events:
        if event["event_type"] == "Failed SSH Login":
            ip = event["source_ip"]

            if ip not in ip_counts:
                ip_counts[ip] = 0

            ip_counts[ip] += 1

    alerts = []

    for ip, count in ip_counts.items():
        if count >= BRUTE_FORCE_THRESHOLD:
            alert = {
                "rule": "SSH Brute Force",
                "severity": "HIGH",
                "source_ip": ip,
                "failed_attempts": count,
                "description": "Multiple failed SSH login attempts detected",
                "mitre_attack": "T1110"
            }

            alerts.append(alert)

    return alerts

PORT_SCAN_THRESHOLD = 5


def detect_port_scan(events):

    source_ports = {}

    for event in events:

        if event["event_type"] == "Network Connection":

            ip = event["source_ip"]

            if ip not in source_ports:
                source_ports[ip] = set()

            source_ports[ip].add(event["destination_port"])

    alerts = []

    for ip, ports in source_ports.items():

        if len(ports) >= PORT_SCAN_THRESHOLD:

            alert = {
                "rule": "Port Scan",
                "severity": "MEDIUM",
                "source_ip": ip,
                "failed_attempts": len(ports),
                "description": "Multiple destination ports contacted from the same source",
                "mitre_attack": "T1046"
            }

            alerts.append(alert)

    return alerts

if __name__ == "__main__":

    create_database()

    # SSH detection
    auth_events = parse_log_file()

    ssh_alerts = detect_brute_force(auth_events)

    # Network detection
    network_events = parse_zeek_conn_log()
    port_scan_alerts = detect_port_scan(network_events)

    # Combine all alerts
    alerts = ssh_alerts + port_scan_alerts

    for alert in alerts:

        save_alert(alert)

        print("\n🚨 SECURITY ALERT")
        print("-------------------------")
        print(f"Rule: {alert['rule']}")
        print(f"Severity: {alert['severity']}")
        print(f"Source IP: {alert['source_ip']}")
        print(f"Attempts/Ports: {alert['failed_attempts']}")
        print(f"Description: {alert['description']}")
        print(f"MITRE ATT&CK: {alert['mitre_attack']}")