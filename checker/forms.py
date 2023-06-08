from checker.models import FileModel

from django.forms import ModelForm


class FileForm(ModelForm):
    class Meta:
        model = FileModel
        fields = (
            'file_original',
            'file_test',
        )
        labels = {
            'file_original': 'Оригинальный файл',
            'file_test': 'Проверочный файл',
        }
        help_texts = {
            'file_original': 'Обязательное поле',
            'file_test': 'Обязательное поле',
        }
