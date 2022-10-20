<script>
    import About from "./pages/About.svelte";
    import Game from "./pages/Game.svelte";
    import mapset from "./mapset.js";
    import mapsetFunky from "./mapsetFunky.js";
    import Navbar from "./components/Navbar.svelte";
    import { Route } from "tinro";
    let score = 0;

    // Functions to trigger sub-component events (bound)
    let resizeMaplet = () => {};
    let onKeyDown = () => {};
</script>

<svelte:window on:resize={resizeMaplet} on:keydown={onKeyDown} />

<Navbar {score} />
<!-- TODO: Update selected nav item | update individual score! -->

<Route path="/">
    <Game {mapset} bind:resizeMaplet bind:onKeyDown bind:score />
</Route>
<Route path="/funky">
    <Game mapset={mapsetFunky} bind:resizeMaplet bind:onKeyDown bind:score />
</Route>
<Route path="/about">
    <About {mapset} {mapsetFunky} />
</Route>

<style>
</style>
