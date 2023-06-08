from django.db import models
from django.contrib.auth import get_user_model


class Report(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='reports/', blank=True, null=True) # delete later
    original_doc = models.FileField(upload_to='origianl_docs/', blank=True, null=True)
    report = models.FileField(upload_to='reports/', blank=True, null=True)
    pickles = models.FileField(upload_to='pickles/', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    date_str = models.CharField(max_length=32)


class Comment(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # last_edited_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    position = models.IntegerField()
    # start_index = models.IntegerField()
    # end_index = models.IntegerField()
    deleted = models.BooleanField(default=False)

    # def __str__(self):
        # return f"{self.author.username}: {self.text[:20]}"