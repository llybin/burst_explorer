import datetime

from django.forms.models import model_to_dict
from django.test import TestCase


class PeersChartsViewTests(TestCase):
    fixtures = ['peers']

    def test_slash_redirect(self):
        response = self.client.get('/peers-charts')
        self.assertEqual(response.status_code, 301)

    def test_ok(self):
        response = self.client.get('/peers-charts/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Online now')
        self.assertEqual(response.context['online_now'], 3)
        self.assertEqual(len(response.context['versions']), 2)
        self.assertEqual(response.context['versions'][0], {'version': '2.3.0', 'cnt': 2})
        self.assertEqual(response.context['versions'][1], {'version': 'v2.4.0', 'cnt': 1})
        self.assertEqual(len(response.context['countries']), 2)
        self.assertEqual(response.context['countries'][0], {'country_code': 'US', 'cnt': 2})
        self.assertEqual(response.context['countries'][1], {'country_code': 'DE', 'cnt': 1})
        self.assertEqual(len(response.context['states']), 5)
        self.assertEqual(response.context['states'][0], {'state': 'online', 'cnt': 3})
        self.assertEqual(response.context['states'][1], {'state': 'unreachable', 'cnt': 1})
        self.assertEqual(response.context['states'][2], {'state': 'in sync', 'cnt': 1})
        self.assertEqual(response.context['states'][3], {'state': 'stuck', 'cnt': 1})
        self.assertEqual(response.context['states'][4], {'state': 'forked', 'cnt': 1})
        self.assertEqual(
            response.context['last_check'],
            {'modified_at': datetime.datetime(2019, 7, 10, 16, 28, 42, 333593)})


class PeersListViewTests(TestCase):
    fixtures = ['peers']

    def test_slash_redirect(self):
        response = self.client.get('/peers')
        self.assertEqual(response.status_code, 301)

    def test_ok(self):
        response = self.client.get('/peers/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'peers found')
        self.assertEqual(len(response.context['peers']), 7)


class PeerDetailViewTests(TestCase):
    fixtures = ['peers']

    def test_404(self):
        response = self.client.get('/peer/abc')
        self.assertEqual(response.status_code, 404)

    def test_ok(self):
        response = self.client.get('/peer/burst.sagichdir.net')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Last Online')
        self.assertDictEqual(
            model_to_dict(response.context['peer']),
            {'announced_address': 'burst.sagichdir.net',
             'application': 'BRS',
             'availability': 100.0,
             'country_code': 'DE',
             'cumulative_difficulty': '64762191462137382682',
             'downtime': 0,
             'height': 641085,
             'last_online_at': datetime.datetime(2019, 7, 10, 16, 28, 33, 628425),
             'lifetime': 17,
             'platform': 'BURST-QKWB-QWSX-8K2F-3NQ9T',
             'state': 1,
             'version': 'v2.4.0'
             })
