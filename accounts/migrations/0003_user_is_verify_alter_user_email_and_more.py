# Generated by Django 5.2.1 on 2025-05-25 14:17

import accounts.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_deleted_at_user_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_verify',
            field=models.BooleanField(default=False, help_text='Is this user verified?'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, validators=[accounts.validators.unique_email_in_layer_app]),
        ),
        migrations.AlterField(
            model_name='user',
            name='nation_code',
            field=models.CharField(blank=True, max_length=11, validators=[accounts.validators.unique_nation_code_in_layer_app]),
        ),
    ]
