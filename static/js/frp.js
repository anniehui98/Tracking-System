let overallChart = null;

async function loadFrpPercent() {
    const startInput = document.getElementById("start_datetime").value;
    const endInput = document.getElementById("end_datetime").value;
    const start = startInput || "";
    const end = endInput || "";

    const loading = document.getElementById("loading");
    loading.classList.add("show");

    try {
        const res = await fetch(`/api/frp_manual_coin_percent?start=${encodeURIComponent(start)}&end=${encodeURIComponent(end)}`);
        const data = await res.json();

        let totalOnline = 0;
        let totalOffline = 0;
        let count = 0;

        for (const [url, stat] of Object.entries(data)) {
            const onlineCell = document.getElementById(`online-${url}`);
            const machineCell = document.getElementById(`machine-${url}`);
            const activationCell = document.getElementById(`activation-${url}`);

            // const offlineCell = document.getElementById(`offline-${url}`);
            if (!onlineCell) continue;

            const row = onlineCell.parentElement;
            const startCell = row.querySelector(".start-cell");
            const endCell = row.querySelector(".end-cell");

            if (stat.error) {
                onlineCell.innerText = "No Data";
                // offlineCell.innerText = "Error";
                if (startCell) startCell.innerText = "-";
                if (endCell) endCell.innerText = "-";
                continue;
            }

            const onlinePercent = stat.percent?.online ?? 0;
            const offlinePercent = stat.percent?.offline ?? 0;

            if (activationCell) activationCell.innerText = stat.activation + "%" ?? "-";

            onlineCell.innerText = onlinePercent + "%";
            // offlineCell.innerText = offlinePercent + "%";

            if (machineCell) machineCell.innerText = stat.machine ?? "-";

            if (startCell) startCell.innerText = stat.start ? new Date(stat.start)
                .toISOString()
                .replace("T", ", ")
                .replace(/\.\d+Z$/, "")
                : "-";

            if (endCell) {
                endCell.innerText = stat.end
                    ? new Date(stat.end)
                        .toISOString()
                        .replace("T", ", ")
                        .replace(/\.\d+Z$/, "")
                    : "-";
            }

            const link = row.querySelector("a.manual-coin-link");
            if (link) {
                link.dataset.start = stat.start ?? "";
                link.dataset.end = stat.end ?? "";
            }

            totalOnline += onlinePercent;
            totalOffline += offlinePercent;
            count += 1;
        }

        const overallOnline = count > 0 ? (totalOnline / count) : 0;
        const overallOffline = count > 0 ? (totalOffline / count) : 0;
        document.getElementById("overallOnline").innerText = overallOnline.toFixed(1);
        document.getElementById("overallOffline").innerText = overallOffline.toFixed(1);

        const ctx = document.getElementById('overallChart').getContext('2d');
        if (overallChart) overallChart.destroy();

        overallChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Online %', 'Offline %'],
                datasets: [{
                    data: [overallOnline, overallOffline],
                    backgroundColor: ['#4CAF50', '#FF6600']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return context.label + ': ' + context.parsed.toFixed(1) + '%';
                            }
                        }
                    }
                }
            }
        });

        document.querySelectorAll('a.manual-coin-link').forEach(a => {
            const frpUrl = a.dataset.frpUrl;

            const rowStart = a.dataset.start || "";
            const rowEnd = a.dataset.end || "";

            a.href = `/ha/manual_coin_stats?frp_url=${encodeURIComponent(frpUrl)}`
                + `&start=${encodeURIComponent(rowStart)}`
                + `&end=${encodeURIComponent(rowEnd)}`;
        });

    } catch (err) {
        console.error("Failed to load online/offline percent:", err);
    } finally {
        setTimeout(() => loading.classList.remove("show"), 300);
    }
}

window.addEventListener("DOMContentLoaded", loadFrpPercent);