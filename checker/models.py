from django.db import models


class FileModel(models.Model):
    file_original = models.FileField(
        upload_to='test_files/',
        null=True,
        blank=True
    )
    file_test = models.FileField(
        upload_to='test_files/',
        null=True,
        blank=True
    )
