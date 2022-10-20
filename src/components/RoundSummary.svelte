<script>
    import { fly } from "svelte/transition";

    export let gameEnded;
    export let roundScore;
    export let score;
    export let kmDist;
    export let roundUrl;
</script>

<div transition:fly|local={{ y: -100, duration: 1500 }} class="round-summary pt-4 pb-4">
    {#if gameEnded}
        <h3>Final score: {score} Points!</h3>
        <p>You were {Math.round(kmDist * 100) / 100}km away ({roundScore} pts)!</p>
    {:else}
        <h3>+{roundScore} Points!</h3>
        <p>You were {Math.round(kmDist * 100) / 100}km away!</p>
    {/if}
    <p class="mt-1">
        <a href={roundUrl} target="_blank">Click here <sup>[&#2197;]</sup></a> to see the original street view.
    </p>
</div>

<style>
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

    .round-summary h3 {
        color: #ffffff;
    }
    .round-summary p,
    .round-summary a,
    .round-summary a:link,
    .round-summary a:hover {
        margin: 0;
        color: #ffffff;
    }
</style>
