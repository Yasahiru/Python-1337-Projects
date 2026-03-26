from ex4.TournamentPlatform import TournamentPlatform
from ex4.TournamentCard import TournamentCard


def main():

    print("=== DataDeck Tournament Platform ===\n")
    print("Registering Tournament Cards...\n")

    platform = TournamentPlatform()

    winner = TournamentCard(
            name="Fire Dragon",
            cost=7,
            rarity="Legend",
            wins=0,
            losses=0
        )
    looser = TournamentCard(
        name="Ice Wizard",
        cost=3,
        rarity="RARE",
        wins=0,
        losses=0
    )
    platform.register_card(winner)
    platform.register_card(looser)

    for card in platform.cards:
        print(f"{card.name} (ID: {card.name}_001):")
        print("- Interfaces: [Card, Combatable, Rankable]")
        print(f"- Rating: {card.calculate_rating()}")
        print(f"- Record: {card.wins} - {card.losses}\n")

    result = platform.create_match("dragon_001", "wizard_001")
    print("Creating tournament match...")
    print(f"Match result: {result}\n")
    print("Tournament Leaderboard:")

    leaderboard = platform.get_leaderboard()

    for card in leaderboard:
        print(
            f" {card.name} - Rating: {card.calculate_rating()} "
            f"({card.wins} - {card.losses})"
        )

    print("\nPlatform Report:")
    print(f"{platform.tournament_report()}\n")

    print("=== Tournament Platform Successfully Deployed! ===")
    print("All abstract patterns working together harmoniously!")


if __name__ == "__main__":
    main()
