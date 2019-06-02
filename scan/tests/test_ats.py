from django.test import TestCase


class AtListViewTests(TestCase):
    databases = {'default', 'java_wallet'}

    def test_slash_redirect(self):
        response = self.client.get('/ats')
        self.assertEqual(response.status_code, 301)

    def test_ok(self):
        response = self.client.get('/ats/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ATs found')
        self.assertQuerysetEqual(response.context['ats'], [])


class AtDetailViewTests(TestCase):
    databases = {'default', 'java_wallet'}

    def test_404(self):
        response = self.client.get('/at/abc')
        self.assertEqual(response.status_code, 404)
