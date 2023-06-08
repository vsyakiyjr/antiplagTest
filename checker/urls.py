from django.urls import path
from django.urls import reverse
from . import views

app_name='checker'

urlpatterns = [
    path('file-upload/', views.file_upload, name ='file_upload' ),
    path('file-processed/<str:response>/', views.file_processed, name='file_processed'),
]
def some_view(request):
    login_url = reverse('users:login')