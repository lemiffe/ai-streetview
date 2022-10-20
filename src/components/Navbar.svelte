<script>
    import { active } from "tinro";
    import * as markerIcons from "../icons.js";
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

            <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
                <li><a href="/" class="nav-link px-2" use:active exact>Home</a></li>
                <li><a href="/funky" class="nav-link px-2" use:active>Funky Mode</a></li>
                <li><a href="/about" class="nav-link px-2" use:active>About</a></li>
            </ul>

            <div class="text-end">
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

    .nav a {
        text-decoration: none;
        color: #ffffff;
    }

    .nav a:global(.active) {
        color: #ff0068;
    }
</style>
