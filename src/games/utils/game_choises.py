from django.db import models


class GameСhoises(models.Model):
    ACTION = "Action"
    ADVENTURE = "Adventure"
    RPG = "RPG"
    SIMULATION = "Simulation"
    STRATEGY = "Strategy"
    SPORTS = "Sports"
    HORROR = "Horror"
    SHOOTER = "Shooter"
    PUZZLE = "Puzzle"

    GENRE_CHOICES = [
        (ACTION, "Action"),
        (ADVENTURE, "Adventure"),
        (RPG, "Role-playing (RPG)"),
        (SIMULATION, "Simulation"),
        (STRATEGY, "Strategy"),
        (SPORTS, "Sports"),
        (HORROR, "Horror"),
        (SHOOTER, "Shooter"),
        (PUZZLE, "Puzzle"),
    ]

    PC = "PC"
    PLAYSTATION3 = "PlayStation 3"
    PLAYSTATION4 = "Playstation 4"
    PLAYSTATION5 = "Playstation 5"
    XBOX360 = "XBOX 360"
    XBOXONE = "XBOX ONE"
    XBOXSERIES = "XBOX Series X/S"
    SWITCH = "Nintendo Switch"
    MOBILE = "Mobile"

    PLATFORM_CHOICES = [
        (PC, "PC"),
        (PLAYSTATION3, "PlayStation 3"),
        (PLAYSTATION4, "PlayStation 4"),
        (PLAYSTATION5, "PlayStation 5"),
        (XBOX360, "XBOX 360"),
        (XBOXONE, "XBOX ONE"),
        (XBOXSERIES, "XBOX Series X/S"),
        (SWITCH, "Nintendo Switch"),
        (MOBILE, "Mobile"),
    ]
