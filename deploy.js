var ghpages = require('gh-pages');

ghpages.publish(
    'public', // path to public directory
    {
        branch: 'gh-pages',
        repo: 'https://github.com/lemiffe/ai-streetview.git',
        user: {
            name: 'lemiffe',
            email: 'lemiffe@lemiffe.com'
        }
    },
    () => {
        console.log('Deploy Complete!')
    }
)
