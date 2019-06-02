from django.test import TestCase


class SearchTests(TestCase):
    def test_empty_nothing_found(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nothing found")
        self.assertEqual(response.context['submit'], "Search")

    def test_wrong_nothing_found(self):
        response = self.client.get('/search/?q=abc')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nothing found")
        self.assertEqual(response.context['submit'], "Search")
