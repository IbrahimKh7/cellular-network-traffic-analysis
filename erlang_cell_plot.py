import matplotlib.pyplot as plt

# Your existing code, imported unchanged
from Zone_splitting_Ibrahim import (
    active_phone_users_in_city_A,
    network_given_pupulation,
)


class ErlangCellPlotter:
    """
    Plots city carried traffic K (Erlang) against the number of cells C.

    For every case (blocking G, cells per system unit U) and every average
    call length, one point is computed:
        A = offered city traffic       (active_phone_users_in_city_A)
        C = cells needed               (network_given_pupulation)
        K = carried city traffic = A * (1 - G)
    Each case becomes one line with one marker per call length.
    """

    # buffering_distance 1 -> U = 4 cells/unit, 2 -> U = 7 cells/unit
    DEFAULT_CASES = [
        {"label": "1% blocking, U=4",   "blocking": 0.01,  "buffering_distance": 1},
        {"label": "1% blocking, U=7",   "blocking": 0.01,  "buffering_distance": 2},
        {"label": "0.1% blocking, U=4", "blocking": 0.001, "buffering_distance": 1},
        {"label": "0.1% blocking, U=7", "blocking": 0.001, "buffering_distance": 2},
    ]

    def __init__(
        self,
        population=7_000_000,                     # 7M
        mobile_users_fraction=0.7,
        percent_of_callers_from_mobile_users=0.25,
        average_call_minutes=(0.5, 1, 2, 3),
        spectrum_channels_N=700,                  # city spectrum channels
        zone_area_Z=2000.0,                       # km^2 (only affects z, not K or C)
        cases=None,
    ):
        self.population = population
        self.mobile_users_fraction = mobile_users_fraction
        self.percent_callers = percent_of_callers_from_mobile_users
        self.call_minutes = list(average_call_minutes)
        self.N = spectrum_channels_N
        self.Z = zone_area_Z
        self.cases = cases if cases is not None else self.DEFAULT_CASES
        self.results = {}

    def compute(self):
        """Fill self.results: {case label: [row, row, ...]} one row per call length."""
        self.results = {}
        for case in self.cases:
            B = case["blocking"]
            rows = []
            for minutes in self.call_minutes:
                A = active_phone_users_in_city_A(
                    self.population,
                    self.mobile_users_fraction,
                    self.percent_callers,
                    minutes,
                )
                n, k, C, R, z = network_given_pupulation(
                    self.N, B, A, self.Z, case["buffering_distance"]
                )
                rows.append({
                    "minutes": minutes, "A": A, "K": A * (1 - B),
                    "C": C, "n": n, "k": k, "R": R, "z": z,
                })
            self.results[case["label"]] = rows
        return self.results

    def print_table(self):
        if not self.results:
            self.compute()
        for label, rows in self.results.items():
            print(f"\n{label}")
            print(f"{'min':>5} {'A':>10} {'K':>10} {'C':>6} {'n':>5}")
            for r in rows:
                print(f"{r['minutes']:>5} {r['A']:>10.1f} {r['K']:>10.1f} "
                      f"{r['C']:>6} {r['n']:>5}")

    def plot(self, save_path=None, show=True):
        if not self.results:
            self.compute()

        fig, ax = plt.subplots(figsize=(10, 6))
        markers = ["o", "s", "^", "D"]

        for i, (label, rows) in enumerate(self.results.items()):
            C_vals = [r["C"] for r in rows]
            K_vals = [r["K"] for r in rows]
            ax.plot(K_vals, C_vals, marker=markers[i % len(markers)], label=label)
            for r in rows:
                ax.annotate(f"{r['minutes']} min", (r["K"], r["C"]),
                            textcoords="offset points", xytext=(5, -12), fontsize=7)

        ax.set_xlabel("Carried city traffic, K (Erlang)")
        ax.set_ylabel("Number of cells, C")
        ax.set_title("Number of cells C vs carried traffic K "
                     f"(N = {self.N} channels, Z = {self.Z:g} km²)")
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.tight_layout()

        if save_path:
            fig.savefig(save_path, dpi=200)
        if show:
            plt.show()
        return fig, ax


if __name__ == "__main__":
    plotter = ErlangCellPlotter()
    plotter.print_table()
    plotter.plot(save_path="K_vs_C.png")
