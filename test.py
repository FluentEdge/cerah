import server

from unittest import TestCase, main


class SairahWebhookTests(TestCase):

    def test_sairah_requires_correct_secret(self):
        server.pr_created('asdf')


if __name__ == '__main__':
    main()
