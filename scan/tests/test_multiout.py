from django.test import TestCase


class MultiOutListViewTests(TestCase):
    databases = {'default', 'java_wallet'}

    def test_slash_redirect(self):
        response = self.client.get('/mos')
        self.assertEqual(response.status_code, 301)

    def test_ok(self):
        response = self.client.get('/mos/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'transactions found')
        self.assertQuerysetEqual(response.context['mos'], [])
