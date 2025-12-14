from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .forms import GameReviewForm, PlayerSearchForm
from .models import Game, Player, Achievement, PlayerGame, GameReview, FriendRequest, Tournament, DailyQuest, PlayerQuestProgress, TournamentResult

def home(request):
    """Главная страница"""
    games = Game.objects.all()[:8]
    top_players = Player.objects.all()[:5]
    total_games = Game.objects.count()
    total_players = Player.objects.count()
    
    context = {
        'games': games,
        'top_players': top_players,
        'total_games': total_games,
        'total_players': total_players,
    }
    return render(request, 'home.html', context)

def games_list(request):
    """Список всех игр"""
    games = Game.objects.all()
    genre = request.GET.get('genre')
    if genre:
        games = games.filter(genre=genre)
    
    genres = Game.objects.values_list('genre', flat=True).distinct()
    
    context = {
        'games': games,
        'genres': genres,
        'selected_genre': genre,
    }
    return render(request, 'games_list.html', context)

def game_detail(request, pk):
    """Детали игры"""
    game = get_object_or_404(Game, pk=pk)
    achievements = game.achievements.all()
    players_count = game.players.count()
    reviews = game.reviews.all()
    
    player_game = None
    if request.user.is_authenticated:
        try:
            player_game = PlayerGame.objects.get(player__user=request.user, game=game)
        except PlayerGame.DoesNotExist:
            pass
    
    context = {
        'game': game,
        'achievements': achievements,
        'players_count': players_count,
        'player_game': player_game,
        'reviews': reviews,
    }
    return render(request, 'game_detail.html', context)

@login_required
def player_profile(request, username):
    """Профиль игрока"""
    user = get_object_or_404(User, username=username)
    player = user.player
    games = player.games.all()
    achievements = player.achievements.all()
    
    context = {
        'player': player,
        'user': user,
        'games': games,
        'achievements': achievements,
    }
    return render(request, 'player_profile.html', context)

@login_required
def player_dashboard(request):
    """Личный кабинет игрока"""
    player = request.user.player
    games = player.games.all()[:6]
    achievements = player.achievements.all()[:6]
    
    context = {
        'player': player,
        'games': games,
        'achievements': achievements,
    }
    return render(request, 'player_dashboard.html', context)

@login_required
def leaderboard(request):
    """Таблица лидеров"""
    players = Player.objects.all()
    
    context = {
        'players': players,
    }
    return render(request, 'leaderboard.html', context)

@login_required
@require_http_methods(["POST"])
def start_game(request, game_id):
    """Начать игру"""
    game = get_object_or_404(Game, pk=game_id)
    player = request.user.player
    
    player_game, created = PlayerGame.objects.get_or_create(
        player=player,
        game=game,
        defaults={'hours_played': 0}
    )
    
    return redirect('game_detail', pk=game_id)

@login_required
@require_http_methods(["POST"])
def add_achievement(request, achievement_id):
    """Добавить достижение игроку"""
    achievement = get_object_or_404(Achievement, pk=achievement_id)
    player = request.user.player
    
    if player not in achievement.players.all():
        achievement.players.add(player)
        player.add_experience(achievement.experience_reward)
        player.add_points(achievement.points)
    
    return redirect('game_detail', pk=achievement.game.pk)

def register(request):
    """Регистрация"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password == password_confirm:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                user_auth = authenticate(username=username, password=password)
                login(request, user_auth)
                return redirect('home')
    
    return render(request, 'register.html')

def login_view(request):
    """Вход"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
    
    return render(request, 'login.html')

@login_required
def logout_view(request):
    """Выход"""
    logout(request)
    return redirect('home')

@login_required
def add_review(request, game_id):
    """Добавить рецензию"""
    game = get_object_or_404(Game, pk=game_id)
    
    try:
        review = GameReview.objects.get(game=game, player__user=request.user)
    except GameReview.DoesNotExist:
        review = None
    
    if request.method == 'POST':
        form = GameReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.game = game
            review.player = request.user.player
            review.save()
            return redirect('game_detail', pk=game_id)
    else:
        form = GameReviewForm(instance=review)
    
    context = {'form': form, 'game': game}
    return render(request, 'add_review.html', context)

@login_required
def search_players(request):
    """Поиск игроков"""
    form = PlayerSearchForm()
    players = Player.objects.all()
    
    if request.method == 'GET':
        search = request.GET.get('search', '')
        if search:
            players = players.filter(
                Q(user__username__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search)
            )
    
    context = {
        'form': form,
        'players': players,
    }
    return render(request, 'search_players.html', context)

@login_required
def send_friend_request(request, player_id):
    """Отправить заявку в друзья"""
    to_player = get_object_or_404(Player, pk=player_id)
    from_player = request.user.player
    
    if from_player != to_player:
        friend_request, created = FriendRequest.objects.get_or_create(
            from_player=from_player,
            to_player=to_player
        )
    
    return redirect('player_profile', username=to_player.user.username)

@login_required
def friend_requests(request):
    """Заявки в друзья"""
    player = request.user.player
    received_requests = player.received_requests.filter(status='pending')
    
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        
        try:
            friend_req = FriendRequest.objects.get(pk=request_id)
            
            if action == 'accept':
                friend_req.accept()
            elif action == 'decline':
                friend_req.status = 'declined'
                friend_req.save()
        except FriendRequest.DoesNotExist:
            pass
        
        return redirect('friend_requests')
    
    context = {
        'received_requests': received_requests,
    }
    return render(request, 'friend_requests.html', context)

@login_required
def tournaments(request):
    """Список турниров"""
    tournaments_list = Tournament.objects.all()
    player = request.user.player
    
    context = {
        'tournaments': tournaments_list,
        'player': player,
    }
    return render(request, 'tournaments.html', context)

@login_required
def tournament_detail(request, pk):
    """Детали турнира"""
    tournament = get_object_or_404(Tournament, pk=pk)
    results = tournament.results.all()
    is_participant = request.user.player in tournament.participants.all()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'join' and not is_participant:
            tournament.participants.add(request.user.player)
            is_participant = True
        elif action == 'leave' and is_participant:
            tournament.participants.remove(request.user.player)
            is_participant = False
    
    context = {
        'tournament': tournament,
        'results': results,
        'is_participant': is_participant,
    }
    return render(request, 'tournament_detail.html', context)

@login_required
def daily_quests(request):
    """Ежедневные квесты"""
    player = request.user.player
    quests = DailyQuest.objects.filter(is_active=True)
    quest_progress = PlayerQuestProgress.objects.filter(player=player)
    
    for quest in quests:
        progress, created = PlayerQuestProgress.objects.get_or_create(
            player=player,
            quest=quest
        )
    
    context = {
        'quests': quests,
        'quest_progress': {qp.quest_id: qp for qp in quest_progress},
    }
    return render(request, 'daily_quests.html', context)

@login_required
def complete_quest(request, quest_id):
    """Завершить квест"""
    quest = get_object_or_404(DailyQuest, pk=quest_id)
    player = request.user.player
    
    try:
        progress = PlayerQuestProgress.objects.get(player=player, quest=quest)
        if not progress.completed:
            progress.completed = True
            progress.progress = 100
            from django.utils import timezone
            progress.completed_at = timezone.now()
            progress.save()
            
            player.add_points(quest.reward_points)
            player.add_experience(quest.reward_experience)
    except PlayerQuestProgress.DoesNotExist:
        pass
    
    return redirect('daily_quests')
