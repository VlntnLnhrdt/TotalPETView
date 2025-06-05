from django.urls import path
from . import views

urlpatterns = [
    path('patient/search', views.search_patients, name='search_patients'),
    path('patient/<str:orthancId>', views.get_patient_data, name='get_patient_data'),
    path('patient/<str:orthancId>/studies', views.patient_studies, name='patient_studies'),
    path('patient/<str:orthancId>/series', views.patient_series, name='patient_series'),
    path('study/<str:orthancId>/series', views.study_series, name='study_series'),
    path('instance/<str:orthancId>/preview', views.instance_preview, name='instance_preview'),
    path('instance/<str:orthancId>/file', views.instance_file, name='instance_file')

]