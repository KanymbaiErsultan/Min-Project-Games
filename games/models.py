from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Game(models.Model):
    """Модель игры"""
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    genre = models.CharField(max_length=100, verbose_name="Жанр")
    release_date = models.DateField(verbose_name="Дата выпуска")
    rating = models.FloatField(default=0, verbose_name="Рейтинг")
    image = models.ImageField(upload_to='games/', null=True, blank=True, verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Player(models.Model):
    """Модель игрока с системой уровней"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player')
    level = models.IntegerField(default=1, verbose_name="Уровень")
    experience = models.IntegerField(default=0, verbose_name="Опыт")
    total_points = models.IntegerField(default=0, verbose_name="Общие очки")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"
        ordering = ['-level', '-experience']

    def __str__(self):
        return f"{self.user.username} (Уровень {self.level})"

    @property
    def exp_to_next_level(self):
        """Опыт необходимый для следующего уровня"""
        return self.level * 100

    @property
    def exp_progress(self):
        """Процент прогресса к следующему уровню"""
        if self.exp_to_next_level == 0:
            return 0
        return int((self.experience % self.exp_to_next_level) / self.exp_to_next_level * 100)

    def add_experience(self, amount):
        """Добавить опыт и проверить повышение уровня"""
        self.experience += amount
        while self.experience >= self.exp_to_next_level:
            self.experience -= self.exp_to_next_level
            self.level += 1
        self.save()

    def add_points(self, amount):
        """Добавить очки"""
        self.total_points += amount
        self.save()


class Achievement(models.Model):
    """Модель достижения"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Легко'),
        ('medium', 'Средне'),
        ('hard', 'Сложно'),
    ]

    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='achievements', verbose_name="Игра")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium', verbose_name="Сложность")
    points = models.IntegerField(default=10, verbose_name="Очки за достижение")
    experience_reward = models.IntegerField(default=50, verbose_name="Награда опыта")
    players = models.ManyToManyField(Player, blank=True, related_name='achievements', verbose_name="Игроки")
    icon = models.ImageField(upload_to='achievements/', null=True, blank=True, verbose_name="Иконка")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.game.name})"


class PlayerGame(models.Model):
    """Прогресс игрока в конкретной игре"""
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='games', verbose_name="Игрок")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='players', verbose_name="Игра")
    hours_played = models.DecimalField(max_digits=6, decimal_places=1, default=0, verbose_name="Часов сыграно")
    game_level = models.IntegerField(default=1, verbose_name="Уровень в игре")
    game_points = models.IntegerField(default=0, verbose_name="Очки в игре")
    last_played = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('player', 'game')
        verbose_name = "Прогресс игрока"
        verbose_name_plural = "Прогресс игроков"
        ordering = ['-last_played']

    def __str__(self):
        return f"{self.player.user.username} в {self.game.name}"


class GameReview(models.Model):
    """Модель рецензии на игру"""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews', verbose_name="Игра")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='reviews', verbose_name="Игрок")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Оценка")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст рецензии")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('game', 'player')
        ordering = ['-created_at']
        verbose_name = "Рецензия"
        verbose_name_plural = "Рецензии"

    def __str__(self):
        return f"{self.title} - {self.game.name}"


class FriendRequest(models.Model):
    """Модель заявки в друзья"""
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('accepted', 'Принята'),
        ('declined', 'Отклонена'),
    ]

    from_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='sent_requests', verbose_name="От")
    to_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='received_requests', verbose_name="К")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_player', 'to_player')
        verbose_name = "Заявка в друзья"
        verbose_name_plural = "Заявки в друзья"

    def __str__(self):
        return f"{self.from_player.user.username} -> {self.to_player.user.username}"

    def accept(self):
        """Принять заявку в друзья"""
        self.status = 'accepted'
        self.save()


class UserBadge(models.Model):
    """Модель значка для игрока"""
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    icon = models.ImageField(upload_to='badges/', verbose_name="Иконка")
    requirement = models.CharField(max_length=200, verbose_name="Требование")
    players = models.ManyToManyField(Player, related_name='badges', verbose_name="Игроки")

    class Meta:
        verbose_name = "Значок"
        verbose_name_plural = "Значки"

    def __str__(self):
        return self.name


class Tournament(models.Model):
    """Модель турнира"""
    STATUS_CHOICES = [
        ('upcoming', 'Предстоящий'),
        ('active', 'Активный'),
        ('finished', 'Завершен'),
    ]

    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='tournaments', verbose_name="Игра")
    prize_pool = models.IntegerField(default=0, verbose_name="Призовой фонд")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming', verbose_name="Статус")
    start_date = models.DateTimeField(verbose_name="Дата начала")
    end_date = models.DateTimeField(verbose_name="Дата окончания")
    max_participants = models.IntegerField(default=100, verbose_name="Макс участников")
    participants = models.ManyToManyField(Player, related_name='tournaments', blank=True, verbose_name="Участники")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Турнир"
        verbose_name_plural = "Турниры"

    def __str__(self):
        return self.name

    @property
    def participants_count(self):
        return self.participants.count()


class TournamentResult(models.Model):
    """Модель результата турнира"""
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='results', verbose_name="Турнир")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='tournament_results', verbose_name="Игрок")
    position = models.IntegerField(verbose_name="Позиция")
    prize = models.IntegerField(default=0, verbose_name="Приз")
    score = models.IntegerField(default=0, verbose_name="Очки")

    class Meta:
        unique_together = ('tournament', 'player')
        ordering = ['position']
        verbose_name = "Результат турнира"
        verbose_name_plural = "Результаты турниров"

    def __str__(self):
        return f"{self.tournament.name} - {self.player.user.username}"


class DailyQuest(models.Model):
    """Модель ежедневного квеста"""
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='quests', verbose_name="Игра")
    reward_points = models.IntegerField(default=50, verbose_name="Награда очков")
    reward_experience = models.IntegerField(default=100, verbose_name="Награда опыта")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ежедневный квест"
        verbose_name_plural = "Ежедневные квесты"

    def __str__(self):
        return self.title


class PlayerQuestProgress(models.Model):
    """Модель прогресса квеста игрока"""
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='quest_progress', verbose_name="Игрок")
    quest = models.ForeignKey(DailyQuest, on_delete=models.CASCADE, verbose_name="Квест")
    completed = models.BooleanField(default=False, verbose_name="Завершен")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Завершен в")
    progress = models.IntegerField(default=0, verbose_name="Прогресс (%)")

    class Meta:
        unique_together = ('player', 'quest')
        verbose_name = "Прогресс квеста"
        verbose_name_plural = "Прогресс квестов"

    def __str__(self):
        return f"{self.player.user.username} - {self.quest.title}"


@receiver(post_save, sender=User)
def create_player(sender, instance, created, **kwargs):
    """Автоматически создавать профиль игрока при создании пользователя"""
    if created:
        Player.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_player(sender, instance, **kwargs):
    """Автоматически сохранять профиль игрока"""
    if hasattr(instance, 'player'):
        instance.player.save()
