import math
import matplotlib.pyplot as plt
import enumeration
import analysis
import sys

Epsilon = 1

sequence = sys.argv[1]

temperature_values = [5.0, 4.0, 3.0, 2.0, 1.5, 1.2, 1.0, 0.8, 0.6]


def calculate_Cv_temperature(paths, sequence, Epsilon, T):
    """
    Heat capacity from energy fluctuations using temperature:
        Cv = (<E^2> - <E>^2) / T^2
    with Boltzmann weight exp(-E / T).
    Assumes k_B = 1.
    """
    Z = 0.0
    avg_E = 0.0
    avg_E2 = 0.0

    for path in paths:
        energy = analysis.hp_contacts(path, sequence, Epsilon)
        weight = math.exp(-energy / T)

        Z += weight
        avg_E += energy * weight
        avg_E2 += energy * energy * weight

    avg_E /= Z
    avg_E2 /= Z

    Cv = (avg_E2 - avg_E * avg_E) / (T * T)
    return Cv


all_paths = enumeration.enumerate_paths(sequence)

T_plot = []
Rg_values = []
Cv_values = []

for T in temperature_values:
    Beta = 1.0 / T
    avg_rg = analysis.average_rg(all_paths, sequence, Epsilon, Beta)
    Cv = calculate_Cv_temperature(all_paths, sequence, Epsilon, T)

    T_plot.append(T)
    Rg_values.append(avg_rg)
    Cv_values.append(Cv)

print("Sequence =", sequence)
print("Number of paths =", len(all_paths))
print()
print("Temperature    Average_Rg    Cv")

for i in range(len(T_plot)):
    print(f"{T_plot[i]:.6f}    {Rg_values[i]:.6f}    {Cv_values[i]:.6f}")

print()

plt.figure()
plt.plot(T_plot, Rg_values, marker='o')
plt.xlabel("Temperature")
plt.ylabel("Average Radius of Gyration")
plt.title("Rg vs Temperature for " + sequence)
plt.grid(True)
plt.savefig(sequence + "_Rg_vs_T.png")
plt.close()

plt.figure()
plt.plot(T_plot, Cv_values, marker='o')
plt.xlabel("Temperature")
plt.ylabel("Cv")
plt.title("Cv vs Temperature for " + sequence)
plt.grid(True)
plt.savefig(sequence + "_Cv_vs_T.png")
plt.close()

print("Saved:", sequence + "_Rg_vs_T.png")
print("Saved:", sequence + "_Cv_vs_T.png")