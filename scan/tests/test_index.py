from django.shortcuts import reverse
from django.test import TestCase


class IndexViewTests(TestCase):
    databases = {"default", "java_wallet"}

    def test_ok(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blockchain Explorer</title>")
        self.assertContains(response, "Latest Blocks")
        self.assertContains(response, "Transactions")
        self.assertContains(response, "View all blocks")
        self.assertContains(response, "View all transactions")
        self.assertContains(response, "Pending transactions")
        self.assertContains(response, "BURST-D372-C2DU-HMKK-CQLHA")
        self.assertContains(response, "BurstScan")
        self.assertQuerysetEqual(response.context["blocks"], [])
        self.assertQuerysetEqual(response.context["txs"], [])
        # TODO: mock
        # self.assertQuerysetEqual(response.context['txs_pending'], [])
