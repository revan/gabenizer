#gabenizer bot
This is a reddit bot which crawls a specified subreddit for its top photos, runs them through
[facial detection](http://skybiometry.com/), and attempts to replace every face with
[Gabe Newell's](http://en.wikipedia.org/wiki/Gabe_Newell).

![alt text](https://raw.github.com/revansopher/gabenizer/master/gaben.png "Our Lord and Savior")

His face is scaled and rotated to match the size of the target.
If the source image is in grayscale, the output is filtered as well.

![alt text](https://raw.github.com/revansopher/gabenizer/master/demo.png "A demo image")

See it in action [here!](http://www.reddit.com/r/gentlemangabers)

##TODO

	-If skintones don't match, apply color filter
    -Direct upload to imgur instead of by URL

Notes for running: this project is designed to run on [OpenShift](https://www.openshift.com/).
`ssh` into the deployed instance to set the environment variables for API keys and reddit account.

If using a new reddit account, the spam filters will lock out your bot.
Manually post and upvote some material until it stops prompting for CAPTCHAs on every post.
