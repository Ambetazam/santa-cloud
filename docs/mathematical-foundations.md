# Mathematical Foundations
## Santa 2026 — The Elf Calculator

**Research area:** Arithmetic Program Synthesis and Mathematical Optimization  
**Project:** Santa 2026 — The Elf Calculator  
**Status:** Foundational research document  
**Version:** 1.0

---

## 1. Introduction

The Elf Calculator presents an interesting mathematical and computational problem: given a finite collection of initial integers, construct a program that produces a required collection of target integers while minimizing the number of arithmetic instructions.

Although the permitted operations are elementary, the optimization problem is not.

The challenge involves several interconnected mathematical disciplines:

- Classical algebra.
- Elementary number theory.
- Integer arithmetic.
- Addition chains and multiplication chains.
- Algebraic identities.
- Arithmetic circuits.
- Combinatorial optimization.
- Program synthesis.

This research investigates how mathematical properties can be transformed into efficient computational constructions.

The central research question is:

> How can we exploit the mathematical structure of initial values and target values to construct valid arithmetic programs with the smallest possible number of instructions?

The purpose of this document is to establish the theoretical foundations needed to investigate that question rigorously.

## 2. Formal Mathematical Model

### 2.1 Initial state

Let a puzzle be represented by:

\[
P=(I,T,R,M)
\]

where:

- \(I\) is the collection of initial integer values.
- \(T\) is the collection of required target values.
- \(R\) is the number of available registers.
- \(M\) is the maximum permitted register value.

Each register contains a positive integer.

The initial state can be represented as:

\[
S_0=(r_0,r_1,\ldots,r_{R-1})
\]

Only the registers initialized by the puzzle are initially available as sources.

### 2.2 Arithmetic instruction

An instruction has the form:

\[
(\operatorname{op},a,b,d)
\]

where:

- \(\operatorname{op}\) is an arithmetic operation.
- \(a\) is the first source register.
- \(b\) is the second source register.
- \(d\) is the destination register.

The supported operations are:

\[
\{+,-,\times,\div\}
\]

The resulting value is:

\[
r_d \leftarrow r_a \operatorname{op} r_b
\]

Both source values are read before the destination register is overwritten.

This allows destination-register aliasing.

For example:

\[
r_0 \leftarrow r_0+r_0
\]

doubles a value without requiring a separate destination register.

### 2.3 Operational constraints

Every instruction must satisfy the following conditions:

1. Both source registers must contain initialized values.
2. The operation must be supported.
3. The result must be a positive integer.
4. The result must not exceed \(M\).
5. Division must be exact.
6. The destination must be a valid register.

For subtraction:

\[
a-b>0
\]

For exact division:

\[
a\bmod b=0,\qquad b>0
\]

and:

\[
\frac{a}{b}>0
\]

### 2.4 Optimization objective

Let \(A(P)\) be a valid arithmetic program for puzzle \(P\).

Define:

\[
C(A(P))=\text{number of instructions in }A(P)
\]

The optimization objective is:

\[
\boxed{
\min_{A(P)} C(A(P))
}
\]

subject to all puzzle constraints and complete target coverage.

For the competition, the aggregate objective is:

\[
\boxed{
\min \sum_{i=1}^{1000} C(A(P_i))
}
\]

This distinction is important: finding a valid program and finding a minimum-cost program are different problems.

---

## 3. Fundamental Lower Bound

One of our first verified mathematical results concerns the minimum number of instructions required by any valid program.

Let:

- \(I\) be the set of initially available values.
- \(T\) be the set of distinct target values.

The targets already available initially require no additional instructions.

Therefore, the missing targets are:

\[
T_{\mathrm{missing}}=T\setminus I
\]

Every missing target must be produced by an arithmetic instruction.

Since each instruction writes exactly one result into one destination register, one instruction cannot produce two different numerical target values.

Consequently:

\[
\boxed{
L(P)=|T\setminus I|
}
\]

is a lower bound on the instruction count.

### 3.1 Proof

Let:

\[
k=|T\setminus I|
\]

Suppose a valid program uses fewer than \(k\) instructions.

Each instruction can produce at most one distinct result value. Therefore, a program with fewer than \(k\) instructions can produce at most \(k-1\) distinct new values.

However, the puzzle requires all \(k\) missing target values.

At least one required target would therefore remain unproduced.

This contradicts the assumption that the program is valid.

Thus:

\[
C(A(P))\geq |T\setminus I|
\]

for every valid program \(A(P)\).

Hence:

\[
\boxed{C(A(P))\geq L(P)}
\]

Q.E.D.

### 3.2 Important interpretation

This lower bound is universal, but it is not necessarily attainable.

To attain it, every instruction must directly produce a different missing target without requiring additional intermediate values.

If a target requires constructing an intermediate value first, the program must use more instructions than the lower bound.

### 3.3 Experimental verification

The practice dataset contains 200 puzzles.

| Measurement | Result |
|---|---:|
| Puzzles analyzed | 200 |
| Target occurrences | 5,294 |
| Initially satisfied targets | 6 |
| Calculated lower bound | 5,288 |
| Sum of supplied lower bounds | 5,288 |
| Exact matches | 200 / 200 |

Every supplied lower bound matched the independently calculated value.

This provides an experimentally verified reference for subsequent optimization research.

---

## 4. Classical Algebra

Our first major mathematical reference is Aurelio Baldor's *Álgebra*.

The book provides a systematic introduction to algebraic operations, powers, products, factorization, equations, and mathematical identities.

For this project, we are particularly interested in algebraic transformations that can be translated into shorter arithmetic programs.

### 4.1 Addition and subtraction

The fundamental additive relationship is:

\[
a+b=c
\]

and its inverse:

\[
c-b=a
\]

Subtraction allows us to construct values by approaching them from above.

For example:

\[
127=128-1
\]

If the initial register contains \(1\), we can construct 128 through repeated doubling and then subtract 1.

An illustrative sequence is:

\[
1\rightarrow2\rightarrow4\rightarrow8\rightarrow16
\rightarrow32\rightarrow64\rightarrow128
\]

Then:

\[
128-1=127
\]

This requires seven doubling instructions and one subtraction instruction.

The complete construction uses eight instructions, assuming enough registers and that the value limit permits 128.

This example illustrates an important principle:

> A target does not necessarily need to be constructed through a sequence of values smaller than itself.

Sometimes constructing
