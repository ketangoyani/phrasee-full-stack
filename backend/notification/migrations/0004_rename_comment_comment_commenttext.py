# Generated by Django 4.2.10 on 2024-02-28 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_comment_notification_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='commentText',
        ),
    ]