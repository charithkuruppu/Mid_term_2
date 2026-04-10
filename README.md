# Mid_term_2

This repository contains my answers and code for the **MID_term 2** exam.

The written answers for the exam questions are included in:

- `1_2_4_answers.pdf`
- `3rd_asnwer_MC.pdf`

## Question answers

- Answers for **Questions 1, 2, and 4** are in `1_2_4_answers.pdf`
- The answer for **Question 3 (Monte Carlo part)** is in `3rd_asnwer_MC.pdf`

## Running the exact enumeration code

The `main.py` file can be run by giving a sequence as input.

Example:

python3 main.py HHPHPHPH

This will calculate the results for the given sequence.

The answers and outputs for each sequence are available inside the corresponding sequence directories.

Running the Monte Carlo code

For the Monte Carlo part, run MC.py first by giving:

the sequence
the number of MC steps

Example:

python3 MC.py HHPHPHPH 100000

This generates the Monte Carlo trajectory.

After that, run analyze_MC.py by giving:

the sequence
the trajectory file name

Example:

python3 analyze_MC.py HHPHPHPH trajectory.txt

This analyzes the Monte Carlo trajectory for the selected sequence.

Mean and standard deviation files

Inside each sequence directory, there are also files containing the mean and standard deviation calculations.

Plotting

The plot.py file can be run by giving the sequence or sequences as input.

It is used to plot:

Radius of gyration as a function of temperature
Cv for each sequence

Example:

python3 plot.py HHPHPHPH

