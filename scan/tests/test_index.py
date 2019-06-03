from django.test import TestCase
from django.shortcuts import reverse


class IndexViewTests(TestCase):
    databases = {'default', 'java_wallet'}

    def test_ok(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Latest Blocks")
        self.assertContains(response, "View All Transactions")
        self.assertQuerysetEqual(response.context['blocks'], [])
        self.assertQuerysetEqual(response.context['txs'], [])

