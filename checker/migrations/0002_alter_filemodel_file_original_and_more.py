# Generated by Django 4.1.5 on 2023-01-05 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemodel',
            name='file_original',
            field=models.FileField(blank=True, null=True, upload_to='test_files/', verbose_name='File'),
        ),
        migrations.AlterField(
            model_name='filemodel',
            name='file_test',
            field=models.FileField(blank=True, null=True, upload_to='test_files/', verbose_name='File'),
        ),
    ]
