<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();
    import L from "leaflet";
    import * as markerIcons from "./icons.js";

    let markerLayer;
    let lineLayer;
    let map;
    let myMarkerLayer;
    let currMarker;
    const defaultLatLon = [30, 1];
    export let isGuessing;

    function createMap(container) {
        let m = L.map(container, {
            preferCanvas: true,
            scrollWheelZoom: false, // disable original zoom function
            smoothWheelZoom: true, // enable smooth zoom
            smoothSensitivity: 2, // zoom speed. default is 1
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

    /* Smooth scroll: https://github.com/mutsuyuki/Leaflet.SmoothWheelZoom */

    L.Map.mergeOptions({
        // @section Mousewheel options
        // @option smoothWheelZoom: Boolean|String = true
        // Whether the map can be zoomed by using the mouse wheel. If passed `'center'`,
        // it will zoom to the center of the view regardless of where the mouse was.
        smoothWheelZoom: true,

        // @option smoothWheelZoom: number = 1
        // setting zoom speed
        smoothSensitivity: 1,
    });

    L.Map.SmoothWheelZoom = L.Handler.extend({
        addHooks: function () {
            L.DomEvent.on(this._map._container, "wheel", this._onWheelScroll, this);
        },

        removeHooks: function () {
            L.DomEvent.off(this._map._container, "wheel", this._onWheelScroll, this);
        },

        _onWheelScroll: function (e) {
            if (!this._isWheeling) {
                this._onWheelStart(e);
            }
            this._onWheeling(e);
        },

        _onWheelStart: function (e) {
            var map = this._map;
            this._isWheeling = true;
            this._wheelMousePosition = map.mouseEventToContainerPoint(e);
            this._centerPoint = map.getSize()._divideBy(2);
            this._startLatLng = map.containerPointToLatLng(this._centerPoint);
            this._wheelStartLatLng = map.containerPointToLatLng(this._wheelMousePosition);
            this._startZoom = map.getZoom();
            this._moved = false;
            this._zooming = true;

            map._stop();
            if (map._panAnim) map._panAnim.stop();

            this._goalZoom = map.getZoom();
            this._prevCenter = map.getCenter();
            this._prevZoom = map.getZoom();

            this._zoomAnimationId = requestAnimationFrame(this._updateWheelZoom.bind(this));
        },

        _onWheeling: function (e) {
            var map = this._map;

            this._goalZoom = this._goalZoom + L.DomEvent.getWheelDelta(e) * 0.003 * map.options.smoothSensitivity;
            if (this._goalZoom < map.getMinZoom() || this._goalZoom > map.getMaxZoom()) {
                this._goalZoom = map._limitZoom(this._goalZoom);
            }
            this._wheelMousePosition = this._map.mouseEventToContainerPoint(e);

            clearTimeout(this._timeoutId);
            this._timeoutId = setTimeout(this._onWheelEnd.bind(this), 200);

            L.DomEvent.preventDefault(e);
            L.DomEvent.stopPropagation(e);
        },

        _onWheelEnd: function (e) {
            this._isWheeling = false;
            cancelAnimationFrame(this._zoomAnimationId);
            this._map._moveEnd(true);
        },

        _updateWheelZoom: function () {
            var map = this._map;

            if (!map.getCenter().equals(this._prevCenter) || map.getZoom() != this._prevZoom) return;

            this._zoom = map.getZoom() + (this._goalZoom - map.getZoom()) * 0.3;
            this._zoom = Math.floor(this._zoom * 100) / 100;

            var delta = this._wheelMousePosition.subtract(this._centerPoint);
            if (delta.x === 0 && delta.y === 0) return;

            if (map.options.smoothWheelZoom === "center") {
                this._center = this._startLatLng;
            } else {
                this._center = map.unproject(
                    map.project(this._wheelStartLatLng, this._zoom).subtract(delta),
                    this._zoom
                );
            }

            if (!this._moved) {
                map._moveStart(true, false);
                this._moved = true;
            }

            map._move(this._center, this._zoom);
            this._prevCenter = map.getCenter();
            this._prevZoom = map.getZoom();

            this._zoomAnimationId = requestAnimationFrame(this._updateWheelZoom.bind(this));
        },
    });

    L.Map.addInitHook("addHandler", "smoothWheelZoom", L.Map.SmoothWheelZoom);
</script>

<link
    rel="stylesheet"
    href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css"
    integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
    crossorigin=""
/>

<div class="map ratio ratio-1x1" style="height:100%; width:100%" use:mapAction />

<style>
    :global(.leaflet-grab) {
        cursor: default !important;
    }

    .map :global(.map-marker) {
        width: 30px;
        transform: translateX(-32%) translateY(-78%);
    }
</style>
