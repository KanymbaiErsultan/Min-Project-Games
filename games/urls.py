from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('games/', views.games_list, name='games_list'),
    path('game/<int:pk>/', views.game_detail, name='game_detail'),
    path('game/<int:game_id>/review/', views.add_review, name='add_review'),
    path('player/<str:username>/', views.player_profile, name='player_profile'),
    path('dashboard/', views.player_dashboard, name='dashboard'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('game/<int:game_id>/start/', views.start_game, name='start_game'),
    path('achievement/<int:achievement_id>/add/', views.add_achievement, name='add_achievement'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('players/search/', views.search_players, name='search_players'),
    path('player/<int:player_id>/friend-request/', views.send_friend_request, name='send_friend_request'),
    path('friend-requests/', views.friend_requests, name='friend_requests'),
    path('tournaments/', views.tournaments, name='tournaments'),
    path('tournament/<int:pk>/', views.tournament_detail, name='tournament_detail'),
    path('quests/', views.daily_quests, name='daily_quests'),
    path('quest/<int:quest_id>/complete/', views.complete_quest, name='complete_quest'),
]
