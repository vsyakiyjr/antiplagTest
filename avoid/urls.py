from django.urls import path
from django.urls import reverse

from . import views
app_name = 'avoid'
urlpatterns = [
    path('file-upload-avoid/', views.file_upload_avoid, name='file_upload_avoid'),
    path('file-processed-avoid/<str:response>/', views.file_processed_avoid, name='file_processed_avoid'),
    path('download/', views.download_file, name='download_file'),
    path('download-report/', views.download_report, name='download_report'),
    path('get-uniqueness/', views.plagiarism_uniqueness, name='plagiarism_uniqueness'),
    path('plagiarism-report', views.get_plagiarism_report, name='plagiarism_report'),
    path('plagiarism-excepturl/', views.plagiarism_excepturl, name='plagiarism_excepturl')
]
def some_view(request):
    login_url = reverse('users:login')