from django.urls import path
from inquiries.views import (AcademicRequestsCreateView,AcademicRequestsUpdateView,AcademicRequestsDeleteView,AcademicRequestsListView,
                             AdministrativeRequestsCreateView,AdministrativeRequestsUpdateView,AdministrativeRequestsDeleteView,AdministrativeRequestsListView)

urlpatterns = [
    path('academicrequest/new/', AcademicRequestsCreateView.as_view(), name='academicrequests-create'),
    path('academicrequest/<int:pk>/update/', AcademicRequestsUpdateView.as_view(), name='academicrequests-update'),
    path('academicrequest/<int:pk>/delete/', AcademicRequestsDeleteView.as_view(), name='academicrequests-delete'),
    path('academicrequests/', AcademicRequestsListView.as_view(), name='academicrequests-list'),
    path('administrativerequest/new/', AdministrativeRequestsCreateView.as_view(), name='administrativerequests-create'),
    path('administrativerequest/<int:pk>/update/', AdministrativeRequestsUpdateView.as_view(), name='administrativerequests-update'),
    path('administrativerequest/<int:pk>/delete/', AdministrativeRequestsDeleteView.as_view(), name='administrativerequests-delete'),
    path('administrativerequests/', AdministrativeRequestsListView.as_view(), name='administrativerequests-list'),
]
