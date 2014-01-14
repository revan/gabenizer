import praw
import unirest
import requests
import time, urllib, cStringIO, os, cPickle, sys
from urlparse import urlparse
from pprint import pprint
from PIL import Image, ImageStat
#from config import SUBREDDIT, SKYBIO_ID, SKYBIO_SECRET, REDDIT_USER, REDDIT_PASSWORD, SUBREDDIT_SUBMIT, IMGUR_KEY, IMGUR_DELETE, URL_STATIC
SUBREDDIT = os.environ['SUBREDDIT']
SKYBIO_ID = os.environ['SKYBIO_ID']
SKYBIO_SECRET = os.environ['SKYBIO_SECRET']
REDDIT_USER = os.environ['REDDIT_USER']
REDDIT_PASSWORD = os.environ['REDDIT_PASSWORD']
SUBREDDIT_SUBMIT = os.environ['SUBREDDIT_SUBMIT']
IMGUR_KEY = os.environ['IMGUR_KEY']
IMGUR_DELETE = os.environ['IMGUR_DELETE']
URL_STATIC = os.environ['URL_STATIC']

donefile = os.path.join(os.environ['OPENSHIFT_DATA_DIR'],'already_done.p')
already_done = []
try:
	already_done = cPickle.load(open(donefile, 'rb'))
except:
	pass

r = praw.Reddit('gabenizer bot')
submissions = r.get_subreddit(SUBREDDIT).get_hot(limit=8)
r.login(REDDIT_USER, REDDIT_PASSWORD)

for pic in submissions:
	#get only valid images
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
	
	if (url in already_done) or (url == ''):
		continue
	already_done.append(url)
	

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
		#try:
		original = Image.open(cStringIO.StringIO(urllib.urlopen(url).read()))
		gabenized = original.copy()
		if not photo['tags']:
			continue
		for face in photo['tags']:
			#get image values
			original_roll = face['roll']
			original_yaw = face['yaw']
			original_center_x = face['center']['x']
			original_center_y = face['center']['y']
			original_size = face['width']
			original_height = photo['height']
			original_width = photo['width']

			#if yaw is too great, skip
			MAX_YAW = 40
			if abs(original_yaw) > MAX_YAW:
				continue

			#hardcoded values for gabenface
			gaben_roll = -1
			gaben_center_x = 51.24
			gaben_center_y = 47.53
			gaben_size = 67.15
			gaben_height = 465
			gaben_width = 484

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

			#open image
			gaben = Image.open(os.path.join(os.environ['OPENSHIFT_REPO_DIR'],'gabenface.png'))

			#rotate gaben to match roll
			gaben = gaben.rotate(int(-1*original_roll))

			#resize gaben
			gaben = gaben.resize((int(scale_width), int(scale_height)))

			gabenized.paste(gaben, (int(place_x), int(place_y)), gaben)
			unprocessed = 0
		if unprocessed:
			continue

		#arrange both images
		final = Image.new("RGB", (original_width * 2, original_height))
		final.paste(original, (0,0))
		final.paste(gabenized, (original_width, 0))

		#if original image was grayscale, convert final
		COLOR_CUTOFF = 100
		colors = ImageStat.Stat(original).var
		if len(colors) == 3 and abs(max(colors) - min(colors))<COLOR_CUTOFF:
			final = final.convert('L')

		#save image and thumbnail
		filename = str(time.time())+'gabenized.png'
		final.save(os.path.join(os.environ['OPENSHIFT_DATA_DIR'],'pics',filename))
		final.thumbnail((800, 400))
		final.save(os.path.join(os.environ['OPENSHIFT_DATA_DIR'],'thumbs',filename))

		#upload to imgur
		dataupload = {
			'image' : URL_STATIC+filename,
			'type' : 'URL',
			'name' : filename,
			'title' : vars(pic)['title'],
			'album' : IMGUR_DELETE
		}
		url = 'https://api.imgur.com/3/image'
		headers = {'Authorization' : 'Client-ID '+IMGUR_KEY}
		req = requests.post(url, data=dataupload, headers=headers)
		imgururl = req.json()['data']['link']
		print imgururl

		#submit link to reddit
		r.submit(SUBREDDIT_SUBMIT, vars(pic)['title'], url=imgururl)

		#except:
		#	print 'Exception: ', sys.exc_info()[0]
		#	continue

#save list of processed URLs to disk
cPickle.dump(already_done, open(donefile, 'wb'))

