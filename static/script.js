// static/script.js
console.log("Map script loaded");

// Create map
const map = L.map("map", { preferCanvas: true }).setView([20.5937, 78.9629], 5);

// Better UX: disable scrollZoom by default (prevents accidental page scroll capture)
map.scrollWheelZoom.disable();

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    noWrap: true
}).addTo(map);

// keep world bound
map.setMaxBounds(L.latLngBounds([-85, -180], [85, 180]));

// marker cluster group
const markerCluster = L.markerClusterGroup({
    maxClusterRadius: 60,
    showCoverageOnHover: false
});
map.addLayer(markerCluster);

// helper to fetch and draw
function loadPoints() {
    const bounds = map.getBounds();
    const bbox = [bounds.getSouth(), bounds.getWest(), bounds.getNorth(), bounds.getEast()].join(",");
    const zoom = map.getZoom();

    const city = document.getElementById("city") ? document.getElementById("city").value : "All";
    const cuisine = document.getElementById("cuisine") ? document.getElementById("cuisine").value : "All";

    fetch(`/map_data?bbox=${bbox}&zoom=${zoom}&city=${encodeURIComponent(city)}&cuisine=${encodeURIComponent(cuisine)}`)
        .then(r => r.json())
        .then(items => {
            markerCluster.clearLayers();

            items.forEach(p => {
                if (p.is_cluster) {
                    // dynamic size for cluster bubble
                    let size = 18;
                    if (p.count > 20) size = 26;
                    if (p.count > 50) size = 34;
                    if (p.count > 150) size = 46;

                    let marker = L.marker([p.lat, p.lon], {
                        icon: L.divIcon({
                            className: "cluster-circle",
                            html: `<div style="width:${size}px;height:${size}px;border-radius:50%;background:rgba(44,123,229,0.28);border:2px solid rgba(44,123,229,0.8);box-shadow:0 0 10px rgba(44,123,229,0.45);"></div>`,
                            iconSize: [size, size]
                        })
                    });

                    marker.bindPopup(`<b>${p.count} restaurants</b><br>${p.examples.join("<br>")}`);
                    markerCluster.addLayer(marker);

                } else {
                    // individual restaurant marker
                    const color = p.color || "#2c7be5";
                    let icon = L.divIcon({
                        className: "point-marker",
                        html: `<div style="width:12px;height:12px;border-radius:50%;background:${color};border:2px solid white;"></div>`,
                        iconSize: [16, 16]
                    });

                    let marker = L.marker([p.lat, p.lon], { icon: icon });
                    let ratingColor = p.rating >= 4.5 ? "#0a8f08" : (p.rating >= 3.5 ? "#e67e22" : "#c0392b");
                    marker.bindPopup(`
                        <div style="width:220px">
                            <div style="font-weight:700;color:#0e3d75;margin-bottom:6px">${p.name}</div>
                            <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
                                <div style="background:${ratingColor};color:white;padding:4px 8px;border-radius:6px;font-weight:700">⭐ ${p.rating}</div>
                                <div style="font-size:13px;color:#333">${p.cuisine}</div>
                            </div>
                            <div style="font-size:13px;color:#666">📍 ${p.city}</div>
                        </div>
                    `);
                    markerCluster.addLayer(marker);
                }
            });

        })
        .catch(err => {
            console.error("Failed to load map data:", err);
        });
}

// re-load points on moveend & zoomend
map.on("moveend", loadPoints);
map.on("zoomend", loadPoints);

// filter button click
const filterBtn = document.getElementById("filterBtn");
if (filterBtn) {
    filterBtn.addEventListener("click", () => {
        // If map is scrolled into view, keep map interactions disabled; users can use controls to zoom
        loadPoints();
    });
}

// initial load after short delay so map tiles render
setTimeout(() => loadPoints(), 300);
