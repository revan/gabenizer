#!/bin/python2
# Script that replies to username mentions.
import praw

import time
import os
import cPickle
import sys
import traceback

from urlparse import urlparse

import gabenizer

KEY_PHRASE = 'have at you'

REDDIT_USER = os.environ['REDDIT_USER']
REDDIT_PASSWORD = os.environ['REDDIT_PASSWORD']
URL_STATIC = os.environ['URL_STATIC']

donefile = os.path.join(os.environ['OPENSHIFT_DATA_DIR'],'processed_mentions.p')
already_done = set()
try:
    already_done = cPickle.load(open(donefile, 'rb'))
except:
    pass

r = praw.Reddit('gabenizer')
r.login(REDDIT_USER, REDDIT_PASSWORD)

mentions = r.get_mentions()

def reply_failure(mention):
    mention.reply("Couldn't find any faces.\n\n***\n\n[More?](http://www.reddit.com/r/gentlemangabers) I am a bot. [Github!](https://github.com/revan/gabenizer)")

for mention in mentions:
    if mention.submission.url in already_done:
        continue
    already_done.add(mention.submission.url)

    if not KEY_PHRASE in mention.body.lower():
        continue

    # get only valid images
    url = ''
    parsed_url = urlparse(mention.submission.url)
    if parsed_url.netloc == 'imgur.com':
        # is album or framed page
        if parsed_url.path.split('/')[1]=='a':
            # is album, skip
            reply_failure(mention)
            continue
        else:
            url = parsed_url.geturl()+'.jpg'
    elif parsed_url.netloc == 'i.imgur.com':
        # is image file
        url = parsed_url.geturl()
    print url

    if url == '':
        reply_failure(mention)
        continue

    try:
        image = gabenizer.process_image(url, os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'gabenface.png'))
        filename = str(time.time())+'gabenized.png'
        imgururl = gabenizer.imgur_upload(image, os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'pics'), filename, 'gabenizer comment', URL_STATIC)

        # comment link
        mention.reply("[Praise be Gaben.](%s)\n\n***\n\n[More?](http://www.reddit.com/r/gentlemangabers) I am a bot. [Github!](https://github.com/revan/gabenizer)" % imgururl)

    except:
        traceback.print_exc()
        reply_failure(mention)
        continue

# save list of processed URLs to disk
cPickle.dump(already_done, open(donefile, 'wb'))
