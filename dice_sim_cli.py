import random

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

def main():
    print("Welcome to the Dice Simulation Tool!")

    try:
        # Attack Phase
        print("\nAttack Phase:")
        attack_dice = int(input("Enter the number of attack dice: "))
        quality_stat = int(input("Enter the quality stat (threshold for attack to succeed): "))

        if not (1 <= quality_stat <= 6):
            raise ValueError("Quality stat must be between 1 and 6.")

        attack_probability = calculate_probability(quality_stat)
        expected_hits = attack_dice * attack_probability
        simulated_hits = perform_simulations(attack_dice, quality_stat)
        attack_rolls, hits = roll_dice(attack_dice, quality_stat)

        print(f"\nExpected Hits: {expected_hits:.2f}")
        print(f"Simulated Average Hits (100 rolls): {simulated_hits:.2f}")
        print(f"Attack Rolls: {attack_rolls}")
        print(f"Hits: {hits}")

        # Allow manual adjustment of hits
        adjust_hits = input("Do you want to manually adjust the number of hits? (yes/no or 1/0): ").strip().lower()
        if adjust_hits in ['yes', '1']:
            hits = int(input("Enter the adjusted number of hits: "))
            if hits < 0:
                raise ValueError("Adjusted hits cannot be negative.")
            print(f"Hits manually adjusted to: {hits}")

        if hits == 0:
            print("No hits were made. Attack ends here.")
            return

        # Defense Phase
        print("\nDefense Phase:")
        defense_stat = int(input("Enter the defense stat (threshold for defense to succeed): "))

        if not (1 <= defense_stat <= 6):
            raise ValueError("Defense stat must be between 1 and 6.")

        defense_probability = calculate_probability(defense_stat)
        expected_saves = hits * defense_probability
        simulated_saves = perform_simulations(hits, defense_stat)
        defense_rolls, saves = roll_dice(hits, defense_stat)
        wounds = hits - saves

        print(f"\nExpected Saves: {expected_saves:.2f}")
        print(f"Simulated Average Saves (100 rolls): {simulated_saves:.2f}")
        print(f"Defense Rolls: {defense_rolls}")
        print(f"Saves: {saves}")
        print(f"Wounds: {wounds}")

        # Summary
        print("\nSummary:")
        print(f"Total Hits: {hits}")
        print(f"Total Saves: {saves}")
        print(f"Total Wounds: {wounds}")
        print(f"\nExpected Wounds: {hits - expected_saves:.2f}")

    except ValueError as e:
        print(f"Input Error: {e}")

if __name__ == "__main__":
    main()
