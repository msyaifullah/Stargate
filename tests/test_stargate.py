import re
import os
import glob

import datetime
import jwt
import json
import pydash
import logging
import unittest

from mock import Mock
from mock import patch
from mock import MagicMock


class TestStargate(unittest.TestCase):

    # initialization logic for the test suite declared in the test module
    # code that is executed before all tests in one test run
    @classmethod
    def setUpClass(cls):
        pass
        # clean up logic for the test suite declared in the test module

    # code that is executed after all tests in one test run
    @classmethod
    def tearDownClass(cls):
        pass
        # initialization logic

    # code that is executed before each test
    def setUp(self):
        pass
        # clean up logic

    # code that is executed after each test
    def tearDown(self):
        pass
        # test method

    def camel_to_snake(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def camel_to_snake_upper(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).upper()

    def test_equal_validator_validate(self):
        from stargate.authentication import Authentication
        makan = True

        mm = Authentication()
        print(mm.set_password('123456', 10))

        self.assertEqual(makan, True)

    def test_equal_is_password(self):
        from stargate.authentication import Authentication
        m = '$2b$10$5eTcbolJokO2aj309mJIhuSn3.gz/AUx67x29jquDWMu71X4JihsW'
        n = '$2b$10$aqqSjRDLLj4T2ioUZ76diO6B.Gj7Y.afHjTGIbbbOsFnG10xSH6va'

        self.assertEqual(Authentication().is_password(m, '123456'), True)
        self.assertEqual(Authentication().is_password(n, '123456'), True)

    def test_equal_generate_token(self):
        from stargate.base import Startgate

        token = Startgate().encode_auth_token(secret='123456', user_id='12345', sender_id='sender-1234', recipients_id='recipients-1234')
        response_auth = Startgate().decode_auth_token(secret='123456', auth_token=token[1], recipients_id='recipients-1234')
        print(response_auth)

    def test_generate_dict(self):
        expiration = 3600
        user_id = 'user-12345'
        sender_id = ''
        recipients_id = 'recipient-12345'

        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration),  # (expiration time)
            'iat': datetime.datetime.utcnow(),  # (issued at)
            'sub': user_id,  # (subject)
        }

        if sender_id is not None:
            payload['iss'] = sender_id  # (issuer)

        if recipients_id is not None:
            payload['aud'] = recipients_id  # (audience)

        print(payload)

    def test_generate(self):
        from stargate.base import _jwt_decode
        from stargate.base import _jwt_encode

        payload, token = _jwt_encode(secret='123456', user_id='12345', sender_id='sender-1234', recipients_id='recipients-1234')
        try:
            decoded_payload = _jwt_decode(secret='123456', auth_token=token, recipients_id='recipients-1234')
        except jwt.InvalidAudience:
            print "error this invalid audience"
        except jwt.ExpiredSignature:
            print "error this signature"
        except jwt.InvalidIssuer:
            print "invalid issuer"
        except Exception, e:
            print("error")
            print(e.message)

        print(payload)
        print(token)
        print(decoded_payload)



    # runs the unit tests in the module
