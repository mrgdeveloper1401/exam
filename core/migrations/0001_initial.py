# Generated by Django 5.2.1 on 2025-05-27 09:27

import core.validation
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('is_deleted', models.BooleanField(default=None, editable=False, null=True)),
                ('deleted_at', models.DateTimeField(default=None, editable=False, null=True)),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('image', models.ImageField(height_field='height', help_text='max size is 1 MG', upload_to='images/%Y/%m/%d', validators=[core.validation.validate_image_size], width_field='width')),
                ('width', models.IntegerField(blank=True, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('file_size', models.PositiveIntegerField(blank=True, help_text='file size as xx.b', null=True)),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
                'db_table': 'image',
                'ordering': ('-created_at',),
            },
        ),
    ]
