# Generated by Django 5.2.1 on 2025-05-27 10:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_otp_device_ip'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('is_deleted', models.BooleanField(default=None, editable=False, null=True)),
                ('deleted_at', models.DateTimeField(default=None, editable=False, null=True)),
                ('student_number', models.CharField(blank=True, max_length=11)),
                ('student_image', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='student_image', to='core.image')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'student',
                'ordering': ('-created_at',),
            },
        ),
    ]
