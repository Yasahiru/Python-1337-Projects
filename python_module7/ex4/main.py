from ex0.CreatureCard import CreatureCard
from ex4.TournamentPlatform import TournamentPlatform


def main():

    print("=== DataDeck Tournament Platform ===")

    platform = TournamentPlatform()

    print("Registering Tournament Cards...")

    platform.register_card(
        CreatureCard("Fire Dragon", 1200, "dragon", 12, 10))
    platform.register_card(
        CreatureCard("Ice Wizard", 1150, "wizard", 10, 11))

    for card in [platform.cards]:

        print(f"{card.name} (ID: {card.name}_001):")
        print("- Interfaces: [Card, Combatable, Rankable]")
        print(f"- Rating: {card.rating}")
        print(f"- Record: {card.record()}")

    print("Creating tournament match...")

    result = platform.match(platform.cards)

    print("Match result:", result)

    print("Tournament Leaderboard:")

    leaderboard = platform.leaderboard()

    for i, card in enumerate(leaderboard, 1):
        print(f"{i}. {card.name} - Rating: {card.rating} ({card.record()})")

    print("Platform Report:")
    print(platform.report())

    print("=== Tournament Platform Successfully Deployed! ===")
    print("All abstract patterns working together harmoniously!")


if __name__ == "__main__":
    main()
