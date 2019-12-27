from django.test import TestCase


class AccountListViewTests(TestCase):
    databases = {"default", "java_wallet"}

    def test_slash_redirect(self):
        response = self.client.get("/accounts")
        self.assertEqual(response.status_code, 301)

    def test_ok(self):
        response = self.client.get("/accounts/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Top accounts by Burst balance")
        self.assertContains(response, "Blockchain Explorer - Top accounts</title>")
        self.assertQuerysetEqual(response.context["accounts"], [])


class AddressDetailViewTests(TestCase):
    databases = {"default", "java_wallet"}

    def test_404(self):
        response = self.client.get("/address/abc")
        self.assertEqual(response.status_code, 404)
