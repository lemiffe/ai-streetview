<script>
    export let images = [];
    let currImageIndex = 0;

    export const reset = () => {
        currImageIndex = 0;
    };

    const next = () => {
        currImageIndex = (currImageIndex + 1) % images.length;
    };
    const previous = () => {
        if (currImageIndex > 0) {
            currImageIndex = (currImageIndex - 1) % images.length;
        } else {
            currImageIndex = images.length - 1;
        }
    };
</script>

<div id="carousel" class="carousel slide" data-ride="carousel">
    <div class="carousel-inner">
        {#each images as image, i}
            <div id="carousel-images" class="carousel-item" class:active={i === currImageIndex}>
                <img class="d-block w-100" src="game/{image}" alt="Generated Image {i + 1}" />
            </div>
        {/each}
    </div>
    <!-- svelte-ignore a11y-invalid-attribute -->
    <a class="carousel-control-prev" href="#" role="button" data-slide="prev" on:click={previous}>
        <span class="carousel-control-prev-icon" aria-hidden="true" />
        <span class="sr-only" />
    </a>
    <!-- svelte-ignore a11y-invalid-attribute -->
    <a class="carousel-control-next" href="#" role="button" data-slide="next" on:click={next}>
        <span class="carousel-control-next-icon" aria-hidden="true" />
        <span class="sr-only" />
    </a>
</div>
