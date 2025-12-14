from django.core.management.base import BaseCommand
from games.models import Game
from datetime import date

class Command(BaseCommand):
    help = 'Добавляет игры в базу данных'

    def handle(self, *args, **options):
        games_data = [
            {
                'name': 'The Witcher 3',
                'description': 'Эпическая RPG с открытым миром, где вы играете охотником на монстров Геральтом из Ривии.',
                'genre': 'RPG',
                'release_date': date(2015, 5, 19),
                'rating': 9.3,
            },
            {
                'name': 'Cyberpunk 2077',
                'description': 'Футуристический экшн-RPG в огромном городе Найт-Сити, где вы создаёте своего персонажа и выбираете свой путь.',
                'genre': 'RPG',
                'release_date': date(2020, 12, 10),
                'rating': 8.5,
            },
            {
                'name': 'Elden Ring',
                'description': 'Сложный экшн-RPG от создателей Dark Souls с открытым миром и глубоким сюжетом.',
                'genre': 'Action RPG',
                'release_date': date(2022, 2, 25),
                'rating': 9.1,
            },
            {
                'name': 'Valorant',
                'description': 'Быстрый командный шутер с тактическим компонентом. Выбирайте агентов с уникальными способностями.',
                'genre': 'Shooter',
                'release_date': date(2020, 6, 2),
                'rating': 8.7,
            },
            {
                'name': 'League of Legends',
                'description': 'Популярная MOBA, где две команды соревнуются в стратегических боях на арене.',
                'genre': 'MOBA',
                'release_date': date(2009, 10, 27),
                'rating': 8.4,
            },
            {
                'name': 'Dota 2',
                'description': 'Сложная MOBA с глубокой механикой и высокой потолком мастерства. Огромная киберспортивная сцена.',
                'genre': 'MOBA',
                'release_date': date(2013, 7, 9),
                'rating': 8.6,
            },
            {
                'name': 'Counter-Strike 2',
                'description': 'Легендарный тактический шутер с бесплатной моделью игры. Требует точности и командной работы.',
                'genre': 'Shooter',
                'release_date': date(2023, 9, 1),
                'rating': 8.8,
            },
            {
                'name': 'Starfield',
                'description': 'Огромная космическая RPG от Bethesda. Исследуйте сотни планет и создавайте свою историю.',
                'genre': 'Space RPG',
                'release_date': date(2023, 9, 6),
                'rating': 7.9,
            },
            {
                'name': 'Baldurs Gate 3',
                'description': 'Потрясающая RPG с адаптивным сюжетом, где каждый выбор имеет значение.',
                'genre': 'RPG',
                'release_date': date(2023, 8, 3),
                'rating': 9.4,
            },
            {
                'name': 'Final Fantasy XVI',
                'description': 'Эпическое приключение в фантастическом мире с захватывающим боевым видеоролик.',
                'genre': 'Action RPG',
                'release_date': date(2023, 6, 22),
                'rating': 8.9,
            },
            {
                'name': 'Palworld',
                'description': 'Уникальное deckbuilding-путешествие с покемонами, охотой и выживанием.',
                'genre': 'Adventure',
                'release_date': date(2024, 1, 18),
                'rating': 8.3,
            },
            {
                'name': 'Helldivers 2',
                'description': 'Кооперативный шутер для 4 игроков. Защищайте человечество от инопланетных угроз.',
                'genre': 'Co-op Shooter',
                'release_date': date(2024, 2, 8),
                'rating': 8.5,
            },
        ]

        for game_data in games_data:
            game, created = Game.objects.get_or_create(
                name=game_data['name'],
                defaults={
                    'description': game_data['description'],
                    'genre': game_data['genre'],
                    'release_date': game_data['release_date'],
                    'rating': game_data['rating'],
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Добавлена игра: {game.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Игра уже существует: {game.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('\n✓ Все игры успешно добавлены!')
        )
