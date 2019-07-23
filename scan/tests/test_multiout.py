from django.test import TestCase

from scan.multiout import (
    aggregate_greater_height,
    find_last_actual_aggr_block,
    group_list,
)


class MultiOutListViewTests(TestCase):
    databases = {'default', 'java_wallet'}

    def test_slash_redirect(self):
        response = self.client.get('/mos')
        self.assertEqual(response.status_code, 301)

    def test_ok(self):
        response = self.client.get('/mos/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'transactions found')
        self.assertContains(response, 'Blockchain Explorer - MultiOut</title>')
        self.assertQuerysetEqual(response.context['mos'], [])


class MultiOutAggrTests(TestCase):
    databases = {'default', 'java_wallet'}

    def test_aggregate_greater_height(self):
        # just call todo after fixtures
        self.assertIsNone(aggregate_greater_height(0))

    def test_find_last_actual_aggr_block(self):
        # just call todo after fixtures
        self.assertEqual(find_last_actual_aggr_block(0), 0)

    def test_group_list(self):
        self.assertTupleEqual(
            tuple(group_list([1, 2, 3, 4], 2)),
            ((1, 2), (3, 4))
        )
