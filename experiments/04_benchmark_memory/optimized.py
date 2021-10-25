import glob
import os

from cockpit.quantities import GradHist1d
from shared import DIR, parse, report_memory, run, set_up, skip_if_exists


def get_out_files(testproblem):
    """Return all available output files for a test problem."""
    pattern = os.path.join(DIR, f"{testproblem}_optimized_*.csv")
    return glob.glob(pattern)


def out_file(testproblem, num_run):
    """Return save path for a specific run of a test problem"""
    return os.path.join(DIR, f"{testproblem}_optimized_{num_run:03d}.csv")


if __name__ == "__main__":
    set_up()

    testproblem, num_run = parse()
    filename = out_file(testproblem, num_run)

    skip_if_exists(filename)

    def benchmark_fn():
        def track_schedule(global_step):
            return True

        quants = [GradHist1d(track_schedule)]
        run(quants, testproblem)

    data = report_memory(benchmark_fn)
    data.to_csv(filename)
