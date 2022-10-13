<script>
    import Carousel from "./Carousel.svelte";
    import Maplet from "./Maplet.svelte";
    import Score from "./Score.svelte";
    import mapset from "./mapset.js";
    import * as markerIcons from "./icons.js";
    import { fly } from "svelte/transition";

    // Functions to trigger sub-component events (bound)

    let resetCarousel = () => {};
    let resetMaplet = () => {};
    let resizeMaplet = () => {};
    let createLine = () => {};
    let addMarkers = () => {};
    let flyToBounds = () => {};

    // Game logic

    let score = 0;
    let currGameMaps = [];
    let currRound = 0;
    let currImages = [];
    let mapOptions = mapset;
    let isGuessing = true;
    let gameEnded = false;
    let plonked = false;
    let plonkLatLon = null;
    let guessedLocations = [];
    let showRoundSummary = false;
    let kmDist = 0; // Last round's distance

    function updateMarkerSet(e) {
        plonked = e.detail.plonked;
        plonkLatLon = e.detail.latlon;
    }

    function addScore(delta) {
        score += delta;
    }

    function resetScore() {
        score = 0;
    }

    const shuffleMapset = () => {
        // Shuffle initial mapset
        mapOptions = mapset
            .map((value) => ({ value, sort: Math.random() }))
            .sort((a, b) => a.sort - b.sort)
            .map(({ value }) => value);
        return mapOptions;
    };

    const chooseMapOption = () => {
        // Select a random map, put it at the end of the list (to avoid selecting it again)
        let map = mapOptions.splice(Math.floor(Math.random() * mapOptions.length - 5), 1)[0];
        mapOptions.push(map);
        return map;
    };

    function chooseMapsForGame() {
        // Select 5 random rounds from available options
        if (mapOptions.length <= 5) {
            return shuffleMapset();
        }
        const maps = [];
        for (let i = 0; i < 5; i++) {
            maps.push(chooseMapOption());
        }
        return maps;
    }

    function calculateRoundScore(distanceInKm) {
        if (distanceInKm <= 0.15) {
            return 5000;
        } else if (distanceInKm > 14800) {
            return 0;
        }
        return Math.round(5000.054 * Math.pow(0.99933, distanceInKm));
    }

    function newGame() {
        currRound = 0;
        isGuessing = true;
        gameEnded = false;
        guessedLocations = [];
        currGameMaps = chooseMapsForGame();
        console.log("New game! Maps:", currGameMaps);
        resetScore();
        resetMaplet();
        nextRound();
    }

    function endGame() {
        // Todo: Show final score overlay, maybe link to the geo map as well?
        gameEnded = true;
        isGuessing = false;
    }

    function nextRound() {
        currRound += 1;
        isGuessing = true;
        showRoundSummary = false;
        currImages = currGameMaps[currRound - 1].images;
        resetMaplet();
        flyToBounds();
        resetCarousel();
    }

    function getDistanceFromLatLonInKm(latlon1, latlon2) {
        var R = 6371;
        var dLat = deg2rad(latlon2[0] - latlon1[0]);
        var dLon = deg2rad(latlon2[1] - latlon1[1]);
        var a =
            Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(deg2rad(latlon1[0])) * Math.cos(deg2rad(latlon2[0])) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
        var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        var d = R * c;
        return d;
    }

    function deg2rad(deg) {
        return deg * (Math.PI / 180);
    }

    function makeGuess() {
        guessedLocations.push(plonkLatLon);
        kmDist = getDistanceFromLatLonInKm(plonkLatLon, currGameMaps[currRound - 1].latlon);
        const roundScore = calculateRoundScore(kmDist);
        addScore(roundScore);
        console.log("Distance:", kmDist, "Score:", roundScore);
        // Todo: Show end of round overlay
        // - Show points for this round (animate?)
        // - Show link to map (external link)

        isGuessing = false;
        if (currRound === 5) {
            for (let i = 0; i < guessedLocations.length; i++) {
                addMarkers([currGameMaps[i].latlon], "plonkGreen");
                createLine([guessedLocations[i], currGameMaps[i].latlon]);
                if (i < guessedLocations.length - 1) {
                    addMarkers([guessedLocations[i]], "plonk");
                }
            }
            flyToBounds();
            endGame();
        } else {
            addMarkers([currGameMaps[currRound - 1].latlon], "plonkGreen");
            createLine([plonkLatLon, currGameMaps[currRound - 1].latlon]);
            flyToBounds([plonkLatLon, currGameMaps[currRound - 1].latlon]);
        }

        showRoundSummary = true;
    }

    function onKeyDown(e) {
        if (e.keyCode === 32 && isGuessing) {
            makeGuess();
        }
    }

    newGame();
</script>

<svelte:window on:resize={resizeMaplet} on:keydown|preventDefault={onKeyDown} />

<div class="container">
    <header class="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom">
        <a href="/" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none">
            {@html markerIcons.plonk}
            <span class="fs-4 ps-1">This Street View Does Not Exist</span>
        </a>

        <ul class="nav nav-pills">
            <li class="nav-item">
                Made by
                <a href="https://hyperfollow.com/lemiffe" target="_blank">@lemiffe</a>
                and
                <a href="https://twitter.com/pjcr" target="_blank">@pjcr</a>
                <Score {score} />
            </li>
        </ul>
    </header>
</div>

<div class="container">
    <div class="row pt-1 mb-3 align-items-end">
        <div class="col">
            <p style="text-align: center; font-size: 1.2em;">
                <strong class="danger">At least 50% of every image on this page has been generated by AI</strong><br />
                <i>Can you figure out where you are regardless?</i>
            </p>
        </div>
    </div>
    <div class="row mb-3 row-map">
        <div id="carousel-container" class="col-lg-6">
            {#if showRoundSummary}
                <div transition:fly={{ y: -100, duration: 1500 }} class="round-summary">
                    {#if !gameEnded}
                        <p>Game has ended</p>
                    {:else}
                        <p>You were {kmDist}km away!</p>
                    {/if}
                </div>
            {/if}
            <Carousel images={currImages} bind:reset={resetCarousel} />
        </div>
        <div class="col-lg-6">
            <Maplet
                bind:reset={resetMaplet}
                bind:resize={resizeMaplet}
                bind:line={createLine}
                bind:addMarkers
                bind:fly={flyToBounds}
                on:plonk={updateMarkerSet}
                {isGuessing}
            />
        </div>
    </div>
    <div class="row mb-3 align-items-end">
        <div class="col" style="text-align: right;">
            {#if !isGuessing && !gameEnded}
                <button type="button" class="btn btn-lg btn-info" on:click={nextRound}>Next Round</button>
            {:else if isGuessing && !gameEnded && plonked}
                <button type="button" class="btn btn-lg btn-success" on:click={makeGuess}>Guess</button>
            {/if}
            <button type="button" class="btn btn-lg btn-danger ms-2" on:click={newGame}>New Game</button>
        </div>
    </div>
</div>

<style>
    .nav-item a {
        text-decoration: none;
    }

    .row-map {
        min-height: 600px;
    }

    #carousel-container {
        position: relative;
        overflow: hidden;
    }

    .round-summary {
        top: 0;
        width: calc(100% - var(--bs-gutter-x));
        text-align: center;
        position: absolute;
        z-index: 1000;
        background-color: rgba(0, 0, 0, 0.5);
        padding: calc(var(--bs-gutter-x) * 0.5);
        margin-right: calc(var(--bs-gutter-x) * 0.5);
    }

    .round-summary p {
        margin: 0;
        color: #ffffff;
    }
</style>
