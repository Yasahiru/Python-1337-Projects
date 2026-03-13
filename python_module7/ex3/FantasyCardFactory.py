from ex0.CreatureCard import CreatureCard
from ex1.SpellCard import SpellCard
from ex1.ArtifactCard import ArtifactCard
from ex3.CardFactory import CardFactory
from typing import Dict
import random


class FantasyCardFactory(CardFactory):

    def create_creature(self) -> CreatureCard:
        return CreatureCard("Dragon", 5, "LEGENDARY", 7, 5)

    def create_spell(self) -> SpellCard:
        return SpellCard("Fireball", 3, "RARE", "damage")

    def create_artifact(self, name_or_power) -> ArtifactCard:
        return ArtifactCard(
            "Mana Crystal", 2,
            "Rare", 12, "Permanent: +1 mana per turn"
        )

    def create_themed_deck(self, size: int) -> Dict:
        deck = {
            "creatures": [],
            "spells": [],
            "artifacts": []
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
            "creature": "Fantasy creatures",
            "spell": "Fantasy magic spells",
            "artifact": "Magical fantasy artifacts"
        }
