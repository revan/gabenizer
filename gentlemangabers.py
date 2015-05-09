#!/bin/python2
# The script that handles all reddit interactions.
import praw
#from praw.handlers import MultiprocessHandler
#handler = MultiprocessHandler()

import time
import os
import cPickle
import sys
import traceback

from urlparse import urlparse
from pprint import pprint
from PIL import Image, ImageStat

import gabenizer

SUBREDDIT = os.environ['SUBREDDIT']
SUBREDDIT_SUBMIT = os.environ['SUBREDDIT_SUBMIT']
REDDIT_USER = os.environ['REDDIT_USER']
REDDIT_PASSWORD = os.environ['REDDIT_PASSWORD']
URL_STATIC = os.environ['URL_STATIC']

donefile = os.path.join(os.environ['OPENSHIFT_DATA_DIR'],'already_done.p')
already_done = []
try:
    already_done = cPickle.load(open(donefile, 'rb'))
except:
    pass

r = praw.Reddit('gabenizer')
submissions = r.get_subreddit(SUBREDDIT).get_hot(limit=5)
r.login(REDDIT_USER, REDDIT_PASSWORD)

for pic in submissions:
    # get only valid images
    url = ''
    parsed_url = urlparse(vars(pic)['url'])
    if parsed_url.netloc == 'imgur.com':
        # is album or framed page
        if parsed_url.path.split('/')[1]=='a':
            # is album, skip
            continue
        else:
            url = parsed_url.geturl()+'.jpg'
    elif parsed_url.netloc == 'i.imgur.com':
        # is image file
        url = parsed_url.geturl()
    print url

    if (url in already_done) or (url == ''):
        continue
    already_done.append(url)

    try:
        image = gabenizer.process_image(url, os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'gabenface.png'))
        title = vars(pic)['title']
        filename = str(time.time())+'gabenized.png'
        imgururl = gabenizer.imgur_upload(image, os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'pics'), filename, title, URL_STATIC)

        # submit link to reddit
        submission = r.submit(SUBREDDIT_SUBMIT, title, url=imgururl)

        submission.add_comment('[Source](' + vars(pic)['permalink'] + ')')

    except:
        traceback.print_exc()
        continue

# save list of processed URLs to disk
cPickle.dump(already_done, open(donefile, 'wb'))
