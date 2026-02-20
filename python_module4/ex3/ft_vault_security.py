
def ft_vault_security():
    try:
        print("Initiating secure vault access...")
        print("Vault connection established with failsafe protocols\n")

        print("SECURE EXTRACTION:")
        file1: any = open("classified_data.txt", "r")
        print(f"{file1.read()}\n")
        file1.close()

        file1 = open("classified_data.txt", "a")
        file2 = open("security_protocols.txt", "r")

        print("SECURE PRESERVATION:")
        print(file2.read())
        file1.write(f"\n{file2.read()}")
        file1.close()
        file2.close()

        print("Vault automatically sealed upon completion")
        print("All vault operations completed with maximum security.")
    except Exception as e:
        print(e)


def main():
    print("=== CYBER ARCHIVES - VAULT SECURITY SYSTEM ===\n")
    ft_vault_security()


if __name__ == "__main__":
    main()
