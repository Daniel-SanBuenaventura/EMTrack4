import logging

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

PASSWORD = (
    "pbkdf2_sha256$100000$C6QcTM4eQ33l$jS1fWJjqXzbmRBSF0hjeJKiRqIlEapMYwcq5GsqfYbc="
)
#  This is a sample user. You can edit this line or add a new one with “last_name first_name email"
USERS = '''\
Receiver Admin admin@admin.com
'''.strip().split(
    '\n'
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        self._create_user_accounts()

    @staticmethod
    def _create_user_accounts():
        users = (line.split() for line in USERS)
        for last_name, first_name, email in users:
            email = email.lower()
            user, created = User.objects.get_or_create(
                username=email,
                defaults=dict(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=PASSWORD,
                    is_staff=True,
                    is_superuser=True,
                ),
            )
            logger.info(f'{user} {"created" if created else "already created"}')
