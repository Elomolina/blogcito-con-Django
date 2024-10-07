from django.urls import path

from . import views

app_name = "blog_site"
urlpatterns = [
    path("", views.index, name = "index"),
    path("posts", views.posts, name = "posts"),
    path("posts/<slug:slug>", views.DetailPostView.as_view(), name = "detail_post"),
    path("perfil", views.PerfilView.as_view(), name = "perfil"),
    path("Miperfil", views.MyProfileView.as_view(), name = "MiPerfil"),
    path("crear", views.CreateView.as_view(), name = "create_post"),
    path("borrar/<slug:slug>", views.BorrarView.as_view(), name = "borrar"),
    path("leer-despues/<int:id>/<slug:slug>", views.ReadLaterView.as_view(), name = "read_later"),
    path("user/<str:username>", views.UserProfileView.as_view(), name="user_profile"),
    path("search/", views.SearchView.as_view(), name="search")
]