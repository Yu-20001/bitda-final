from pathlib import Path

from amm_sim.experiments import generate_all
from amm_sim.plotting import generate_figures


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    frames = generate_all(root / "config/scenarios.yaml", root / "results/data")
    generate_figures(frames, root / "results/figures")
    for name, frame in frames.items():
        print(f"{name}: {len(frame)} rows")


if __name__ == "__main__":
    main()
