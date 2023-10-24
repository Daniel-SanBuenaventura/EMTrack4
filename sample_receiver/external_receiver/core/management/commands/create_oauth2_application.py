import logging
import os

from django.core.management.base import BaseCommand
from oauth2_provider.models import Application

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        self._make_oauth2_application()

    @staticmethod
    def _make_oauth2_application():
        app_exists = Application.objects.exists()
        if app_exists:
            logger.info("OAuth2 app already exists")
        else:
            Application.objects.create(
                name='sample_receiver',
                client_type=Application.CLIENT_CONFIDENTIAL,
                authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
                client_id=os.environ.get('client_id') or "1234",
                client_secret=os.environ.get('client_secret') or "12345678",
            )
            logger.info("OAuth2 app created")
