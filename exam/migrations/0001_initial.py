# Generated by Django 5.2.1 on 2025-05-27 14:31

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('is_deleted', models.BooleanField(default=None, editable=False, null=True)),
                ('deleted_at', models.DateTimeField(default=None, editable=False, null=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, verbose_name='توضیحات')),
                ('time_limit', models.PositiveIntegerField()),
                ('passing_score', models.PositiveIntegerField()),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'exam',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ExamAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('is_deleted', models.BooleanField(default=None, editable=False, null=True)),
                ('deleted_at', models.DateTimeField(default=None, editable=False, null=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('is_passed', models.BooleanField(default=False)),
                ('ip_address', models.GenericIPAddressField()),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='exam.exam')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_attempts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'exam_attempt',
                'ordering': ('-start_time',),
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('is_deleted', models.BooleanField(default=None, editable=False, null=True)),
                ('deleted_at', models.DateTimeField(default=None, editable=False, null=True)),
                ('text', models.TextField()),
                ('score', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='exam.exam')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.image')),
            ],
            options={
                'db_table': 'question',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('is_deleted', models.BooleanField(default=None, editable=False, null=True)),
                ('deleted_at', models.DateTimeField(default=None, editable=False, null=True)),
                ('text', models.CharField(max_length=500, verbose_name='متن گزینه')),
                ('is_correct', models.BooleanField(default=False, verbose_name='پاسخ صحیح')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='exam.question', verbose_name='سوال')),
            ],
            options={
                'verbose_name': 'گزینه',
                'verbose_name_plural': 'گزینه\u200cها',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('is_deleted', models.BooleanField(default=None, editable=False, null=True)),
                ('deleted_at', models.DateTimeField(default=None, editable=False, null=True)),
                ('answered_at', models.DateTimeField(auto_now_add=True)),
                ('attempt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='exam.examattempt')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.option', verbose_name='گزینه انتخاب شده')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.question')),
            ],
            options={
                'db_table': 'user_answer',
                'unique_together': {('attempt', 'question')},
            },
        ),
    ]
