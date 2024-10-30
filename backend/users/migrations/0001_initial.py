# Generated by Django 5.0.1 on 2024-01-23 18:27
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations, transaction
from os import getenv as os_getenv
from dotenv import load_dotenv

load_dotenv()


def apply_migration(apps, schema_editor):
    if os_getenv('ENV') != 'dev':
        return
    try:
        with transaction.atomic():
            Group = apps.get_model('auth', 'Group')
            groups_created = Group.objects.bulk_create([
                Group(name='admin'),
                Group(name='user'),
                
            ])
            User = apps.get_model('auth', 'User')
            users_created = User.objects.bulk_create([
                User(
                    username='admin',
                    password=make_password(settings.DEMO_SUPERUSER_PASS),
                    is_staff = True,
                    is_superuser = True
                ),
                User(
                    username='user',
                    first_name='Test',
                    last_name='User',
                    email='user@test.com',
                    password=make_password(settings.DEMO_USER_PASS)
                )
            ])
            c = 0
            for user in users_created:
                user.groups.add(groups_created[c])
                c+=1
    except transaction.TransactionManagementError:
        users_created.delete()
        groups_created.delete()
    
def revert_migration(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.filter(username__in=[
        'admin',
        'user',
        ]
    ).delete()
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=[
        'admin',
        'user',
        ]
    ).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration)
    ]