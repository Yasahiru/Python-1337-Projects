from ex0.Card import Card
from ex3.CardFactory import CardFactory
from ex3.GameStrategy import GameStrategy
from typing import List


class GameEngine:
    def configure_engine(
        self, factory: CardFactory, strategy: GameStrategy,
        hand: List[Card], battlefield: str, turn_count: int
    ) -> None:
        self.strategy = strategy
        self.factory = factory
        self.hand = hand
        self.battlefield = battlefield
        self.turn_count = turn_count

    def simulate_turn(self) -> dict:
        result = self.strategy.execute_turn(self.hand, self.battlefield)
        self.turn_count += 1
        return result

    def get_engine_status(self) -> dict:
        return {
            "turn": self.turn_count,
            "hand_size": len(self.hand),
            "battlefield_size": len(self.battlefield),
            "strategy": self.strategy.get_strategy_name()
        }
