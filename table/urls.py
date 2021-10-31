from django.urls import path
from . import views

urlpatterns = [
    path('index/<int:pageId>',views.index_view,name="index_view"),
]