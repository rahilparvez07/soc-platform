import re

LOG_FILE = "../logs/sample_network.log"


def parse_network_log():
    events = []

    with open(LOG_FILE, "r") as file:
        for line in file:

            match = re.search(
                r"from (\d+\.\d+\.\d+\.\d+) "
                r"to (\d+\.\d+\.\d+\.\d+):(\d+)",
                line
            )

            if match:
                source_ip = match.group(1)
                destination_ip = match.group(2)
                destination_port = int(match.group(3))

                events.append({
                    "event_type": "Network Connection",
                    "source_ip": source_ip,
                    "destination_ip": destination_ip,
                    "destination_port": destination_port,
                    "raw_log": line.strip()
                })

    return events


if __name__ == "__main__":

    events = parse_network_log()

    for event in events:
        print(event)