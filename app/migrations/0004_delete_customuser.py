# Generated by Django 4.2.7 on 2023-11-13 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_customuser_username_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
