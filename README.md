# This Street View Does Not Exist

A small website where you can guess a location based on images where at least half of the image has been generated
by an AI generator such as DALL-E 2.

## Getting started

```bash
npm install
npm run dev # Uses Rollup
```

Navigate to [localhost:8080](http://localhost:8080). Auto-reload on changes in the src/ folder should work by default.

## Building and running in production mode

To create an optimised version of the app:

```bash
npm run build
npm run start
```

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

### Adding maps / images

- Grab a screenshot from GeoGuessr (preferrably square, around 1024x1024) containing some meta
- In Dall-E use Out Painting to paint to the right or left, make sure the generated part is at least 50% of the new image
- In "My Collection" download the 4 generated images and name then N-a to N-d.jpg and place these in the public/game directory
- Copy the lat/lon values as well as the street view URLs of each location after finishing the GeoGuessr game (click on the markers)
- Paste them in the same order as the images in the src/mapset.js file (make sure to use the correct filenames and lat/lons)

### Optimising images

- `cd scripts`
- `python convert_to_jpgs.py`
- This will convert all pngs to jpgs (and replace .png for .jpg in mapset.js)

## Deploying to GH Pages

```bash
npm run build
git add .
git commit -m "deploy"
git push origin gh-pages --force
node ./deploy.js
```
