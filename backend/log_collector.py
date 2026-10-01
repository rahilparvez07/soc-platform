import subprocess
import os

UBUNTU_USER = "wazuh"
UBUNTU_IP = "192.168.8.132"

REMOTE_LOG = "/tmp/conn.log"

LOCAL_LOG = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../logs/conn.log"
    )
)


def collect_zeek_log():

    command = [
        "scp",
        f"{UBUNTU_USER}@{UBUNTU_IP}:{REMOTE_LOG}",
        LOCAL_LOG
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("✅ Zeek log collected successfully")
        print(f"Saved to: {LOCAL_LOG}")
    else:
        print("❌ Failed to collect Zeek log")
        print(result.stderr)


if __name__ == "__main__":
    collect_zeek_log()
