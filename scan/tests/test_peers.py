import datetime
from unittest import mock

import vcr
from freezegun import freeze_time
from django.forms.models import model_to_dict
from django.test import TestCase

from scan.peers import (
    get_ip_by_domain,
    is_good_version,
    get_country_by_ip,
    explore_peer,
)

my_vcr = vcr.VCR(
    cassette_library_dir='scan/tests/fixtures/vcr/peers',
    record_mode='once',
    decode_compressed_response=True,
)


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


class GetIPByDomainTests(TestCase):
    def test_ok(self):
        self.assertEqual(get_ip_by_domain('1.1.1.1'), '1.1.1.1')
        self.assertEqual(get_ip_by_domain('1.1.1.1:8123'), '1.1.1.1')
        self.assertEqual(get_ip_by_domain('http://1.1.1.1'), '1.1.1.1')
        with mock.patch('scan.peers.socket.gethostbyname', return_value='2.3.4.5'):
            self.assertEqual(get_ip_by_domain('devtrue.net'), '2.3.4.5')
            self.assertEqual(get_ip_by_domain('http://devtrue.net'), '2.3.4.5')

    def test_ipv6(self):
        self.assertEqual(get_ip_by_domain('[2a02:c207:2016:1984:0:0:0:1]'), '2a02:c207:2016:1984:0:0:0:1')
        self.assertEqual(get_ip_by_domain('[2a02:c207:2016:1984:0:0:0:1]:8123'), '2a02:c207:2016:1984:0:0:0:1')
        self.assertEqual(get_ip_by_domain('http://[2a02:c207:2016:1984:0:0:0:1]'), '2a02:c207:2016:1984:0:0:0:1')

    def test_wrong(self):
        self.assertEqual(get_ip_by_domain(''), None)
        self.assertEqual(get_ip_by_domain('https://'), None)
        self.assertEqual(get_ip_by_domain('2a02:c207:2016:1984:0:0:0:1'), None)
        self.assertEqual(get_ip_by_domain('http://2a02:c207:2016:1984:0:0:0:1'), None)

    def test_short(self):
        self.assertEqual(get_ip_by_domain('1.0.0'), '1.0.0.0')


class IsGoodVersionTests(TestCase):
    def test_ok(self):
        self.assertTrue(is_good_version('2.3.0'))
        self.assertTrue(is_good_version('2.3.1'))
        self.assertTrue(is_good_version('2.4.0'))
        self.assertTrue(is_good_version('v2.4.0'))
        self.assertFalse(is_good_version('2.2.0'))

    def test_wrong(self):
        self.assertFalse(is_good_version('vvv'))
        self.assertFalse(is_good_version(''))


class GetCountryByIPTests(TestCase):
    @my_vcr.use_cassette('geoplugin_success')
    def test_ok(self):
        self.assertEqual(get_country_by_ip('8.8.8.8', _refresh=True), 'US')


class ExplorePeerTests(TestCase):
    @freeze_time('2019-07-10 17:47:6.963229', tz_offset=0)
    @my_vcr.use_cassette('explore_peer_success')
    def test_ok(self):
        updates = {}
        with mock.patch('scan.peers.get_country_by_ip', return_value='FR'):
            explore_peer('wallet.burst.devtrue.net', updates)
        self.assertDictEqual(
            updates,
            {
                'wallet.burst.devtrue.net': {
                    'announced_address': 'wallet.burst.devtrue.net',
                    'application': 'BRS',
                    'country_code': 'FR',
                    'cumulative_difficulty': '64770577730996744870',
                    'height': 641103,
                    'last_online_at': datetime.datetime(2019, 7, 10, 17, 47, 6, 963229),
                    'platform': 'BURST-BTKF-8WT9-L98N-98JH2',
                    'version': 'v2.4.0'
                }
            })

    @my_vcr.use_cassette('explore_peer_old_version')
    def test_old_version(self):
        updates = {}
        explore_peer('wallet.burst.devtrue.net', updates)
        self.assertEqual(updates, {'wallet.burst.devtrue.net': None})

    @my_vcr.use_cassette('explore_peer_error')
    def test_error(self):
        updates = {}
        explore_peer('wallet.burst.devtrue.net', updates)
        self.assertEqual(updates, {'wallet.burst.devtrue.net': None})
