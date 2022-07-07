from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_tunnel/", views.new_tunnel, name="new_tunnel"),
    path("edit_tunnel/<int:tunnel_id>", views.edit_tunnel, name="edit_tunnel")
]