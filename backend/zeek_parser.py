LOG_FILE = "../logs/conn.log"


def parse_zeek_conn_log():

    events = []

    with open(LOG_FILE, "r") as file:

        fields = None

        for line in file:

            line = line.strip()

            if line.startswith("#fields"):
                fields = line.split("\t")[1:]
                continue

            if line.startswith("#") or not line:
                continue

            values = line.split("\t")

            if not fields:
                continue

            event = dict(zip(fields, values))

            if "id.orig_h" not in event:
                continue

            events.append({
                "event_type": "Network Connection",
                "source_ip": event["id.orig_h"],
                "destination_ip": event["id.resp_h"],
                "destination_port": int(event["id.resp_p"]),
                "protocol": event["proto"],
                "raw_log": line
            })

    return events


if __name__ == "__main__":

    events = parse_zeek_conn_log()

    print(f"Parsed events: {len(events)}")

    for event in events[-10:]:
        print(event)