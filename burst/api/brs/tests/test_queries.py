from unittest import TestCase

from burst.api.exceptions import ClientException, APIException
from burst.api.brs.queries import (
    QueryBase,
    GetPeers,
)


class QueryBaseTest(TestCase):
    def test_abc(self):
        self.assertEqual(
            getattr(QueryBase, '__abstractmethods__'),
            frozenset({'_request_type'}))


class TestQuery(QueryBase):
    _request_type = 'Test'


class TestQueryTest(TestCase):
    def test_repr(self):
        self.assertEqual(
            str(TestQuery()), 'Test')

    def test_request_type(self):
        self.assertEqual(
            TestQuery().request_type, 'Test')

    def test_params_validated(self):
        class Temp(TestQuery):
            _required_params = {'test'}

        with self.assertRaises(ClientException) as em:
            Temp()

        self.assertEqual(
            str(em.exception),
            "Omitted required params: {'test'}"
        )


class TestQueryValidateParamsTest(TestCase):
    def test_empty_all(self):
        TestQuery()

    def test_required_ok(self):
        class Temp(TestQuery):
            _required_params = {'test'}

        Temp({'test': 'a'})

    def test_required_optional_ok(self):
        class Temp(TestQuery):
            _required_params = {'test'}
            _optional_params = {'b'}

        Temp({'test': 'a', 'b': 'c'})

    def test_required_omitted(self):
        class Temp(TestQuery):
            _required_params = {'test'}

        with self.assertRaises(ClientException) as em:
            Temp()

        self.assertEqual(
            str(em.exception),
            "Omitted required params: {'test'}"
        )

    def test_unknown_params_empty_required_optional(self):
        with self.assertRaises(ClientException) as em:
            TestQuery({'test': 'a'})

        self.assertEqual(
            str(em.exception),
            "Unknown params: {'test'}"
        )

    def test_unknown_params_empty_optional(self):
        class Temp(TestQuery):
            _required_params = {'test'}

        with self.assertRaises(ClientException) as em:
            Temp({'test': 'a', 'b': 'c'})

        self.assertEqual(
            str(em.exception),
            "Unknown params: {'b'}"
        )

    def test_unknown_params(self):
        class Temp(TestQuery):
            _required_params = {'test'}
            _optional_params = {'q'}

        with self.assertRaises(ClientException) as em:
            Temp({'test': 'a', 'b': 'c'})

        self.assertEqual(
            str(em.exception),
            "Unknown params: {'b'}"
        )


class TestQueryValidateResponseTest(TestCase):
    def test_empty_schema(self):
        self.assertTrue(TestQuery().validate_response({'a': 'b'}))

    def test_ok(self):
        class Temp(TestQuery):
            _json_schema = {
                "type": "array",
                "items": {"type": "string"}
            }

        self.assertTrue(Temp().validate_response(['a', 'b']))

    def test_fail(self):
        class Temp(TestQuery):
            _json_schema = {
                "type": "array",
                "items": {"type": "string"}
            }

        with self.assertRaises(APIException) as em:
            Temp().validate_response({'a': 'b'})

        self.assertIn('malformed_data', str(em.exception))
        self.assertIn("is not of type 'array'", str(em.exception))


class GetPeersTest(TestCase):
    def test_ok(self):
        self.assertEqual(GetPeers().request_type, 'getPeers')
        self.assertTrue(GetPeers().validate_response({
            "peers": ["8.8.8.8"],
            "requestProcessingTime": 0,
        }))
