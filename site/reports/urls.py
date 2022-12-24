from django.urls import path

from reports.views import CreateReport

app_name = 'reports'

urlpatterns = [
    path('create/<int:book_id>/', CreateReport.as_view(), name='create'),
]
