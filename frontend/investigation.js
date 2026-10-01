async function loadAlert() {

    const parameters = new URLSearchParams(
        window.location.search
    );

    const alertId = parameters.get("id");

    if (!alertId) {

        document.getElementById("alert-container").innerHTML =
            "<p>Alert ID missing.</p>";

        return;
    }


    const response = await fetch(
        `/api/alerts/${alertId}`
    );


    if (!response.ok) {

        document.getElementById("alert-container").innerHTML =
            "<p>Alert not found.</p>";

        return;
    }


    const alert = await response.json();


    document.getElementById("alert-container").innerHTML = `

        <div class="investigation-card">

            <h2>Incident #${alert.id}</h2>

            <div class="detail">

                <strong>Rule:</strong>

                <span>${alert.rule}</span>

            </div>


            <div class="detail">

                <strong>Severity:</strong>

                <span class="severity-${alert.severity.toLowerCase()}">
                    ${alert.severity}
                </span>

            </div>


            <div class="detail">

                <strong>Status:</strong>

                <span>${alert.status}</span>

            </div>


            <div class="detail">

                <strong>Timestamp:</strong>

                <span>${alert.timestamp}</span>

            </div>


            <div class="detail">

                <strong>Source IP:</strong>

                <span>${alert.source_ip}</span>

            </div>


            <div class="detail">

                <strong>Attempts / Ports:</strong>

                <span>${alert.failed_attempts}</span>

            </div>


            <div class="detail">

                <strong>MITRE ATT&CK:</strong>

                <span>${alert.mitre_attack}</span>

            </div>


            <div class="description">

                <h3>Description</h3>

                <p>${alert.description}</p>

            </div>


            <div class="actions">

                <button onclick="updateStatus('Investigating')">
                    Investigate
                </button>

                <button onclick="updateStatus('Resolved')">
                    Resolve
                </button>

            </div>

        </div>
    `;
}


async function updateStatus(status) {

    const parameters = new URLSearchParams(
        window.location.search
    );

    const alertId = parameters.get("id");


    const response = await fetch(
        `/api/alerts/${alertId}/status`,
        {
            method: "PUT",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                status: status
            })
        }
    );


    if (response.ok) {

        alert(`Alert marked as ${status}`);

        loadAlert();

    } else {

        alert("Failed to update alert");

    }
}


loadAlert();