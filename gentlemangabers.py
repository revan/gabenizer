#!/bin/python3

import logging

import database
import reddit
import gabenizer

db = database.Database()
fetcher = reddit.SubredditFetcher()
submitter = reddit.LinkSubmitter()


def main():
    for post in fetcher.get_recent_posts():
        try:
            if db.contains(post.url):
                continue
            uploaded_url = gabenizer.process_image(post.url, post.title)

            submitter.post_link(
                url=uploaded_url,
                title=post.title,
                source=post.permalink,
            )
            db.record_post(source_url=post.url, uploaded_url=uploaded_url)
        except Exception:
            logging.exception('Error while processing %s:' % post.url)
            db.record_failure(post.url)


if __name__ == '__main__':
    main()
