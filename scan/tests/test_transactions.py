from django.test import TestCase


class TxListViewTests(TestCase):
    databases = {"default", "java_wallet"}

    def test_slash_redirect(self):
        response = self.client.get("/txs")
        self.assertEqual(response.status_code, 301)

    def test_ok(self):
        response = self.client.get("/txs/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "transactions found")
        self.assertContains(response, "Blockchain Explorer - Transactions</title>")
        self.assertQuerysetEqual(response.context["txs"], [])


class TxDetailViewTests(TestCase):
    databases = {"default", "java_wallet"}

    def test_404(self):
        response = self.client.get("/tx/abc")
        self.assertEqual(response.status_code, 404)
