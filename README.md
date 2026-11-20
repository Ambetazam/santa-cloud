# Santa 2026 — The Elf Calculator

**Mathematical Optimization · Arithmetic Program Synthesis · Computational Research**

An independent research project exploring arithmetic program synthesis, mathematical identities, and instruction-count optimization for the [Santa 2026 — The Elf Calculator](https://www.kaggle.com/competitions/santa-2026) Kaggle competition.

The project investigates how classical algebraic techniques, arithmetic transformations, algorithm design, and computational experimentation can produce shorter and more efficient programs for a constrained arithmetic machine.

Our objective is twofold:

1. Develop competitive, correct, and efficient solutions to the Elf Calculator challenge.
2. Build a reproducible body of mathematical and computational research that can be studied, evaluated, and extended by the wider community.

---

## Table of Contents

- [Research Vision](#research-vision)
- [The Elf Calculator Problem](#the-elf-calculator-problem)
- [Mathematical Foundations](#mathematical-foundations)
- [Research Questions](#research-questions)
- [Verified Results](#verified-results)
- [Research Methodology](#research-methodology)
- [Project Architecture](#project-architecture)
- [Development Environment](#development-environment)
- [Getting Started](#getting-started)
- [Validation](#validation)
- [Experimental Principles](#experimental-principles)
- [Research References](#research-references)
- [Reproducibility](#reproducibility)
- [Contributing](#contributing)
- [Ethical and Competition Compliance](#ethical-and-competition-compliance)
- [License](#license)

---

## Research Vision

Arithmetic program synthesis is the problem of constructing a sequence of computational operations that produces a required set of numerical results.

The Elf Calculator provides a particularly interesting environment for studying this problem because it imposes strict operational constraints:

- A finite number of registers.
- A restricted arithmetic instruction set.
- Positive integer register values.
- A maximum permitted value.
- Exact integer division.
- A maximum program length.
- An objective that rewards minimizing the number of instructions.

These constraints transform elementary arithmetic into an optimization problem.

We investigate the relationship between algebraic knowledge and computational efficiency:

> Can mathematical identities, arithmetic structure, and shared intermediate computations help us construct the required values using fewer instructions?

The project aims to answer this question through mathematical reasoning, algorithm development, and reproducible experiments.

## The Elf Calculator Problem

Each puzzle provides:

- A collection of initial integer values.
- A set of target values.
- A fixed number of registers.
- A maximum permitted register value.

A program consists of arithmetic instructions:

```text
[operation, source_register_a, source_register_b, destination_register]
```

The supported operations are:

| Operation | Meaning |
|---|---|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Exact integer division |

Each instruction reads its source values and writes its result into a destination register.

The generated program must respect the puzzle's register, arithmetic, and value constraints while producing every required target.

### Optimization objective

The competition objective is to minimize the total number of arithmetic instructions across the scored puzzles.

A valid program is therefore not necessarily an efficient program.

Our research focuses on minimizing the instruction count without compromising correctness.

---

## Mathematical Foundations

We use classical mathematics as a source of computational transformations.

### 1. Arithmetic operations

- Addition and subtraction.
- Multiplication and division.
- Laws of signs.
- Properties of equality.
- Divisibility and integer arithmetic.

### 2. Powers and exponentiation

- Laws of exponents.
- Repeated multiplication.
- Powers of two and other bases.
- Multiplicative decompositions.
- Construction of intermediate powers.

### 3. Factorization and divisibility

- Prime factorization.
- Greatest common divisors.
- Least common multiples.
- Factor relationships.
- Exact quotient construction.

### 4. Algebraic identities

- Difference of squares.
- Perfect square identities.
- Product of binomials.
- Factorization techniques.
- Equivalent arithmetic expressions.

### 5. Computational mathematics

- Addition chains.
- Arithmetic circuit optimization.
- Expression trees and directed acyclic graphs.
- Common subexpression elimination.
- Dynamic programming.
- Search and optimization algorithms.

These subjects provide a bridge between classical algebra and modern computational methods.

---

## Research Questions

The project investigates several hypotheses.

| ID | Research direction | Main question |
|---|---|---|
| HYP-001 | Subtraction | Can differences reduce the cost of constructing targets? |
| HYP-002 | Multiplication chains | Can carefully selected products generate multiple useful values? |
| HYP-003 | Exact division | Can divisibility relationships produce cheaper constructions? |
| HYP-004 | Algebraic identities | Can equivalent expressions reduce instruction counts? |
| HYP-005 | Shared intermediates | How much overhead can shared computational structures eliminate? |
| HYP-006 | Search algorithms | Can systematic search outperform greedy construction? |
| HYP-007 | Hybrid strategies | Can operation-specific algorithms outperform a single general strategy? |

Each hypothesis must be evaluated experimentally. No technique is considered an improvement until it has been tested against a common baseline.

---

## Verified Results

### Practice dataset: lower-bound verification

The first completed mathematical experiment analyzed all 200 practice puzzles.

For a puzzle \(P\), define:

- \(I(P)\): initially available values.
- \(T(P)\): required target values.

Every target not initially available must be produced by an instruction.

Since each instruction writes one result, the number of instructions cannot be lower than the number of distinct missing targets:

\[
L(P)=|T(P)\setminus I(P)|
\]

Our verification established:

| Measurement | Result |
|---|---:|
| Practice puzzles | 200 |
| Total target occurrences | 5,294 |
| Initially satisfied targets | 6 |
| Calculated lower bound | 5,288 |
| Sum of supplied lower bounds | 5,288 |
| Exact matches | 200 / 200 |

All five practice puzzle families matched:

| Family | Verified |
|---|---:|
| Independent | 45 / 45 |
| Mixed | 48 / 48 |
| Multiplicative | 40 / 40 |
| Shared | 51 / 51 |
| Tiny | 16 / 16 |

**Result:** all supplied practice lower bounds matched the independently calculated theoretical minimum.

This establishes a reference point for evaluating future solvers.

### Official sample submission: validation baseline

An independent Python reference validator was developed and used to evaluate the supplied sample submission.

| Measurement | Result |
|---|---:|
| Scored puzzles | 1,000 |
| Valid programs | 1,000 |
| Invalid programs | 0 |
| Total instructions | 1,490,379 |
| Average instructions per puzzle | 1,490.38 |
| Addition instructions | 1,462,481 |
| Subtraction instructions | 0 |
| Multiplication instructions | 26,898 |
| Division instructions | 1,000 |

All 1,000 programs passed the local validator.

The sample's absence of subtraction motivates an investigation into whether subtraction-based constructions can reduce instruction counts.

These results describe the supplied sample and the independent validation implementation. They do not establish an optimal solution or guarantee equivalence with the competition's hidden evaluator.

---

## Research Methodology

Every experiment follows a consistent procedure.

1. **Mathematical formulation:** identify the underlying identity, property, or transformation.
2. **Computational translation:** express the technique using legal calculator instructions.
3. **Implementation:** develop an independent solver or optimization strategy.
4. **Correctness validation:** test generated programs against the reference validator.
5. **Performance measurement:** calculate instruction counts and optimization gaps.
6. **Comparison:** evaluate competing strategies using identical puzzles and constraints.
7. **Documentation:** record results, assumptions, limitations, and reproducibility information.

### Optimization gap

Let:

- \(S(P)\) be the instruction count produced by a solver.
- \(L(P)\) be the theoretical lower bound.

The optimization gap is:

\[
G(P)=S(P)-L(P)
\]

The relative gap is:

\[
R(P)=\frac{S(P)-L(P)}{L(P)}
\]

Our primary objective is to reduce the total instruction count and the associated optimization gap.

---

## Project Architecture

The repository is organized to separate implementation, mathematical research, experiments, and validation.

```text
santa-2026/
├── data/
│   └── .gitkeep
├── docs/
│   ├── competition-rules.md
│   ├── mathematical-foundations.md
│   └── research-methodology.md
├── research/
│   ├── hypotheses/
│   │   ├── subtraction.md
│   │   ├── multiplication.md
│   │   ├── divisibility.md
│   │   ├── algebraic-identities.md
│   │   └── shared-intermediates.md
│   └── results/
│       └── lower-bound-verification.md
├── src/
│   ├── python/
│   │   ├── validator.py
│   │   ├── inspect_practice.py
│   │   └── analyze_lower_bounds.py
│   └── cpp/
│       ├── arithmetic.cpp
│       ├── solver.cpp
│       └── optimizer.cpp
├── tests/
├── submissions/
├── experiments/
├── .gitignore
└── README.md
```

The architecture will evolve as the research develops. Python provides the initial reference implementations and validation tools, while C++ will be considered for computationally intensive search and optimization.

---

## Development Environment

Initial development environment:

| Component | Version / Platform |
|---|---|
| Operating system | Kali Linux |
| Python | 3.14.8 |
| GCC | 16.2.0 |
| CMake | 4.3.4 |
| Initial implementation | Python |
| Planned optimization implementation | C++ |

The initial implementation prioritizes correctness, transparency, and reproducibility over premature performance optimization.

---

## Getting Started

Clone the repository:

```bash
git clone <YOUR_REPOSITORY_URL>
cd santa-2026
```

Inspect the available Python version:

```bash
python3 --version
```

Run the practice dataset inspection:

```bash
python3 src/python/inspect_practice.py
```

Verify the mathematical lower bounds:

```bash
python3 src/python/analyze_lower_bounds.py
```

Validate the supplied sample submission:

```bash
python3 src/python/validator.py
```

The scripts use the Python standard library and do not initially require third-party packages.

Competition data files must be obtained through the official competition platform and stored locally in the expected `data/` directory.

---

## Validation

Correctness is a prerequisite for optimization.

The reference validator checks:

- Program structure.
- Instruction format.
- Supported operations.
- Register indices.
- Source register initialization.
- Destination register validity.
- Positive integer results.
- Exact division.
- Puzzle-specific value limits.
- Target coverage.
- Instruction limits.
- Program size constraints.
- Submission identifier uniqueness and coverage.

Initial target values count as already satisfied.

The validator is an independent implementation of the documented rules, not a replacement for official competition evaluation.

---

## Experimental Principles

To maintain scientific integrity:

- Every experiment must have a clearly defined hypothesis.
- All compared algorithms must use identical puzzle inputs.
- Correctness must be established before performance comparisons.
- Baseline results must be preserved.
- Randomized experiments must record their seeds.
- Performance claims must be supported by recorded measurements.
- Failed experiments and limitations must be documented.
- Competition data and research artifacts must comply with the applicable rules.
- No result should be described as optimal without a corresponding proof.

The project distinguishes between:

- **Verified mathematical results:** supported by mathematical reasoning.
- **Experimental results:** supported by reproducible measurements.
- **Research hypotheses:** proposed techniques awaiting evaluation.
- **Engineering decisions:** implementation choices that may change.

---

## Research References

The following authors and works provide an initial intellectual foundation. Specific editions, publication details, and relevant sections will be recorded as the research bibliography develops.

### Classical algebra and mathematical foundations

- Aurelio Baldor — *Álgebra*. A foundational reference for arithmetic, algebraic identities, equations, powers, and factorization.
- Richard R. P. Pólya — *How to Solve It*. Mathematical problem-solving strategies and heuristic reasoning.
- George Chrystal — *Algebra: An Elementary Text-Book*. Classical algebraic foundations.

### Algorithms and optimization

- Donald E. Knuth — *The Art of Computer Programming*. Algorithm analysis and computational problem-solving.
- Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein — *Introduction to Algorithms*. Algorithm design and analysis.
- Richard Bellman — *Dynamic Programming*. Foundations of dynamic optimization.
- Ronald L. Graham, Donald E. Knuth, and Oren Patashnik — *Concrete Mathematics*. Discrete mathematics and mathematical techniques for computer science.

### Computational arithmetic

- Research on addition chains, arithmetic circuits, expression optimization, and program synthesis will be incorporated as relevant literature is identified and evaluated.

References will be connected to specific research questions rather than included merely as a reading list.

---

## Reproducibility

Research reproducibility is a core project objective.

Each significant experiment should record:

- Experiment identifier.
- Date and software version.
- Dataset and puzzle subset.
- Algorithm and configuration.
- Random seed, where applicable.
- Validation results.
- Instruction counts.
- Lower-bound gaps.
- Runtime and memory measurements, where relevant.
- Conclusions and limitations.

The goal is to allow another researcher to reproduce the experiment and independently evaluate its conclusions.

---

## Contributing

Contributions are welcome in the areas of:

- Mathematical analysis.
- Arithmetic optimization.
- Program synthesis.
- Algorithm design.
- Search strategies.
- Performance evaluation.
- Independent validation.
- Scientific documentation.

Contributions should include a clear explanation of the mathematical or computational idea and reproducible evidence for any claimed improvement.

---

## Ethical and Competition Compliance

This project is developed in accordance with the applicable Kaggle competition rules.

All participants and contributors must respect the competition's data usage, collaboration, submission, and external resource policies.

Competition datasets are not included in this repository unless their redistribution is explicitly permitted.

Any external code, algorithms, datasets, or publications used in the project must be properly documented and attributed.

Before publication or prize submission, the current official competition rules and applicable licensing requirements must be checked.

---

## License

The repository's license will be selected and documented before public release, taking into account the competition's source-code and prize eligibility requirements.

Third-party materials remain subject to their respective licenses and copyright terms.

---

**Research direction:** Explore the intersection of classical algebra, arithmetic program synthesis, and computational optimization through transparent, reproducible experimentation.

**Project status:** Early research and baseline validation.

**Primary objective:** Develop correct and increasingly efficient arithmetic programs while contributing documented mathematical and computational knowledge to the community.
