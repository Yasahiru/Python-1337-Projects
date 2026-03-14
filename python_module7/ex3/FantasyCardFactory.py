from ex0.CreatureCard import CreatureCard
from ex1.SpellCard import SpellCard
from ex1.ArtifactCard import ArtifactCard
from ex3.CardFactory import CardFactory
from typing import Dict  # , List
import random


class FantasyCardFactory(CardFactory):

    def __init__(self) -> None:
        self.creatures = []
        self.spells = []
        self.artifacts = []

    def create_creature(self) -> CreatureCard:
        card = CreatureCard("Dragon", 5, "LEGENDARY", 7, 5)
        self.creatures.append(card)
        return (card)

    def create_spell(self) -> SpellCard:
        card = SpellCard("Fireball", 3, "RARE", "damage")
        self.spells.append(card)
        return (card)

    def create_artifact(self, name_or_power) -> ArtifactCard:
        card = ArtifactCard(
            "Mana Crystal", 2,
            "Rare", 12, "Permanent: +1 mana per turn"
        )
        self.artifacts.append(card)
        return card

    def create_themed_deck(self, size: int) -> Dict:
        deck = {
            "creatures": self.creatures,
            "spells": self.spells,
            "artifacts": self.artifacts
        }

        for _ in range(size):
            choice = random.choice(["creature", "spell", "artifact"])

            if choice == "creature":
                deck["creatures"].append(self.create_creature())
            elif choice == "spell":
                deck["spells"].append(self.create_spell())
            else:
                deck["artifacts"].append(self.create_artifact())
        return deck

    def get_supported_types(self) -> dict:
        return {
            "creatures": self.creatures,
            "spell": self.spells,
            "artifact": self.artifacts
        }
