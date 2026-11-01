
import tkinter as tk
from tkinter import ttk, messagebox

from Zone_splitting_Ibrahim import (
    network_given_pupulation,
    active_phone_users_in_city_A
)

def calculate():
    try:
        F = int(buffering.get())
        B = float(blocking.get())

        population = int(population_entry.get())
        mobile_fraction = float(mobile_entry.get())
        callers_fraction = float(callers_entry.get())
        minutes = float(minutes_entry.get())
        N = int(channels_entry.get())
        Z = float(area_entry.get())

        if population <= 0 or N <= 0 or Z <= 0 or minutes <= 0:
            raise ValueError("Inputs must be positive")

        if not (0 <= mobile_fraction <= 1 and 0 <= callers_fraction <= 1):
            raise ValueError("Fractions must be between 0 and 1")

        A = active_phone_users_in_city_A(
            population,
            mobile_fraction,
            callers_fraction,
            average_call_minutes=minutes
        )

        n, k, C, R, z = network_given_pupulation(
            spectrum_channels_N=N,
            blocking_rate_B=B,
            active_phone_users_in_city_A=A,
            Zone_area_Z=Z,
            buffering_distance=F
        )

        results.set(
            f"Offered city traffic (A): {A:.2f} Erlangs\n"
            f"Channels per cell (n): {n}\n"
            f"Carried traffic per cell (k): {k:.4f} Erlangs\n"
            f"Number of cells (C): {C}\n"
            f"Frequency reuse (R): {R:.4f}\n"
            f"Area per cell (z): {z:.4f} km²"
        )

    except ValueError as error:
        messagebox.showerror("Invalid input", str(error))


root = tk.Tk()
root.title("Cellular Network Zone Splitting")
root.geometry("480x620")

frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

ttk.Label(
    frame,
    text="Cellular Network Zone Splitting",
    font=("Arial", 16, "bold")
).pack(pady=10)

buffering = tk.StringVar(value="1")
blocking = tk.StringVar(value="0.01")
results = tk.StringVar(value="Results will appear here")

def add_field(label, default):
    ttk.Label(frame, text=label).pack(anchor="w", pady=(8, 0))
    entry = ttk.Entry(frame)
    entry.insert(0, default)
    entry.pack(fill="x")
    return entry

ttk.Label(frame, text="Buffering distance (F)").pack(anchor="w")
ttk.Radiobutton(
    frame, text="1 layer (U=4)",
    variable=buffering, value="1"
).pack(anchor="w")
ttk.Radiobutton(
    frame, text="2 layers (U=7)",
    variable=buffering, value="2"
).pack(anchor="w")

ttk.Label(frame, text="Acceptable blocking").pack(anchor="w")
ttk.Radiobutton(
    frame, text="1%",
    variable=blocking, value="0.01"
).pack(anchor="w")
ttk.Radiobutton(
    frame, text="0.1%",
    variable=blocking, value="0.001"
).pack(anchor="w")

population_entry = add_field("Population", "100000")
mobile_entry = add_field("Mobile-user fraction", "0.5")
callers_entry = add_field("Calling-user fraction", "0.5")
minutes_entry = add_field("Average call duration (minutes)", "3")
channels_entry = add_field("Spectrum channels (N)", "360")
area_entry = add_field("Zone area (km²)", "632")

ttk.Button(
    frame, text="Calculate",
    command=calculate
).pack(pady=15)

ttk.Label(
    frame,
    textvariable=results,
    justify="left"
).pack(anchor="w")

root.mainloop()
