# Iteration 3 report source

This folder is a self-contained Overleaf project. The compiled PDF is
[../iteration-3-report.pdf](../iteration-3-report.pdf). The historical Iteration 2
source and signed PDF remain unchanged.

## Build and upload

Keep main.tex beside the figures/ folder. Compile with pdfLaTeX twice, or run
tectonic main.tex from this folder. All packages are standard TeX Live packages.
Copy the resulting main.pdf to ../iteration-3-report.pdf.

For Overleaf, upload the delivered source ZIP as a new project, select main.tex
as the main document, use the pdfLaTeX compiler, and recompile. The ZIP includes
main.tex, this README and all three PNGs. After team review, enable view-only
link sharing and add that link to the repository README and status checklist.
Each student submits the repository link and read-only Overleaf link separately
on Canvas.

The source uses only figures/ as a local dependency. Confirm all references
resolve and visually inspect the PDF after any edits.

## Evidence and numerical provenance

The main numerical tables consistently cite the original stdout at code commit
3a7dc93aecb41656a4ed86f93029cdb301a18199. Derived differences, ratios and storage
shares are labelled. A separate fresh rerun passed all checks and all seven
existing tests. Its logs, versions and source checksums are in
[../verification-2026-11-22/](../verification-2026-11-22/).

| Report material | Script | Original evidence |
|---|---|---|
| Exact worked example and substitution checks | src/small_example.py | outputs/small_example.txt |
| All five current math answers | all three scripts | report Section 3 and the three stdout files |
| Baseline truth/library comparison, three-size sweep and k=8 stress test | src/check_simulation.py | outputs/simulation.txt and simulation_error.png |
| Image cleaning, reconstructions, energy, errors and storage | src/run_real.py | outputs/real_image.txt, image_reconstructions.png and image_energy.png |
| Verification and assumption tables | all three scripts | original stdout, with fresh results separately identified |
| Seven regression tests | python -m unittest discover -s tests -v | docs/verification-2026-11-22/unittest.txt |

Run commands from the repository root as shown in the root README. Script runs
create plots in outputs/; capture stdout explicitly if updating the saved logs.
Floating-point final digits and compressed NPZ sizes can change across versions.
Keep the distinction between a committed run and a fresh run explicit rather
than mixing values from different runs in one table.

When refreshing the report, update repeated values consistently in prose and
tables, recalculate labelled derived arithmetic, copy updated PNGs into figures/,
and compile and visually inspect again.

## Team confirmations

Jiaxiao Chen is the confirmed Iteration 3 leader. The instructor's unused-leader
rule remains unresolved because both members have already led. The user confirmed
equal overall contributions of 50% each. The positive technical review is supported
by the verified results. Student peer-check details remain separate; no student
signatures or task-specific contributions have been invented.
