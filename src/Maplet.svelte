<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();
    import L, { latLng } from "leaflet";
    import * as markerIcons from "./icons.js";

    let markerLayer;
    let lineLayer;
    let map;
    let myMarkerLayer;
    let currMarker;
    const defaultLatLon = [60, 1];
    export let isGuessing;

    function createMap(container) {
        let m = L.map(container, {
            preferCanvas: true,
        }).setView(defaultLatLon, 2);
        L.tileLayer("https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png", {
            attribution: `&copy;<a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>,
	        	&copy;<a href="https://carto.com/attributions" target="_blank">CARTO</a>`,
            subdomains: "abcd",
            maxZoom: 18,
        }).addTo(m);

        m.on("click", function (e) {
            if (!isGuessing) {
                return;
            }
            const latLng = [e.latlng.lat, e.latlng.lng];
            if (currMarker) {
                currMarker.setLatLng(latLng);
            } else {
                currMarker = createMarker(latLng, "plonk");
                currMarker.on("click", removeMarker);
                myMarkerLayer.addLayer(currMarker);
            }
            dispatch("plonk", { plonked: true, latlon: latLng });
        });

        return m;
    }

    function mapAction(container) {
        map = createMap(container);

        myMarkerLayer = L.layerGroup();
        markerLayer = L.layerGroup();
        lineLayer = L.layerGroup();

        myMarkerLayer.addTo(map);
        markerLayer.addTo(map);
        lineLayer.addTo(map);

        return {
            destroy: () => {
                map.remove();
                map = null;
            },
        };
    }

    function removeMarker() {
        if (!isGuessing) {
            return;
        }
        currMarker = null;
        dispatch("plonk", { plonked: false, latlon: null });
        myMarkerLayer.clearLayers();
    }

    function createMarker(loc, iconName) {
        const html = `<div class="map-marker">${markerIcons[iconName]}</div>`;
        const icon = L.divIcon({
            html,
            className: "map-marker",
        });
        return L.marker(loc, { icon });
    }

    function createLine(locations) {
        return L.polyline(locations, { color: "#E4E", opacity: 0.5 });
    }

    export const line = (latLons) => {
        lineLayer.addLayer(createLine(latLons));
    };

    export const addMarkers = (markerLocations, svgName) => {
        for (let location of markerLocations) {
            let m = createMarker(location, svgName);
            markerLayer.addLayer(m);
        }
    };

    export const fly = (markerLocations) => {
        if (!markerLocations || markerLocations.length === 0) {
            map.flyTo(defaultLatLon, 2, {
                animate: true,
                duration: 0.4,
            });
        } else {
            map.flyToBounds(markerLocations, {
                animate: true,
                duration: 1.5,
            });
        }
    };

    export const resize = () => {
        if (map) {
            map.invalidateSize();
        }
    };

    export const reset = () => {
        // Called from parent component to reset map and remove all elements
        if (markerLayer) {
            markerLayer.clearLayers();
        }
        if (myMarkerLayer) {
            currMarker = null;
            dispatch("plonk", { plonked: false, latlon: null });
            myMarkerLayer.clearLayers();
        }
        if (map) {
            lineLayer.clearLayers();
        }
    };
</script>

<link
    rel="stylesheet"
    href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css"
    integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
    crossorigin=""
/>

<div class="map" style="height:100%; width:100%" use:mapAction />

<style>
    :global(.leaflet-grab) {
        cursor: default !important;
    }

    .map :global(.map-marker) {
        width: 30px;
        transform: translateX(-32%) translateY(-78%);
    }
</style>
