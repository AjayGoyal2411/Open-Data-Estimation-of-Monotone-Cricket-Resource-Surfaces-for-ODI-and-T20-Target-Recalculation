# SPDX-License-Identifier: MIT
"""Independently check archived cricket-model calculations, without model fitting.

Requires Python 3.10+, numpy and pandas.
Run: python verify_archived_results.py --data-root /path/to/S5_File_Reproducibility
Extract the Zenodo data ZIP files into a common parent directory first.
This utility was added during the final submission review. It is not the
original MATLAB estimation pipeline and does not rerun selection or bootstrap.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


def require_close(actual, expected, label, tolerance=1e-9):
    maximum = float(np.max(np.abs(np.asarray(actual) - np.asarray(expected))))
    if not np.isfinite(maximum) or maximum > tolerance:
        raise AssertionError(f"{label}: maximum difference {maximum:g}")
    return maximum


def resource(parameters, balls, wickets, allocation):
    """Evaluate the published compact function at the supplied cricket states."""
    a, b, c, d, e, f = parameters
    wicket_fraction = np.asarray(wickets, dtype=float) / 10
    ball_fraction = np.asarray(balls, dtype=float) / allocation
    logistic = lambda value: 1 / (1 + np.exp(-value))
    capacity = (logistic(a + b*wicket_fraction + c*wicket_fraction**2) - logistic(a))
    capacity /= logistic(a+b+c) - logistic(a)
    decay = np.exp(d + e*wicket_fraction + f*wicket_fraction**2)
    return capacity * (-np.expm1(-decay*ball_fraction)) / (-np.expm1(-decay))


def winning_target(par):
    return math.floor(par + 1e-10*max(1, abs(par))) + 1


def verify(data_root):
    derived = data_root / "derived_revision"
    parameters = pd.read_csv(derived / "CompactParameters.csv").set_index("Format")
    performance = pd.read_csv(derived / "FrozenPerformance.csv")
    error_files = sorted((data_root / "source_reports").rglob("Step22_MatchErrors.csv"))
    if len(error_files) != 1:
        raise ValueError(f"Expected one archived Step22_MatchErrors.csv; found {len(error_files)}")
    match_errors = pd.read_csv(error_files[0])
    checks = []
    for (format_name, role), group in match_errors.groupby(["Format", "Role"], sort=False):
        saved = performance[(performance.Format == format_name) & (performance.Role == role)]
        if len(saved) != 1:
            raise AssertionError(f"Ambiguous saved performance: {format_name}, {role}")
        saved = saved.iloc[0]
        observed = [math.sqrt(group.MSE.mean()), group.MAE.mean(), group.Bias.mean()]
        expected = [saved.EqualInningsRMSE, saved.EqualInningsMAE, saved.EqualInningsBias]
        difference = require_close(observed, expected, f"{format_name} {role} errors")
        assert len(group) == saved.Matches and group.States.sum() == saved.States
        checks.append({"format": format_name, "role": role, "matches": len(group),
                       "states": int(group.States.sum()), "maximum_difference": difference})

    pairs = pd.read_csv(derived / "PairedComparisons.csv")
    for _, comparison in pairs.iterrows():
        # Saved comparison columns use research roles rather than displayed table labels.
        candidate = performance[(performance.Format == comparison.Format) &
                                (performance.Role == comparison.Role)].iloc[0]
        comparator = performance[(performance.Format == comparison.Format) &
                                 (performance.Role == comparison.Comparator)].iloc[0]
        require_close(comparator.EqualInningsRMSE-candidate.EqualInningsRMSE,
                      comparison.RMSEGain, "paired RMSE gain")

    worked = pd.read_csv(derived / "WorkedCases.csv")
    for _, case in worked.iterrows():
        fitted = parameters.loc[case.Format]
        coefficients = fitted[["a", "b", "c", "d", "e", "f"]].to_numpy(float)
        allocation = 300 if case.Format == "ODI" else 120
        wickets = 10-case.WicketsLost
        before = float(resource(coefficients, case.BeforeRemainingBalls, wickets, allocation))
        after = float(resource(coefficients, case.AfterRemainingBalls, wickets, allocation))
        chasing_allocation = 1-before+after
        par = case.FirstInningsRuns*chasing_allocation
        require_close([before, after, chasing_allocation, par],
                      [case.BeforeEventResource, case.AfterEventResource, case.FinalResource,
                       case.UnroundedPar], f"worked match {case.MatchID}")
        assert winning_target(par) == case.ModelTargetRuns

    benchmarks = pd.read_csv(derived / "HistoricalBenchmarks.csv")
    for _, case in benchmarks.iterrows():
        fitted = parameters.loc[case["Format"]]
        coefficients = fitted[["a", "b", "c", "d", "e", "f"]].to_numpy(float)
        allocation = 300 if case["Format"] == "ODI" else 120
        chasing_resource = float(resource(coefficients, case["Chase overs"]*6, 10, allocation))
        par = case["First innings runs"]*chasing_resource
        require_close(par, case["Proposed continuous par"], "historical pre-start par")
        assert winning_target(par) == case["Proposed winning target"]

    folder = data_root / "full_wicket_development"
    coefficients = pd.read_csv(folder / "12_01_Coefficients.csv")
    grid = pd.read_csv(folder / "Pre20E_FullWicketApproximation.csv")
    model = "Compact::compact__mean_state_n30_precision_l0"
    selected = grid[grid.Model == model]
    if len(selected) != 363:
        raise AssertionError(f"Expected 363 earlier-fit full-wicket states; found {len(selected)}")
    largest_difference = 0.0
    for year, group in selected.groupby("Year", sort=True):
        available = coefficients[(coefficients.PackageID == f"Fold_{year}_T20") &
                                 (coefficients.ReferenceCandidate == "mean_state_n30_precision_l0")]
        fitted = available.set_index("Coefficient").loc[["a", "b", "c", "d", "e", "f"], "Estimate"]
        reconstructed = resource(fitted.to_numpy(float), group.BallsRemaining.to_numpy(), 10, 120)
        difference = require_close(reconstructed, group.FittedCapacity.to_numpy(),
                                   f"full-wicket development fit {year}", 1e-12)
        largest_difference = max(largest_difference, difference)

    return {"scope": "Saved calculations only; no fitting, model selection or bootstrap rerun",
            "performance_checks": checks, "paired_gains_checked": len(pairs),
            "worked_targets_checked": len(worked), "pre_start_targets_checked": len(benchmarks),
            "earlier_fit_grid_values_checked": len(selected),
            "maximum_earlier_fit_reconstruction_difference": largest_difference,
            "status": "All checks passed"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", required=True, type=Path)
    parser.add_argument("--report", type=Path, help="Optional JSON report destination")
    args = parser.parse_args()
    result = verify(args.data_root)
    output = json.dumps(result, indent=2)
    print(output)
    if args.report:
        args.report.write_text(output + "\n", encoding="utf-8")
