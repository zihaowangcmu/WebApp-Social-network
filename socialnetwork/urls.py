from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$',                 views.global_stream,     name='home'),
    url(r'^myProfile$',        views.myProfile,         name='myProfile'),
    url(r'^someone_profile$',  views.someone_profile,   name='someone_profile'),
    url(r'^add_post$',         views.add_post,          name='add_post'),
    url(r'^global_stream$',    views.global_stream,     name='global_stream'),
    url(r'^follower_stream$',  views.follower_stream,   name='follower_stream'),
    url(r'^register$',         views.register,          name='register'),
    url(r'^edit_bio$',         views.edit_bio,          name='edit_bio'),
    url(r'^add_comment$',      views.add_comment,       name='add_comment'),
    
    url(r'^follow$',           views.follow,            name='follow'),
    url(r'^unfollow$',         views.unfollow,          name='unfollow'),
    url(r'^someone_not_exist$',views.someone_not_exist, name='someone_not_exist'),

    url(r'^add_photo$',             views.add_photo,    name='add_photo'),
    url(r'^get_photo/(?P<id>\d+)$', views.get_photo,    name='get_photo'),

    url(r'^get_list_json$',    views.get_list_json,     name='get_list_json'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$',    auth_views.login, {'template_name':'socialnetwork/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$',   auth_views.logout_then_login,                                  name='logout'),
]