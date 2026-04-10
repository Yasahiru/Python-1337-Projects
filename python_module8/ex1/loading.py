import importlib.util
from typing import Dict, Any
import sys


dependencies: dict[str, str] = {
        "pandas": "Data manipulation ready",
        "numpy": "Numerical computation ready",
        "matplotlib": "Visualization ready",
        "requests": "Network access ready"
    }

missing: list[str] = []


def dependencie_check() -> bool:
    print("Checking dependencies:")
    for pkg, status in dependencies.items():
        spec = importlib.util.find_spec(pkg)
        if spec is not None:
            try:
                version = importlib.metadata.version(pkg)
                print(f"[OK] {pkg} ({version} - {status})")
            except importlib.metadata.PackageNotFoundError:
                print(f"[ERROR] {pkg} found but version inaccessible.")
                missing.append(pkg)
        else:
            missing.append(pkg)

    if missing:
        print()
        print(f"CRITICAL FAILURE: Missing dependencies: {', '.join(missing)}")
        print()
        print("To enter the construct with all programs, run:")
        print("For pip users:    pip install -r requirements.txt")
        print("For Poetry users: poetry install")
        sys.exit(1)


def fetch_matrix_data() -> Dict[str, Any]:
    ...


def main() -> None:
    print("LOADING STATUS: Loading programs...")
    dependencie_check()
    # fetch_matrix_data()
    # print("Analysis complete!")
    # print("Results saved to: matrix_analysis.png")


if __name__ == "__main__":
    main()
