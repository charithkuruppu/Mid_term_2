from collections import Counter
import math
import analysis


def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def calculate_restraint_energy(path, bead_i, bead_j, k_force):
    """
    Zero when the two chosen beads are adjacent in space (Manhattan distance = 1).
    Otherwise increases quadratically as k_force * (d - 1)^2.
    """
    posi = path[bead_i]
    posj = path[bead_j]
    d = manhattan_distance(posi, posj)

    if d == 1:
        return 0.0
    else:
        return k_force * (d - 1) ** 2


def calculate_energy_with_restraint(sequence, path, Epsilon, bead_i, bead_j, k_force):
    hp_energy = analysis.hp_contacts(path, sequence, Epsilon)
    restraint_energy = calculate_restraint_energy(path, bead_i, bead_j, k_force)
    return hp_energy + restraint_energy


def partition_function_with_restraint(paths, sequence, Beta, Epsilon, bead_i, bead_j, k_force):
    Z = 0.0
    for path in paths:
        E = calculate_energy_with_restraint(sequence, path, Epsilon, bead_i, bead_j, k_force)
        Z += math.exp(-Beta * E)
    return Z


def probability_with_restraint(path, sequence, Z, Beta, Epsilon, bead_i, bead_j, k_force):
    E = calculate_energy_with_restraint(sequence, path, Epsilon, bead_i, bead_j, k_force)
    return math.exp(-Beta * E) / Z


def entropy_term_with_restraint(path, sequence, Z, Beta, Epsilon, bead_i, bead_j, k_force):
    p = probability_with_restraint(path, sequence, Z, Beta, Epsilon, bead_i, bead_j, k_force)
    return p * math.log(p)


def restrained_macrostates_by_energy(paths, sequence, Epsilon, bead_i, bead_j, k_force):
    energies = []
    for path in paths:
        E = calculate_energy_with_restraint(sequence, path, Epsilon, bead_i, bead_j, k_force)
        energies.append(E)
    return Counter(energies)


def lowest_energy_microstates_with_restraint(paths, sequence, Epsilon, bead_i, bead_j, k_force):
    energies = []

    for path in paths:
        E = calculate_energy_with_restraint(sequence, path, Epsilon, bead_i, bead_j, k_force)
        energies.append((E, path))

    min_energy = min(E for E, _ in energies)
    lowest_paths = [path for E, path in energies if E == min_energy]
    degeneracy = len(lowest_paths)

    return min_energy, lowest_paths, degeneracy


def analyze_paths_with_restraint(paths, sequence, Beta, Epsilon, bead_i, bead_j, k_force):
    Z = partition_function_with_restraint(paths, sequence, Beta, Epsilon, bead_i, bead_j, k_force)

    sum_end2end = 0.0
    sum_rg = 0.0
    expected_end2end = 0.0
    expected_rg = 0.0
    expected_energy = 0.0
    entropy1 = 0.0
    energies = []

    for path in paths:
        E = calculate_energy_with_restraint(sequence, path, Epsilon, bead_i, bead_j, k_force)
        p = probability_with_restraint(path, sequence, Z, Beta, Epsilon, bead_i, bead_j, k_force)

        ree = analysis.end_to_end(path)
        rg = analysis.calculate_radius_of_gyration(path)

        sum_end2end += ree
        sum_rg += rg
        expected_end2end += p * ree
        expected_rg += p * rg
        expected_energy += p * E
        entropy1 -= entropy_term_with_restraint(path, sequence, Z, Beta, Epsilon, bead_i, bead_j, k_force)
        energies.append(E)

    macro = Counter(energies)

    results = {
        "Z": Z,
        "n_paths": len(paths),
        "avg_end2end": sum_end2end / len(paths),
        "avg_rg": sum_rg / len(paths),
        "expected_end2end": expected_end2end,
        "expected_rg": expected_rg,
        "expected_energy": expected_energy,
        "S1": entropy1,
        "S2": analysis.entropy_from_definition(expected_energy, Z, Beta),
        "macrostates": macro
    }

    return results