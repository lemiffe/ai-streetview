<script>
    export let mapset;
    export let mapsetFunky;
</script>

<div class="container">
    <div class="row pt-1 mb-3 align-items-end">
        <div class="col">
            <h1>About the game</h1>
            <p style="font-size: 1.1em" class="mb-3">
                <strong class="danger">At least 50% of every image has been generated by AI: </strong><i
                    >Can you figure out where you are regardless?</i
                >
            </p>
            <p>
                <strong>Credits:</strong>
            </p>
            <ul>
                <li>
                    <a href="https://twitter.com/lemiffe" target="_blank">@lemiffe</a> - Development &amp; maps/images
                </li>
                <li><a href="https://twitter.com/pjcr" target="_blank">@pjcr</a> - Maps/images</li>
                <li>
                    <a href="https://twitter.com/offeringofpie" target="_blank">@offeringofpie</a> - Svelte code bugfixes
                </li>
                <li><a href="https://twitter.com/aniulyy" target="_blank">@aniulyy</a> - Beta testing</li>
                <li>Special thanks to the creators of GeoGuessr and DALL-E 2 (OpenAI)</li>
            </ul>
            <p>
                <strong>Current image count:</strong>
            </p>
            <ul>
                <li>Standard rounds: {mapset.length} (each round has ~4 image variations)</li>
                <li>Funky rounds: {mapsetFunky.length}</li>
            </ul>
        </div>
    </div>
</div>
