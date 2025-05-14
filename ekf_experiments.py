import subprocess
import numpy as np
import matplotlib.pyplot as plt

r_values = [1/64, 1/16, 1/4, 4, 16, 64]
n_trials = 10

def run_trial(r, mode):
    errors = []
    mahalanobis_errors = []
    anees = []

    for seed in range(n_trials):
        if mode == 'b':
            args = [
                'python', 'localization.py', 'ekf',
                '--data-factor', str(r),
                '--filter-factor', str(r),
                '--seed', str(seed)
            ]
        elif mode == 'c':
            args = [
                'python', 'localization.py', 'ekf',
                '--filter-factor', str(r),
                '--seed', str(seed)
            ]
        else:
            raise ValueError("Mode must be 'b' or 'c'")

        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in result.stdout.split('\n'):
            if 'Mean position error' in line:
                errors.append(float(line.split(':')[1]))
            elif 'Mean Mahalanobis error' in line:
                mahalanobis_errors.append(float(line.split(':')[1]))
            elif 'ANEES' in line:
                anees.append(float(line.split(':')[1]))

    return np.mean(errors), np.mean(mahalanobis_errors), np.mean(anees)



def run_experiments(mode='b'):
    mean_errors = []
    mean_mahal_errors = []
    mean_anees = []

    for r in r_values:
        print(f"Running for r = {r} (mode {mode})")
        error, mahal_error, anees_val = run_trial(r, mode)
        mean_errors.append(error)
        mean_mahal_errors.append(mahal_error)
        mean_anees.append(anees_val)

    # Subplot layout: 3 rows, 1 column
    fig, axes = plt.subplots(3, 1, figsize=(8, 12), sharex=True)
    fig.suptitle(f'Part {mode.upper()} - EKF Performance vs Noise Factor', fontsize=16)

    # Subplot 1: Position Error
    axes[0].plot(r_values, mean_errors, marker='o', color='blue')
    axes[0].set_ylabel('Mean Position Error')
    axes[0].grid(True)

    # Subplot 2: Mahalanobis Error
    axes[1].plot(r_values, mean_mahal_errors, marker='^', color='green')
    axes[1].set_ylabel('Mean Mahalanobis Error')
    axes[1].grid(True)

    # Subplot 3: ANEES
    axes[2].plot(r_values, mean_anees, marker='x', color='red')
    axes[2].set_xlabel('r (log scale)')
    axes[2].set_ylabel('ANEES')
    axes[2].grid(True)

    # Log scale for x-axis on all subplots
    for ax in axes:
        ax.set_xscale('log')

    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to make room for suptitle
    plt.savefig(f'ekf_part_{mode}_all_metrics.png')
    plt.show()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['b', 'c'], required=True, help="Choose part 'b' or 'c'")
    args = parser.parse_args()

    run_experiments(mode=args.mode)
