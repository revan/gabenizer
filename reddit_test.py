import os
import unittest

import api_module
import reddit


class SubredditFetcherTest(unittest.TestCase):

    def setUp(self):
        api_module.use_mocks = True

    def test_filters_already_processed(self):
        fetcher = reddit.SubredditFetcher()

        unprocessed = fetcher.get_unprocessed_posts(
            target_subreddit='target_subreddit',
            our_subreddit='our_subreddit',
            limit_target=5,
            limit_ours=3,
        )

        self.assertEqual(
            [p.title for p in unprocessed],
            ['Fake 3', 'Fake 4'],
        )

    def test_no_results(self):
        fetcher = reddit.SubredditFetcher()

        self.assertEqual(
            fetcher.get_unprocessed_posts(
                target_subreddit='target_subreddit',
                our_subreddit='our_subreddit',
                limit_target=5,
                limit_ours=10,
            ),
            [],
        )

    def test_normalize_url_noop(self):
        self.assertEqual(
            reddit.SubredditFetcher._get_normalized_url_or_none('https://i.imgur.com/example.jpg'),
            'https://i.imgur.com/example.jpg'
        )

    def test_normalize_url_handles_imgur_page(self):
        self.assertEqual(
            reddit.SubredditFetcher._get_normalized_url_or_none('https://imgur.com/example'),
            'https://imgur.com/example.png'
        )

    def test_normalize_url_rejects_album(self):
        self.assertIsNone(
            reddit.SubredditFetcher._get_normalized_url_or_none('https://imgur.com/a/example'),
        )

    def test_normalize_url_rejects_non_imgur(self):
        self.assertIsNone(
            reddit.SubredditFetcher._get_normalized_url_or_none('https://notimgur.com/example.png'),
        )


if __name__ == '__main__':
    unittest.main()
