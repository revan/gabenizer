import time
import praw
import unirest
from urlparse import urlparse
from pprint import pprint
from config import SUBREDDIT, IMGUR_ID, IMGUR_SECRET, SKYBIO_ID, SKYBIO_SECRET

r = praw.Reddit('gabenizer bot')
#r.login()
already_done = []

#while True:

submissions = r.get_subreddit(SUBREDDIT).get_hot(limit=2)

for pic in submissions:
	#get only 
	url = ''
	parsed_url = urlparse(vars(pic)['url'])
	if parsed_url.netloc == 'imgur.com':
		#is album or framed page
		if parsed_url.path.split('/')[1]=='a':
			#is album, skip
			continue
		else:
			url = parsed_url.geturl()+'.jpg'
	elif parsed_url.netloc == 'i.imgur.com':
		#is image file
		url = parsed_url.geturl()
	print url
	
	if url in already_done:
		continue
	already_done.append(url)
	
	#detect face, get x,y
	response = unirest.get('http://api.skybiometry.com/fc/faces/detect.json'
			+'?api_key='+SKYBIO_ID
			+'&api_secret='+SKYBIO_SECRET
			+'&detector=aggressive'
			+'&attributes=none'
			+'&urls='+url)
	print response
	pprint(vars(response))

	#image manipulation
