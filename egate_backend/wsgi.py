"""
WSGI config for egate_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

settings_module = 'egate_backend.deployment_settings' if 'RENDER_EXTERNAL_HOSTNAME' in os.environ else 'egate_backend.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()

if os.environ.get('DJANGO_CREATE_SUPERUSER_ON_START', 'false').strip().lower() == 'true':
    try:
        from django.contrib.auth import get_user_model

        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if password:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username=username, email=email, password=password)
                print('Created superuser from environment variables.')
            else:
                print(f'Superuser with username "{username}" already exists. Skipping creation.')
        else:
            print('DJANGO_SUPERUSER_PASSWORD is not set; superuser creation skipped.')
    except Exception as exc:
        print('Failed to create superuser on startup:', exc)
