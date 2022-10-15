<script>
    import * as markerIcons from "./icons.js";
    import Score from "./Score.svelte";

    export let score;
</script>

<header class="p-3 text-bg-dark mb-4">
    <div class="container">
        <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
            <a href="/" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-white text-decoration-none">
                {@html markerIcons.plonk}
                <span class="fs-4 ps-1">This Street View Does Not Exist</span>
            </a>

            <div class="text-end">
                Made by
                <a href="https://twitter.com/lemiffe" target="_blank">@lemiffe</a>,
                <a href="https://twitter.com/pjcr" target="_blank">PJ3</a> &amp;
                <a href="https://twitter.com/offeringofpie" target="_blank">Pie</a>
                <Score {score} />
            </div>
        </div>
    </div>
</header>

<style>
    .text-bg-dark {
        color: #fff !important;
        background-color: RGBA(33, 37, 41, var(--bs-bg-opacity, 1)) !important;
    }

    .text-end a {
        color: #ffffff;
    }
</style>
