import enumeration
import analysis
import analysis_restrain
import sys

sequence = sys.argv[1]

Epsilon = 1
Beta = 10.0 / 6.0


# Choose two beads far apart in sequence
bead_i = 0
bead_j = len(sequence) - 1

# At least three force constants for Q4
k_values = [0.1, 0.5, 1.0]

all_paths = enumeration.enumerate_paths(sequence)

# -----------------------------
# Unrestrained system
# -----------------------------
results = analysis.analyze_paths(all_paths, sequence, Beta=Beta, Epsilon=Epsilon)
avg_rg = analysis.average_rg(all_paths, sequence, Epsilon=Epsilon, Beta=Beta)
min_energy, lowest_paths = analysis.lowest_energy_microstates(all_paths, sequence, Epsilon=Epsilon)

print("==================================================")
print("UNRESTRAINED SYSTEM")
print("==================================================")
print("Sequence =", sequence)
print("Number of paths =", results["n_paths"])
print("Partition function Z =", results["Z"])
print("Average end-to-end distance =", results["avg_end2end"])
print("Average radius of gyration =", avg_rg)
print("Expected end-to-end distance =", results["expected_end2end"])
print("Expected energy =", results["expected_energy"])
print("Entropy S1 =", results["S1"])
print("Entropy S2 =", results["S2"])

print("\nMacrostates (Energy : Degeneracy)")
for energy in sorted(results["macrostates"]):
    print(f"{energy} : {results['macrostates'][energy]}")

print("Lowest energy =", min_energy)
print("Number of lowest-energy microstates =", len(lowest_paths))
print("\nLowest-energy microstates (unrestrained):")
for i, path in enumerate(lowest_paths, start=1):
    print(f"{path}")

# -----------------------------
# Restrained systems
# -----------------------------
for k_force in k_values:
    restrained_results = analysis_restrain.analyze_paths_with_restraint(
        all_paths, sequence, Beta, Epsilon, bead_i, bead_j, k_force
    )

    min_energy_r, lowest_paths_r, degeneracy_r = analysis_restrain.lowest_energy_microstates_with_restraint(
        all_paths, sequence, Epsilon, bead_i, bead_j, k_force
    )

    print("\n==================================================")
    print(f"RESTRAINED SYSTEM  (k = {k_force})")
    print("==================================================")
    print("Restrained beads (0-based indices) =", bead_i, bead_j)
    print("Restrained beads (human numbering) =", bead_i + 1, bead_j + 1)

    print("Partition function Z =", restrained_results["Z"])
    print("Average end-to-end distance =", restrained_results["avg_end2end"])
    print("Average radius of gyration =", restrained_results["expected_rg"])
    print("Expected end-to-end distance =", restrained_results["expected_end2end"])
    print("Expected energy =", restrained_results["expected_energy"])
    print("Entropy S1 =", restrained_results["S1"])
    print("Entropy S2 =", restrained_results["S2"])

    if restrained_results["Z"] > results["Z"]:
        print("Comparison with unrestrained: Z increased")
    elif restrained_results["Z"] < results["Z"]:
        print("Comparison with unrestrained: Z decreased")
    else:
        print("Comparison with unrestrained: Z unchanged")

    print("\nRestrained macrostates (Energy : Degeneracy)")
    for energy in sorted(restrained_results["macrostates"]):
        print(f"{energy} : {restrained_results['macrostates'][energy]}")

    print("Lowest restrained energy =", min_energy_r)
    print("Degeneracy of lowest restrained energy =", degeneracy_r)
    print("Number of lowest-energy restrained microstates =", len(lowest_paths_r))