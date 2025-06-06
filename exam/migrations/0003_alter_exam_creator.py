# Generated by Django 5.2.1 on 2025-05-27 14:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_alter_exam_creator_alter_exam_description_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='creator',
            field=models.ForeignKey(help_text='User who created this exam', limit_choices_to={'is_staff': True, 'user_type': 'admin'}, on_delete=django.db.models.deletion.PROTECT, related_name='exam_creator', to=settings.AUTH_USER_MODEL),
        ),
    ]
