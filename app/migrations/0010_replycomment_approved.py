# Generated by Django 4.2.7 on 2023-11-14 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_rename_reply_comment_replycomment_comment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='replycomment',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
