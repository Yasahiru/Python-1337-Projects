from ex3.FantasyCardFactory import FantasyCardFactory
from ex3.AggressiveStrategy import AggressiveStrategy
from ex3.GameEngine import GameEngine


def main():

    print("=== DataDeck Game Engine ===\n")
    print("Configuring Fantasy Card Game...")

    factory = FantasyCardFactory()
    strategy = AggressiveStrategy()
    engine = GameEngine()

    print(f"Factory: {factory.__class__.__name__}")
    print(f"Strategy: {strategy.__class__.__name__}")

    card_types = factory.get_supported_types()
    print(f"Available types: {card_types}")
    for key, value in card_types.items():
        print(value)

    hand = ""
    battlefield = []

    print("Simulating aggressive turn...")
    print(f"Hand: {hand}")

    engine.configure_engine(
        factory=factory,
        strategy=strategy,
        hand=hand,
        battlefield=battlefield,
        turn_count=0
    )

    actions = engine.simulate_turn()

    print("\nTurn execution:")
    print(f"Strategy: {strategy.get_strategy_name()}")
    print(f"Actions: {actions}")

    report = {
        "turns_simulated": engine.turn_count,
        "strategy_used": strategy.get_strategy_name(),
        "total_damage": actions.get("damage_dealt", 0),
        "cards_created": 3
    }

    print("\nGame Report:")
    print(f"{report}\n")

    print("Abstract Factory + Strategy Pattern: Maximum flexibility achieved!")


if __name__ == "__main__":
    main()
