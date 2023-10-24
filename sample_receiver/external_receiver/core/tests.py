import random
from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from model_bakery import baker
from oauth2_provider.models import (
    AccessToken,
    Application,
)
from rest_framework import status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db
User = get_user_model()
TEST_SERVER_MESSAGE_URL = 'http://testserver/api/message/'
TEST_SERVER_VERIFICATION_URL = 'http://testserver/api/verification/'


@pytest.fixture
def oauth2_context():
    user = baker.make(User)
    application = baker.make(
        Application,
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_PASSWORD,
    )
    return baker.make(
        AccessToken,
        user=user,
        application=application,
        token=str(random.getrandbits(128)),
        expires=timezone.now() + timedelta(minutes=15),
        scope="read write",
    )


@pytest.fixture
def token_client(oauth2_context):
    client = APIClient()
    access_token = oauth2_context.token
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client


@pytest.fixture
def unauthorized_client():
    return APIClient()


correct_message = {
    'created': '2019-10-16T06:22:33',
    'customer': 'Test Customer',
    'license_plate': 'DWRRRR',
    'fleet_id': 'vehicle name',
    'longitude': 51.113294,
    'latitude': 17.052380,
    'event_type': 'pressure_low',
    'iso_position': 23,
    'pressure': 800000,
    'temperature': 20,
    'mileage': 3000,
    'heading': 20,
    'speed': 60,
}
empty_message = {}


def adapt_msg(key, pop_key=False, value_for_key=None):
    message = correct_message.copy()
    if key in message and pop_key:
        message.pop(key)
    if value_for_key:
        message[key] = value_for_key
    return message


wrong_datetime_format_message = adapt_msg(key='created', value_for_key='2019-10-16')
message_with_null_value = adapt_msg(
    key=random.choice(list(correct_message.keys())), value_for_key=None
)
missing_key_message = adapt_msg(
    key=random.choice(list(correct_message.keys())), pop_key=True
)
additional_key_message = adapt_msg(key='future_key', value_for_key='ABC')


@pytest.mark.parametrize(
    'msg, status_code',
    [
        (correct_message, 200),
        (message_with_null_value, 200),
        (missing_key_message, 400),
        (wrong_datetime_format_message, 400),
        (empty_message, 400),
        (additional_key_message, 200),
    ],
)
def test_post_message(msg, status_code, token_client):
    response = token_client.post(TEST_SERVER_MESSAGE_URL, data=msg)
    assert response.status_code == status_code, response.status_code


def test_if_new_key_gets_through(token_client):
    response = token_client.post(TEST_SERVER_MESSAGE_URL, data=additional_key_message)
    assert 'future_key' in response.data


def test_post_unauthorized_message_expect_401(unauthorized_client):
    response = unauthorized_client.post(TEST_SERVER_MESSAGE_URL, data=correct_message)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.status_code


def test_verify_external_receiver_expect_200(token_client):
    response = token_client.get(TEST_SERVER_VERIFICATION_URL)
    assert response.status_code == status.HTTP_200_OK, response.status_code


def test_verify_unauthorized_external_receiver_expect_401(unauthorized_client):
    response = unauthorized_client.get(TEST_SERVER_VERIFICATION_URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.status_code
