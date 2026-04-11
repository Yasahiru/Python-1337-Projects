

def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(
        artifacts,
        key=lambda a: a["power"],
        reverse=True
    )


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return (
        list(
            filter(lambda m: m["power"] >= min_power, mages)
        )
    )


def spell_transformer(spells: list[str]) -> list[str]:
    return (
        list(
            map(lambda s: f"* {s} *", spells)
        )
    )


def mage_stats(mages: list[dict]) -> dict:
    return {
        "max": max(mages, key=lambda a: a["power"])["power"],
        "min": min(mages, key=lambda a: a["power"])["power"],
        "avg": sum(
            map(
                lambda s: s["power"], mages
            )
        ) / len(mages)
    }


def main() -> None:
    artifacts = [
        {"name": "Crystal Orb", "power": 85, "type": "magic"},
        {"name": "Fire Staff", "power": 92, "type": "weapon"},
        {"name": "Ancient Tome", "power": 70, "type": "book"},
    ]

    mages = [
        {"name": "Aelith", "power": 90, "element": "fire"},
        {"name": "Borin", "power": 60, "element": "earth"},
        {"name": "Ciri", "power": 75, "element": "water"},
    ]

    spells = ["fireball", "heal", "shield"]

    print("Testing artifact sorter...")
    sorted_artifacts = artifact_sorter(artifacts)
    for a in sorted_artifacts:
        print(f"{a['name']} ({a['power']} power)")

    print("\nTesting power filter...")
    print(power_filter(mages, 70))

    print("\nTesting spell transformer...")
    print(spell_transformer(spells))

    print("\nTesting mage stats...")
    print(mage_stats(mages))


if __name__ == "__main__":
    main()
