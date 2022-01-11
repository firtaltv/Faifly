from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('users_list', views.users_list, name='users_list'),
    path('detail/<str:url>', views.movie_detail_view, name='detail'),
    path('profile/<int:pk>', views.profile_view, name='profile'),

    path('profile/<int:pk>/private', views.go_private, name='private'),
    path('profile/<int:pk>/public', views.go_visible, name='public'),

    path('movies_list/watch_later/<str:url>', views.watch_later, name='watch_later'),
    path('movies_list/viewed/<str:url>', views.viewed, name='viewed'),
    path('movies_list/abandoned/<str:url>', views.abandoned, name='abandoned'),

    path('movies_list/delete_from_later/<str:url>', views.delete_from_later, name='delete_later'),
    path('movies_list/delete_from_viewed/<str:url>', views.delete_from_viewed, name='delete_viewed'),
    path('movies_list/delete_from_abandoned/<str:url>', views.delete_from_abandoned, name='delete_abandoned'),

    path('watch_later/list/<int:pk>', views.watch_later_list_view, name='watch_later_list'),
    path('viewed/list/<int:pk>', views.viewed_list_view, name='viewed_list'),
    path('abandoned/list/<int:pk>', views.abandoned_list_view, name='abandoned_list'),
]
