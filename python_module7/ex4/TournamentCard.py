from ex0.Card import Card
from ex2.Combatable import Combatable
from ex4.Rankable import Rankable


class TournamentCard(Card, Combatable, Rankable):
    def play(self, game_state: dict) -> dict:
        ...

    def attack(self, target) -> dict:
        ...

    def calculate_rating(self) -> int:
        ...

    def get_tournament_stats(self) -> dict:
        ...
