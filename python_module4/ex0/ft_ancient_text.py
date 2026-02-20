
def ft_ancient_text():
    try:
        print("Accessing Storage Vault: ancient_fragment.txt")
        print("Connection established...\n")
        print("RECOVERED DATA:")

        f = open("ancient_fragment.txt", "r")
        print(f.read())

    except FileNotFoundError as e:
        print(e)
    finally:
        print("\nData recovery complete. Storage unit disconnected.")
        f.close()


def main():
    print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===\n")
    ft_ancient_text()


if __name__ == "__main__":
    main()
