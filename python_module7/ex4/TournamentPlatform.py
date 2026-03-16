from ex4.TournamentCard import TournamentCard


class TournamentPlatform:

    def __init__(self):
        self.cards = []
        self.matches_played = 0

    def register_card(self, card: TournamentCard) -> str:
        self.cards.append(card)

    def create_match(self, card1_id: str, card2_id: str) -> dict:
        if card1_id.attack(card2_id):
            winner, loser = card1_id, card2_id
        else:
            winner, loser = card2_id, card1_id

        winner.record_win()
        loser.record_loss()

        winner.update_rating(winner.rating + 16)
        loser.update_rating(loser.rating - 16)

        self.matches_played += 1

        return {
            "winner": winner.card_id,
            "loser": loser.card_id,
            "winner_rating": winner.rating,
            "loser_rating": loser.rating,
        }

    def get_leaderboard(self) -> list:
        return sorted(
            self.cards.values(),
            key=lambda c: c.rating,
            reverse=True,
        )

    def generate_tournament_report(self) -> dict:
        _sum = sum(c.rating for c in self.cards.values())
        avg_rating = _sum // len(self.cards)

        return {
            "total_cards": len(self.cards),
            "matches_played": self.matches_played,
            "avg_rating": avg_rating,
            "platform_status": "active",
        }
