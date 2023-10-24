import logging
import os

from django.core.management.base import BaseCommand
from django.utils import timezone
from oauth2_provider.models import AccessToken

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        self._create_test_access_token()

    @staticmethod
    def _create_test_access_token():
        test_access_token = os.getenv('RECEIVER_TEST_ACCESS_TOKEN')
        if test_access_token:
            AccessToken.objects.filter(token=test_access_token).delete()
            AccessToken.objects.create(
                token=test_access_token,
                scope="read write",
                expires=timezone.now() + timezone.timedelta(minutes=30),
            )
            logger.info("AccessToken for testing purposes created.")
        else:
            logger.warning("No RECEIVER_TEST_ACCESS_TOKEN provided in env vars.")
