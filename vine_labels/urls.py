from django.urls import path
from . import views
from vine_labels.views import MainView

urlpatterns = [
    path('', MainView.as_view())
]