<script>
    import * as markerIcons from "./icons.js";
    import Score from "./Score.svelte";

    export let score;
</script>

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

<style>
    .nav-item a {
        text-decoration: none;
    }
</style>
