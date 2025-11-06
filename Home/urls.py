from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', views.home, name='home'),
	path('login/', views.login_view, name='login'),
	path('logout/', views.logout_view, name='logout'),
	path('signup/', views.user_signup, name='signup'),
	path('member-signup/', views.member_signup, name='member_signup'),
	path('feed/', views.feed_view, name='feed'),
	path('adminFeed/', views.admin_view, name='admin_dashboard'),
	path('addEvent/', views.addEvent, name='event'),
	path('delEvent/', views.delEvent, name='delEvent'),
	path('events_json/', views.events_json, name='events_json'),
	path('addNotification/', views.addNotic, name='notic'),
	path('delNotic/', views.delNotic, name='delNotic'),
	path('search-notifications/', views.search_notifications, name='search_notifications'),
	path('members/',views.list_users, name='members'),
	path('add-club/', views.add_club, name='clubs'),
	path('member/<str:username>/', views.member_detail, name='member_detail'),
	path('search-events/', views.search_events, name='search_events'),
	path('delClub/', views.delClub, name='delClub'),
	path('club-events/', views.club_events, name='club_events'),

]