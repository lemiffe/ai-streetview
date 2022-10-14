<script>
    import Carousel from "./Carousel.svelte";
    import Maplet from "./Maplet.svelte";
    import mapset from "./mapset.js";
    import Navbar from "./Navbar.svelte";
    import RoundSummary from "./RoundSummary.svelte";

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
    let mapOptions = mapset
        .map((value) => ({ value, sort: Math.random() }))
        .sort((a, b) => a.sort - b.sort)
        .map(({ value }) => value); // Shuffle initial mapset
    let isGuessing = true;
    let gameEnded = false;
    let plonked = false;
    let plonkLatLon = null;
    let guessedLocations = [];
    let showRoundSummary = false;
    let kmDist = 0; // Last round's distance in km
    let roundScore = 0; // Last round's score
    let roundUrl = "";

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

    const chooseMapOption = () => {
        // Select a random map, put it at the end of the list (to avoid selecting it again)
        let rndIndex = Math.floor(Math.random() * (mapOptions.length - 5));
        let rndItem = mapOptions.splice(rndIndex, 1)[0];
        mapOptions.push(rndItem);
        return rndItem;
    };

    function chooseMapsForGame() {
        // Select 5 random rounds from available options
        if (mapOptions.length <= 5) {
            return mapOptions;
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
        roundScore = calculateRoundScore(kmDist);
        roundUrl = currGameMaps[currRound - 1].streetUrl;
        addScore(roundScore);
        console.log("Distance:", kmDist, "Score:", roundScore);

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
        if (e.keyCode === 32 && isGuessing && plonked) {
            makeGuess();
        }
    }

    newGame();
</script>

<svelte:window on:resize={resizeMaplet} on:keydown={onKeyDown} />

<Navbar {score} />

<div class="container-xl">
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
                <RoundSummary {gameEnded} {roundScore} {score} {kmDist} {roundUrl} />
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
    .row-map {
        min-height: 600px;
    }

    #carousel-container {
        position: relative;
        overflow: hidden;
    }

    @media (min-width: 1400px) {
        .container-xl {
            max-width: 1600px;
        }
    }
</style>
