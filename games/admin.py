from django.contrib import admin
from .models import Game, Player, Achievement, PlayerGame, GameReview, FriendRequest, UserBadge, Tournament, TournamentResult, DailyQuest, PlayerQuestProgress

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'rating', 'release_date')
    list_filter = ('genre', 'release_date')
    search_fields = ('name', 'description')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'experience', 'total_points')
    list_filter = ('level',)
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'difficulty', 'points', 'experience_reward')
    list_filter = ('game', 'difficulty')
    search_fields = ('name',)
    filter_horizontal = ('players',)

@admin.register(PlayerGame)
class PlayerGameAdmin(admin.ModelAdmin):
    list_display = ('player', 'game', 'game_level', 'hours_played')
    list_filter = ('game', 'game_level')
    search_fields = ('player__user__username', 'game__name')

@admin.register(GameReview)
class GameReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'game', 'player', 'rating', 'created_at')
    list_filter = ('game', 'rating', 'created_at')
    search_fields = ('title', 'text')

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_player', 'to_player', 'status', 'created_at')
    list_filter = ('status', 'created_at')

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'requirement')
    filter_horizontal = ('players',)

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'status', 'start_date', 'participants_count')
    list_filter = ('status', 'game', 'start_date')
    filter_horizontal = ('participants',)

@admin.register(TournamentResult)
class TournamentResultAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'player', 'position', 'score')
    list_filter = ('tournament', 'position')

@admin.register(DailyQuest)
class DailyQuestAdmin(admin.ModelAdmin):
    list_display = ('title', 'game', 'reward_points', 'is_active')
    list_filter = ('game', 'is_active')

@admin.register(PlayerQuestProgress)
class PlayerQuestProgressAdmin(admin.ModelAdmin):
    list_display = ('player', 'quest', 'progress', 'completed')
    list_filter = ('completed', 'quest')
