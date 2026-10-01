import re

LOG_FILE = "../logs/sample_auth.log"


def parse_log_file():
    events = []

    with open(LOG_FILE, "r") as file:
        for line in file:
            if "Failed password" in line:
                match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)

                if match:
                    source_ip = match.group(1)

                    events.append({
                        "event_type": "Failed SSH Login",
                        "source_ip": source_ip,
                        "raw_log": line.strip()
                    })

    return events


if __name__ == "__main__":
    events = parse_log_file()

    for event in events:
        print(event)