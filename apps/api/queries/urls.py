from django.urls import path

from apps.api.queries.views import CategoryView, QueryViewSet, ParamView

urlpatterns = [
    path('categories/', CategoryView.as_view()),
    path('params/<slug>', ParamView.as_view()),
    path('queries/<slug>', QueryViewSet.as_view({'get': 'retrieve'})),
    path('queries/<slug>/excel', QueryViewSet.as_view({'get': 'excel'})),
]
