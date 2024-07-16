from django.contrib.auth.models import AbstractUser
from django.db import models

team_options = (
    ('Spania', 'spain'),
    ('Georgia', 'georgia'),
    ('Germania', 'germany'),
    ('Danemarca', 'denmark'),
    ('Portugalia', 'portugal'),
    ('Slovenia', 'slovenia'),
    ('Franța', 'france'),
    ('Belgia', 'belgium'),
    ('România', 'romania'),
    ('Olanda', 'netherlands'),
    ('Austria', 'austria'),
    ('Turcia', 'turkey'),
    ('Anglia', 'england'),
    ('Slovacia', 'slovakia'),
    ('Elveția', 'switzerland'),
    ('Italia', 'italy'),
)


# Model for user

class CustomUserModel(AbstractUser):
    gender_options = (
        ('male', 'Masculin'),
        ('female', 'Feminin'),
        ('other', 'As prefera sa nu raspund'),
    )
    gender = models.CharField(max_length=6, choices=gender_options, null=True)
    birth_day = models.DateField(null=True)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.username}'


class TeamModel(models.Model):
    name = models.CharField(max_length=50, choices=team_options, null=False, unique=True)
    manager = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ChoseTeamModel(models.Model):

    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE, null=True)
    team = models.ForeignKey(TeamModel, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.user.username} - {self.team.name}"

class Player(models.Model):
    position_options = (
        ('goalkeeper', 'GK'),
        ('defender', 'DF'),
        ('midfielder', 'MF'),
        ('attacker', 'FW')
    )
    name = models.CharField(max_length=50, null=False)
    age = models.PositiveIntegerField(null=False, default=0)
    position = models.CharField(max_length=26, choices=position_options, null=False, default='goalkeeper')
    team = models.ForeignKey(TeamModel, on_delete=models.CASCADE)
    price_value = models.IntegerField(null=False, default=0)
    ball_skills = models.PositiveIntegerField(null=False, default=0)
    passing = models.PositiveIntegerField(null=False, default=0)
    shooting = models.PositiveIntegerField(null=False, default=0)
    defence = models.PositiveIntegerField(null=False, default=0)
    physical = models.PositiveIntegerField(null=False, default=0)
    mental = models.PositiveIntegerField(null=False, default=0)
    goalkeeper = models.PositiveIntegerField(null=False, default=0)
    overall_avg = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} poziție ({self.position})'

    def save(self, *args, **kwargs):
        attributes_fields = [
            'ball_skills', 'passing', 'shooting', 'defence', 'physical', 'mental', 'goalkeeper'
        ]
        total_skills = 0
        for field in attributes_fields:
            total_skills += getattr(self, field)
        self.overall_avg = total_skills / len(attributes_fields)
        super().save(*args, **kwargs)

# selected player model
class SelectedPlayer(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    player = models.ForeignKey(Player,on_delete=models.CASCADE)

    def __str__(self):
        return f'La echipa ta s-a alăturat :  {self.player}'




