#!/bin/python3

import logging

import reddit
import gabenizer

fetcher = reddit.SubredditFetcher()
submitter = reddit.LinkSubmitter()


def main():
    for post in fetcher.get_unprocessed_posts():
        try:
            uploaded_url = gabenizer.process_image(post.url, post.title)

            submitter.post_link(
                url=uploaded_url,
                title=post.title,
                source=post.permalink,
            )
        except Exception:
            logging.exception('Error while processing %s:' % post.url)


if __name__ == '__main__':
    main()
