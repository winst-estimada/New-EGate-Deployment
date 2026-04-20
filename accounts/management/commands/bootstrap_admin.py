import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create or update a frontend-usable admin account from environment variables."

    def handle(self, *args, **options):
        username = (os.environ.get("BOOTSTRAP_ADMIN_USERNAME") or "").strip()
        password = os.environ.get("BOOTSTRAP_ADMIN_PASSWORD") or ""
        email = (os.environ.get("BOOTSTRAP_ADMIN_EMAIL") or "").strip()

        if not username:
            raise CommandError("BOOTSTRAP_ADMIN_USERNAME is required.")
        if not password:
            raise CommandError("BOOTSTRAP_ADMIN_PASSWORD is required.")

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_active": True,
                "is_staff": True,
                "is_superuser": False,
                "is_admin": True,
                "is_gate_operator": False,
                "is_resident": False,
            },
        )

        user.email = email
        user.is_active = True
        user.is_staff = True
        user.is_superuser = False
        user.is_admin = True
        user.is_gate_operator = False
        user.is_resident = False
        user.set_password(password)
        user.save()

        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} bootstrap admin '{username}'"))

