from django import forms
from .models import GameReview, FriendRequest

class GameReviewForm(forms.ModelForm):
    """Форма для создания рецензии"""
    class Meta:
        model = GameReview
        fields = ['rating', 'title', 'text']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} ⭐') for i in range(1, 6)]),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок рецензии'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваша рецензия...',
                'rows': 5
            }),
        }

class PlayerSearchForm(forms.Form):
    """Форма для поиска игроков"""
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск игрока...'
        })
    )
