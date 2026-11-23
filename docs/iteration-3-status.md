# Iteration 3 status and requirements

Snapshot: 22 November 2026. Implementation reviewed:
3a7dc93aecb41656a4ed86f93029cdb301a18199.

The non-code deliverables are prepared and reviewed. The original implementation,
tests, data, saved outputs and Iteration 2 source/PDF are preserved.

| Deliverable | Evidence |
|---|---|
| Compiled report | [iteration-3-report.pdf](iteration-3-report.pdf) |
| Portable Overleaf source and figures | [iteration-3/main.tex](iteration-3/main.tex), [build/upload instructions](iteration-3/README.md) |
| Updated Excel task plan, timeline and contributions | [project-plan.xlsx](project-plan.xlsx); historical content preserved |
| Fresh independent verification logs and source hashes | [verification-2026-11-22/](verification-2026-11-22/) |
| Run instructions and results links | [repository README](../README.md) |

## Assignment coverage

| Handout requirement | Result |
|---|---|
| Small worked example with every intermediate and second-way check | Report Section 2: Gram matrix, characteristic polynomial, eigenvalues/vectors, AV, U, Sigma, fractional A1, residual and exact squared error 5; substitution and shared-solver checks |
| Current Iteration 3 math questions | Section 3 explicitly answers the five Project 3 prompts: tiny SVD, rank-one error, power/deflation implementation, paired signs/subspaces, and 95% image energy |
| Equations mapped to numbered algorithm steps | Section 4, Table 3, and existing src/methods.py |
| Preserved simulation model, parameters and seed | Section 5: 120 x 80, rank 5, noise SD 0.01, seed 0, draw order L/R/Z |
| Truth and library comparisons, at least three sizes, log-log plot | Section 5 and Figure 1; widths 20/80/320, height 1.5n, ten seeds per size |
| Stress test with broken separation assumption | k=8: all stopping checks converge; noise modes require 436/1069/1752 steps. Their separate library accuracy is not asserted |
| Real image cleaning and verification | Section 6: same grayscale camera image, uint8 / 255 to float64, zero missing values, no removed pixels or split |
| Required reconstructions, energy and storage | Figures 2-3 and Table 6: k=5/20/50 and k95=3; scalar, raw-byte and measured NPZ costs |
| Verification table with differences and pass rules | Section 7, Table 7; all listed checks pass; sign and paired-subspace handling matches the code |
| Simulation-first and real-data assumption checks | Section 8, Table 8 |
| Assumptions and limitations | Sections 5-9 distinguish noise error from rounding, dimension growth from ordinary sampling, display clipping from raw loss, scalar counts from bytes, and energy from visual quality |
| Leadership and contribution record | Section 10 and Excel plan record confirmed facts and editable member fields |
| Reproducibility and fresh verification | Section 11; all three scripts exited successfully and all seven existing tests passed |

The PDF was compiled with Tectonic, checked for unresolved references and
overflowing content, and visually reviewed across all pages. The Overleaf ZIP
contains the same source and all required figures.

## Confirmed leadership and remaining course actions

Jiaxiao Chen leads Iteration 3 and also led Iteration 1, as confirmed by the user.
Alexander Rees led Iteration 2. The handout asks for a member who has not led
before. Neither current member qualifies, so an instructor exception or alternate
instruction remains necessary. No exception has been claimed.

| Remaining action | Who completes it |
|---|---|
| Resolve and record the leader-rotation exception | Team / instructor |
| Confirm each member's actual math and code work | Each student, in report Table 9 and the Excel plan |
| Record the other student's actual check | Each student; AI review is separate |
| Upload reviewed sources to Overleaf and verify the view-only link | Team |
| Submit repository and Overleaf read-only links to Canvas | Jiaxiao Chen and Alexander Rees, separately |

At the user's request, Claude assisted with drafting and Codex performed the
independent mathematical, numerical and document review. This does not certify
student ownership or replace the required second-member check. No student
signatures, contributions, Overleaf publication, or Canvas submissions were
invented.
