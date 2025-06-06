# Generated by Django 5.2.1 on 2025-05-27 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_remove_otp_is_used'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(blank=True, choices=[('teacher', 'Teacher'), ('student', 'Student')], default='student', help_text='The type of user this is. admin - teacher - student', max_length=10),
        ),
    ]
