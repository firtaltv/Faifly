from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('detail/<str:url>', views.movie_detail_view, name='detail'),
    path('profile/', views.profile_view, name='profile'),
    path('movies_list/watch_later/<str:url>', views.watch_later, name='watch_later'),
    path('movies_list/viewed/<str:url>', views.viewed, name='viewed'),
    path('movies_list/abandoned/<str:url>', views.abandoned, name='abandoned'),
    path('movies_list/delete_from_later/<str:url>', views.delete_from_later, name='delete_later'),
    path('movies_list/delete_from_viewed/<str:url>', views.delete_from_viewed, name='delete_viewed'),
    path('movies_list/delete_from_abandoned/<str:url>', views.delete_from_abandoned, name='delete_abandoned'),
    path('watch_later/list', views.watch_later_list_view, name='watch_later_list'),
    path('viewed/list', views.viewed_list_view, name='viewed_list'),
    path('abandoned/list', views.abandoned_list_view, name='abandoned_list'),
]
