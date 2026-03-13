from ex3.GameStrategy import GameStrategy
# from typing import Dict
# import random


class AggressiveStrategy(GameStrategy):
    def execute_turn(self, hand: list, battlefield: list) -> dict:
        played_cards = []
        attacks = []

        for card in hand:
            if card.__class__.__name__ == "CreatureCard":
                battlefield.append(card)
                hand.remove(card)
                played_cards.append(card.name)

        for card in battlefield:
            attacks.append(card.name)

        return {
            "played": played_cards,
            "attacks": attacks
        }

    def get_strategy_name(self) -> str:
        return ("AggressiveStrategy")

    def prioritize_targets(self, available_targets: list) -> list:
        return sorted(
            available_targets,
            key=lambda t: getattr(t, "power", 0),
            reverse=True
        )
