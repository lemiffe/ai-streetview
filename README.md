# This Street View Does Not Exist

TODO: Write documentation

## Get started

Install the dependencies...

```bash
npm install
```

...then start [Rollup](https://rollupjs.org):

```bash
npm run dev
```

Navigate to [localhost:8080](http://localhost:8080). You should see your app running. Edit a component file in `src`, save it, and reload the page to see your changes.

## Building and running in production mode

To create an optimised version of the app:

```bash
npm run build
```

You can run the newly built app with `npm run start`. This uses [sirv](https://github.com/lukeed/sirv), which is included in your package.json's `dependencies` so that the app will work when you deploy to platforms like [Heroku](https://heroku.com).

## Using TypeScript

This template comes with a script to set up a TypeScript development environment, you can run it immediately after cloning the template with:

```bash
node scripts/setupTypeScript.js
```

Or remove the script via:

```bash
rm scripts/setupTypeScript.js
```

If you want to use `baseUrl` or `path` aliases within your `tsconfig`, you need to set up `@rollup/plugin-alias` to tell Rollup to resolve the aliases. For more info, see [this StackOverflow question](https://stackoverflow.com/questions/63427935/setup-tsconfig-path-in-svelte).

## Development

An example of modifying the map with reactive syntax (instead of onclick handler):

```javascript
$: if (markerLayers && map) {
    if (eye) {
        markerLayers.addTo(map);
    } else {
        markerLayers.remove();
    }
}

$: if (lineLayers && map) {
    if (lines) {
        lineLayers.addTo(map);
    } else {
        lineLayers.remove();
    }
}
```

## Deploying to GH Pages

```bash
npm run build
git add .
git commit -m "deploy"
git push origin gh-pages

# Deploy the code with the gh-pages module
node ./gh-pages.js
```

## Task List

- Bugfix: Map disappears when screen too small (column should collapse / boostrap!)
- Bugfix: Try to keep the images in the carousel the same height as the map (when resizing)... min-height?
- Larger max container width (bootstrap override)
- Optimise images (jpg instead of png?)
- Splash screen
- End game screen
- Timer (per game) + stop at endGame()
- Sounds
- Button to share final results / score (twitter)
- Verify if Math.round is correct or switch to floor/ceil (depending on max points, etc.)
