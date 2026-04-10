from typing import Dict, Any, Final
import matplotlib.pyplot as plt
import importlib.metadata
import importlib.util
import pandas as pd
import numpy as np
import sys


dependencies: dict[str, str] = {
        "pandas": "Data manipulation ready",
        "numpy": "Numerical computation ready",
        "matplotlib": "Visualization ready",
        "requests": "Network access ready"
    }

missing: list[str] = []


def dependencie_check() -> None:
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
            print()
            print(
                "CRITICAL FAILURE: Missing dependencies: "
                f"{', '.join(missing)}"
            )
            print()
            print("To enter the construct with all programs, run:")
            print("For pip users:    pip install -r requirements.txt")
            print("For Poetry users: poetry install")
            sys.exit(1)


DATA_POINTS: Final[int] = 1000


def fetch_matrix_data() -> Dict[str, Any]:
    """
    Analyzes the distribution of Matrix signals using a Histogram.
    """
    try:
        print(
            "Analyzing Matrix data... Processing "
            f"{DATA_POINTS} data points..."
        )
        raw_signals: np.ndarray = np.random.normal(
            loc=0, scale=1, size=DATA_POINTS
        )
        df: pd.DataFrame = pd.DataFrame(raw_signals, columns=['Frequency'])

        print("Generating visualization...")
        plt.figure(figsize=(10, 6))
        plt.hist(
            df['Frequency'],
            bins=20,
            color='purple',
            edgecolor='black',
            alpha=0.7
        )

        plt.title("Matrix Signal Frequency Distribution")
        plt.xlabel("Signal Intensity")
        plt.ylabel("Occurrences")
        plt.grid(axis='y', alpha=0.3)
        plt.savefig("matrix_analysis.png")
        print("Analysis complete! Results saved to: matrix_analysis.png")

    except Exception as e:
        print(f"CRITICAL ERROR: Data stream corrupted: {e}")


def main() -> None:
    print("LOADING STATUS: Loading programs...")
    dependencie_check()
    fetch_matrix_data()
    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")


if __name__ == "__main__":
    main()
