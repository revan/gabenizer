import time
import praw
import unirest
import urllib, cStringIO
from urlparse import urlparse
from pprint import pprint
from PIL import Image
from config import SUBREDDIT, IMGUR_ID, IMGUR_SECRET, SKYBIO_ID, SKYBIO_SECRET

r = praw.Reddit('gabenizer bot')
#r.login()
already_done = []

#while True:

submissions = r.get_subreddit(SUBREDDIT).get_hot(limit=10)

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
	
	if url == '':
		continue

	#detect face, get x,y
	response = unirest.get('http://api.skybiometry.com/fc/faces/detect.json'
			+'?api_key='+SKYBIO_ID
			+'&api_secret='+SKYBIO_SECRET
			+'&detector=aggressive'
			+'&attributes=none'
			+'&urls='+url)
	pprint(vars(response))

	photos = response.body['photos']
	for photo in photos:
		try:
			#get image values
			original_roll = photo['tags'][0]['roll']
			original_center_x = photo['tags'][0]['center']['x']
			original_center_y = photo['tags'][0]['center']['y']
			original_size = photo['tags'][0]['width']
			original_height = photo['height']
			original_width = photo['width']

			#hardcoded values for gaben
			gaben_roll = -1
			gaben_center_x = 47.02
			gaben_center_y = 59.28
			gaben_size = 51.76
			gaben_height = 663
			gaben_width = 655

			#calculate values for scale and position
			scale = (original_size * original_width) / (gaben_size * gaben_width)
			scale_height = gaben_height * scale
			scale_width = gaben_width * scale
			place_x = (0.01 * original_center_x * original_width) - (0.01 * gaben_center_x * scale_width)
			place_y = (0.01 * original_center_y * original_height) - (0.01 * gaben_center_y * scale_height)

			print scale
			print scale_height
			print scale_width
			print place_x
			print place_y

			#open images
			original = Image.open(cStringIO.StringIO(urllib.urlopen(url).read()))
			gaben = Image.open('gaben.png')

			#rotate gaben to match roll
			gaben = gaben.rotate(int(-1*original_roll))

			#resize gaben
			gaben = gaben.resize((int(scale_width), int(scale_height)))

			gabenized = original.copy()
			gabenized.paste(gaben, (int(place_x), int(place_y)), gaben)
			gabenized.save(str(time.time())+'gabenized.png')
		except:
			continue

