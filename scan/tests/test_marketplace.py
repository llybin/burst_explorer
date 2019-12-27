from django.test import TestCase


class MarketPlaceListViewTests(TestCase):
    databases = {"default", "java_wallet"}

    def test_slash_redirect(self):
        response = self.client.get("/mps")
        self.assertEqual(response.status_code, 301)

    def test_ok(self):
        response = self.client.get("/mps/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "goods found")
        self.assertContains(response, "Blockchain Explorer - Market Place</title>")
        self.assertQuerysetEqual(response.context["goods"], [])


class MarketPlaceDetailViewTests(TestCase):
    databases = {"default", "java_wallet"}

    def test_404(self):
        response = self.client.get("/mp/abc")
        self.assertEqual(response.status_code, 404)
