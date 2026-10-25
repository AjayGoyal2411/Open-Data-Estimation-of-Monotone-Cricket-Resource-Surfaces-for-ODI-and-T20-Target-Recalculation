# Cricket resource estimation and target recalculation

MATLAB source code supporting *Estimating monotone batting resources from open data for One Day International and Twenty20 target recalculation*.

Code: https://github.com/AjayGoyal2411/Open-Data-Estimation-of-Monotone-Cricket-Resource-Surfaces-for-ODI-and-T20-Target-Recalculation

Analytical materials: https://doi.org/10.5281/zenodo.23617887

All versions of the analytical record: https://doi.org/10.5281/zenodo.23617886

## Scope

The repository contains 27 step-specific ZIP archives. Extract the archives before using the source; the functions cannot be called from inside a ZIP. Each archive contains a Step directory with MATLAB files under Code. Preserve their filenames because the functions call one another. The accompanying FROZEN_CODE_LOCATIONS.csv maps all 87 files in the retained-model checksum record to their step archives. All 87 matched the archived SHA-256 checksums during the 25 October 2026 submission review. This check established source identity; it did not rerun model estimation.

## Computing environment and dependencies

The recorded analysis used MATLAB R2024b Update 1. Constrained estimation uses Optimization Toolbox functions, including quadprog and fmincon. The initial YAML import uses a SnakeYAML Java archive located in the configured project lib directory; that third-party dependency and the raw Cricsheet records must be obtained separately under their own terms. Inspect the source headers and configuration functions for stage-specific requirements. In MATLAB, matlab.codetools.requiredFilesAndProducts can help inspect the dependencies of an entry point; this is not a substitute for running it with the required inputs.

The archived project root was D:\VihaanProject1. Paths and configuration conventions differ between early scripts and later functions. Review the relevant settings before execution. Do not overwrite retained results or change model-integrity records merely to bypass a missing-file or hash check.

## Data and extraction

Only S1 is a journal supporting-information upload. The external files retain legacy S2–S7 filenames:

| Manuscript label | Zenodo filename | Contents |
|---|---|---|
| Repository File 1 | S2_Supporting_Information_Data.zip | Retained models, coefficients, numerical results, source inventory, reference inputs and earlier-fit diagnostics |
| Repository File 2 | S3_Supporting_Information.docx | Equation sources and derivations |
| Repository File 3 | S4_Supporting_Information.zip | Fixed 2024–2025 prediction artifacts |
| Repository File 4 | S5_Supporting_Information.zip | Reports for Steps 9–12 |
| Repository File 5 | S6_Supporting_Information.zip | Reports for Step 13 |
| Repository File 6 | S7_Supporting_Information.zip | Reports for Steps 14–23 |

Extract the five ZIP files into the same parent directory. They merge into S5_File_Reproducibility; that internal directory name is historical, not a current supplement number. Read README_S2_Data.txt before restoring the reference inputs or retained model directory. Where a retained-model integrity check expects a source file beneath a `frozen_models/<build>/code` directory, use the paths in `Retained_Model_Boundary.csv` and the matching step-archive locations in `FROZEN_CODE_LOCATIONS.csv`. Restore the exact source bytes; do not rename the functions or edit the checksum records. These path-restoration instructions have not been verified by a fresh model run. The mathematical document is separate from the ZIP extraction tree.

## Execution and analytical stages

These stages form a dependent analytical workflow. A configuration file is not itself a full analysis. Inspect each source header for the call signature and required predecessor inputs. Later stages often require saved MAT objects, state partitions or an integrity-checked retained-model directory. Add the required extracted Code directories to the MATLAB path before calling their functions. Run the supplied self-test functions where present, then the applicable entry point with the documented inputs.

| Step | Purpose | Configuration or execution files |
|---|---|---|
| 1 | Import Cricsheet YAML | `Step1_20052026.m` |
| 2 | Extract Competition Metadata | `Step2_20052026.m` |
| 3 | Prepare Match Metadata | `Step3_20052026.m` |
| 4 | Consolidate Retained Data | `Step4_20052026.m` |
| 5 | Inspect Retained Data | `Step5_20052026.m` |
| 6 | Describe Recorded Matches | `Step6_20052026.m` |
| 7 | Explore Resource Surfaces | `Step7_20052026.m` |
| 8 | Audit Cohorts and Chronology | `RevisedCodes_Step8A_PrerequisiteAudit.m`, `RevisedCodes_Step8_PoolingAuditSplits.m` |
| 9 | Construct States and Context | `RevisedCodes_09_00_Config.m` |
| 10 | Estimate Empirical Resources | `RevisedCodes_10_RunAll.m`, `RevisedCodes_10_00_Config.m` |
| 11 | Verify Resource References | `RevisedCodes_11_RunAll.m`, `RevisedCodes_11_00_Config.m` |
| 12 | Fit Candidate Models | `RevisedCodes_12_00_Config.m`, `RevisedCodes_12_RunAll.m` |
| 13 | Assess Resource Approximation | `RevisedCodes_13_00_Config.m`, `RevisedCodes_13_14_RunAll.m`, `RevisedCodes_13_RunAll.m` |
| 14 | Calculate Interruption Targets | `RevisedCodes_14_00_Config.m`, `RevisedCodes_14_RunAll.m` |
| 15 | Evaluate Development Prediction | `RevisedCodes_15_16_RunAll.m`, `RevisedCodes_15_00_Config.m`, `RevisedCodes_15_RunAll.m` |
| 16 | Assess Estimation Sensitivity | `RevisedCodes_16_RunAll.m`, `RevisedCodes_16_00_Config.m` |
| 17 | Audit Pooling Prerequisites | `RevisedCodes_17D_RunAll.m`, `RevisedCodes_17_19_RunAll.m`, `RevisedCodes_17_Preflight_RunAll.m`, `RevisedCodes_17C_Config.m` |
| 18 | Assess Innings Selection | `RevisedCodes_18_00_Utils.m`, `RevisedCodes_18_00_LoadCache.m`, `RevisedCodes_18_00_SelfTests.m`, `RevisedCodes_18_00_ChaseReconstruction.m` |
| 19 | Confirm and Retain Final Models | `RevisedCodes_19_00_LockProtocol.m`, `RevisedCodes_19_RunAll.m`, `RevisedCodes_19_00_GenderStateAudit.m`, `RevisedCodes_19_00_Config.m` |
| 20 | Evaluate Historical Interruptions | `RevisedCodes_Pre20_RunAll.m`, `RUN_Step20.m`, `RevisedCodes_Pre20C_RunAll.m`, `RevisedCodes_20_Config.m` |
| 21 | Assess Historical Agreement | `RUN_Step21.m`, `RevisedCodes_21_Config.m`, `RevisedCodes_21_RunAll.m` |
| 22 | Evaluate Temporal Test | `RevisedCodes_22_RunAll.m`, `RevisedCodes_22_Config.m`, `RUN_Step22.m` |
| 23 | Assess Pooling and Metadata | `RevisedCodes_23_Config.m`, `RUN_Step23_ComputationalClosure.m`, `RevisedCodes_23_RunAll.m` |
| 24 | Prepare Repository Inventory | `RevisedCodes_24_Config.m`, `RevisedCodes_24_RunAll.m` |
| 25 | Extract Manuscript Evidence | `RevisedCodes_25_RunAll.m`, `RUN_Step25_ManuscriptEvidence.m`, `RevisedCodes_25_Config.m` |
| 26 | Prepare Publication Artifacts | `RevisedCodes_26_RunAll.m`, `RUN_Step26_PublicationArtifacts.m`, `RevisedCodes_26_Config.m` |
| 27 | Regenerate Archived Figures | `RevisedCodes_27_Regenerate_All_Manuscript_Figures_600dpi.m` |

Steps 1–8 prepare and describe source records. Steps 9–12 construct states, estimate empirical resource measures, verify constrained references and fit candidates. Step 13 examines resource approximation. Steps 14–18 calculate target scenarios and assess development predictions, sensitivities and innings scope. Step 19 confirms specifications in 2023 and refits retained models through 2023. Steps 20–21 reconstruct and summarize historical interruptions. Step 22 evaluates the fixed models on 2024–2025 matches. Step 23 assesses pooling and metadata. Steps 24–27 organize and regenerate archived publication evidence. Their earlier layouts do not replace the current submission figures and tables.

## Reproducibility boundary

The non-code deposit supplies saved models, fixed predictions, derived data and archived reports. It does not contain the complete raw delivery collection, all original Step 9 state partitions or every upstream model-development MAT object. A source checksum inventory identifies the analyzed records; it is not the source data itself. Recover or regenerate the required upstream inputs before attempting a fresh raw-data-to-model execution. A complete fresh fit, selection and bootstrap run was not verified during the submission review. Checking saved calculations must not be described as a new fit or independent interrupted-match validation.

The resource models and contextual forecasts have different roles. Resource models use balls remaining and wickets in hand and enter target allocation. Contextual forecasts predict remaining runs only. Opponent history means totals conceded while fielding, not the opponent's own batting totals. Numeric contextual main effects and their products with the remaining-ball fraction are both retained.

## Licensing and citation

Original MATLAB code is covered by the MIT License supplied in each step archive. Original documentation and author-created derived tables carry the supplied Creative Commons Attribution 4.0 notice. Cricsheet records, comparator tables and other third-party materials retain their original terms. Cite the manuscript, the code repository and the Zenodo version used in a replication.

## Independent check of the archived calculations

The accompanying verify_archived_results.py was added during the final submission review. It checks ten performance summaries from archived match errors, twelve paired gains, two worked targets, six historical pre-start targets, and 363 full-wicket values from earlier fits. It does not rerun fitting, selection, bootstrap intervals or independent-match validation. Python 3.10 or newer, NumPy and pandas are required. After merging the five Zenodo ZIP files into one extraction tree, run:

```sh
python verify_archived_results.py --data-root /path/to/S5_File_Reproducibility
```

The source_reports directory from Repository File 6 is needed for the match-level error check. The --report option can save an optional JSON report; it is not required. The final-review run passed all checks against the deposited analytical materials.
