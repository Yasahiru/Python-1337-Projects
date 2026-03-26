from ex0.Card import Card
from ex2.Combatable import Combatable
from ex4.Rankable import Rankable


class TournamentCard(Card, Combatable, Rankable):
    def __init__(
        self, name: str, cost: int, rarity: str,
        wins, losses
    ) -> None:
        super().__init__(name, cost, rarity)
        self.wins = wins
        self.losses = losses

    # Card.py
    def play(self, game_state: dict) -> dict:
        ...

    # Combatable
    def attack(self, target) -> dict:
        ...

    def defend(self, incoming_damage: int) -> dict:
        ...

    def get_combat_stats(self) -> dict:
        ...

    # Rankable
    def calculate_rating(self) -> int:
        rating = (self.wins * 10) - (self.losses * 12)
        return (rating)

    def update_wins(self, wins: int) -> None:
        self.wins += wins

    def update_losses(self, losses: int) -> None:
        self.losses += losses

    def get_rank_info(self) -> dict:
        ...

    #  Tournament card
    def get_tournament_stats(self) -> dict:
        ...
