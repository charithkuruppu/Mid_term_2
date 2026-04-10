import math

files = ["1.txt", "2.txt", "3.txt", "4.txt", "5.txt",
         "6.txt", "7.txt", "8.txt", "9.txt", "10.txt"]

steps_list = []

for filename in files:
    with open(filename, "r") as f:
        for line in f:
            if "Steps used" in line:
                value = int(line.strip().split("=")[1])
                steps_list.append(value)

n = len(steps_list)

mean_steps = sum(steps_list) / n
variance = sum((x - mean_steps) ** 2 for x in steps_list) / (n - 1)
std_steps = math.sqrt(variance)
sem_steps = std_steps / math.sqrt(n)

print("Steps used values:", steps_list)
print("Mean =", mean_steps)
print("Standard deviation =", std_steps)
print()
print("Standard Error of the Mean =", sem_steps)
print()
print("Mean ± SEM = " + str(mean_steps) + " ± " + str(sem_steps))