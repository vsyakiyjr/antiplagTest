from django.urls import path
from . import views

app_name='reports'

urlpatterns = [
    path('', views.display_user_reports, name='display_report_list'),
    path('<int:report_id>/', views.download_file, name='download_file'),
    path('<int:report_id>/open/', views.open_report, name='open_report'),
]