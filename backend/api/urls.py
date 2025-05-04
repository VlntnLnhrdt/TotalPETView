from django.urls import path
from . import views

urlpatterns = [
    path('patient/search', views.search_patients, name='search_patients'),
    path('patient/<str:orthancId>/studies', views.patient_studies, name='patient_studies'),
    path('study/<str:orthancId>/series', views.study_series, name='study_series'),

]