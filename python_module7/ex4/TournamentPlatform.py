from ex4.TournamentCard import TournamentCard


class TournamentPlatform:

    def __init__(self):
        self.cards = []
        self.matches_played = 0

    platform_status: bool = False

    def register_card(self, card: TournamentCard) -> str:
        self.cards.append(card)
        self.platform_status = True
        return "Card registred successfuly!!"

    def create_match(self, card1_id: str, card2_id: str) -> dict:
        self.matches_played += 1

        winner = self.cards[0]
        looser = self.cards[1]

        winner.update_wins(1)
        looser.update_losses(1)

        self.register_card(winner)
        self.register_card(looser)

        return {
            'winner': card1_id, 'loser': card2_id,
            'winner_rating': winner.calculate_rating(),
            'loser_rating': looser.calculate_rating()
        }

    def get_leaderboard(self) -> list:
        self.platform_status = False
        leaderboard = []
        card1_rating = self.cards[0].calculate_rating()
        card2_rating = self.cards[1].calculate_rating()
        if (card1_rating > card2_rating):
            leaderboard.append(self.cards[0])
            leaderboard.append(self.cards[1])
        else:
            leaderboard.append(self.cards[1])
            leaderboard.append(self.cards[0])
        return (leaderboard)

    def tournament_report(self) -> dict:
        _sum = 0
        for card in self.cards:
            _sum += card.calculate_rating()
        avg_rating = _sum / len(self.cards) if len(self.cards) > 0 else 0

        return {
            "total_cards": len(self.cards),
            "matches_played": self.matches_played,
            "avg_rating": avg_rating,
            "platform_status": self.platform_status,
        }
