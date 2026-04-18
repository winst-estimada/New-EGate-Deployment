set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate

if [ "$CREATE_SUPERUSER" = "true" ]; then
    python manage.py createsuperuser --noinput || true
    python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); u=User.objects.get(username='$DJANGO_SUPERUSER_USERNAME'); u.is_admin=True; u.is_staff=True; u.is_superuser=True; u.save()"
fi