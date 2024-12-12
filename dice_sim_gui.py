import random
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

def roll_dice(dice_count, threshold):
    """Rolls dice_count number of dice and returns the count of rolls >= threshold."""
    rolls = [random.randint(1, 6) for _ in range(dice_count)]
    successes = [roll for roll in rolls if roll >= threshold]
    return rolls, len(successes)

def calculate_probability(threshold):
    """Calculates the probability of a single die meeting or exceeding the threshold."""
    return max(0, (7 - threshold) / 6)

def perform_simulations(dice_count, threshold, simulations=100):
    """Performs multiple simulations to calculate average results."""
    total_successes = 0
    for _ in range(simulations):
        _, successes = roll_dice(dice_count, threshold)
        total_successes += successes
    return total_successes / simulations

def plot_results(rolls, successes, title):
    """Creates a bar chart of the dice rolls."""
    values = [1, 2, 3, 4, 5, 6]
    counts = [rolls.count(value) for value in values]

    plt.bar(values, counts, color='skyblue', edgecolor='black')
    plt.axhline(len(rolls) / 6, color='red', linestyle='--', label='Average per Face')
    plt.title(f"{title}\nSuccesses: {successes}")
    plt.xlabel("Dice Value")
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()

def simulate():
    try:
        attack_dice = int(entry_attack_dice.get())
        quality_stat = int(entry_quality_stat.get())

        if not (1 <= quality_stat <= 6):
            raise ValueError("Quality stat must be between 1 and 6.")

        # Attack Phase
        attack_probability = calculate_probability(quality_stat)
        expected_hits = attack_dice * attack_probability
        simulated_hits = perform_simulations(attack_dice, quality_stat)
        attack_rolls, hits = roll_dice(attack_dice, quality_stat)

        # Display attack results
        attack_result = (f"Expected Hits: {expected_hits:.2f}\n"
                         f"Simulated Average Hits (100 rolls): {simulated_hits:.2f}\n"
                         f"Hits: {hits}\nRolls: {attack_rolls}")
        lbl_attack_result.config(text=attack_result)
        plot_results(attack_rolls, hits, "Attack Rolls")

        if hits == 0:
            messagebox.showinfo("Simulation Result", "No hits were made. Attack ends here.")
            return

        # Defense Phase
        defense_stat = int(entry_defense_stat.get())
        if not (1 <= defense_stat <= 6):
            raise ValueError("Defense stat must be between 1 and 6.")

        defense_probability = calculate_probability(defense_stat)
        expected_saves = hits * defense_probability
        simulated_saves = perform_simulations(hits, defense_stat)
        defense_rolls, saves = roll_dice(hits, defense_stat)
        wounds = hits - saves

        # Display defense results
        defense_result = (f"Expected Saves: {expected_saves:.2f}\n"
                          f"Simulated Average Saves (100 rolls): {simulated_saves:.2f}\n"
                          f"Saves: {saves}\nWounds: {wounds}\nRolls: {defense_rolls}")
        lbl_defense_result.config(text=defense_result)
        plot_results(defense_rolls, saves, "Defense Rolls")

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("Dice Simulation Tool")

# Attack Phase Inputs
frame_attack = tk.Frame(root)
frame_attack.pack(pady=10)

lbl_attack_title = tk.Label(frame_attack, text="Attack Phase", font=("Arial", 14))
lbl_attack_title.pack()

lbl_attack_dice = tk.Label(frame_attack, text="Number of Attack Dice:")
lbl_attack_dice.pack()
entry_attack_dice = tk.Entry(frame_attack)
entry_attack_dice.pack()

lbl_quality_stat = tk.Label(frame_attack, text="Quality Stat (Threshold for Success):")
lbl_quality_stat.pack()
entry_quality_stat = tk.Entry(frame_attack)
entry_quality_stat.pack()

lbl_attack_result = tk.Label(frame_attack, text="", font=("Arial", 10), fg="blue")
lbl_attack_result.pack(pady=5)

# Defense Phase Inputs
frame_defense = tk.Frame(root)
frame_defense.pack(pady=10)

lbl_defense_title = tk.Label(frame_defense, text="Defense Phase", font=("Arial", 14))
lbl_defense_title.pack()

lbl_defense_stat = tk.Label(frame_defense, text="Defense Stat (Threshold for Success):")
lbl_defense_stat.pack()
entry_defense_stat = tk.Entry(frame_defense)
entry_defense_stat.pack()

lbl_defense_result = tk.Label(frame_defense, text="", font=("Arial", 10), fg="green")
lbl_defense_result.pack(pady=5)

# Simulate Button
btn_simulate = tk.Button(root, text="Simulate", command=simulate, bg="lightgreen")
btn_simulate.pack(pady=10)

# Run the GUI
root.mainloop()
