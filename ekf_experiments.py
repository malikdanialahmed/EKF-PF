# FOR THE COMBINED PLOTTING OF RESULTS

# import subprocess
# import numpy as np
# import matplotlib.pyplot as plt

# r_values = [1/64, 1/16, 1/4, 4, 16, 64]
# n_trials = 10

# def run_trial(r, mode):
#     errors = []
#     mahalanobis_errors = []
#     anees = []

#     for seed in range(n_trials):
#         if mode == 'b':
#             args = [
#                 'python', 'localization.py', 'ekf',
#                 '--data-factor', str(r),
#                 '--filter-factor', str(r),
#                 '--seed', str(seed)
#             ]
#         elif mode == 'c':
#             args = [
#                 'python', 'localization.py', 'ekf',
#                 '--filter-factor', str(r),
#                 '--seed', str(seed)
#             ]
#         else:
#             raise ValueError("Mode must be 'b' or 'c'")

#         result = subprocess.run(
#             args,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )

#         for line in result.stdout.split('\n'):
#             if 'Mean position error' in line:
#                 errors.append(float(line.split(':')[1]))
#             elif 'Mean Mahalanobis error' in line:
#                 mahalanobis_errors.append(float(line.split(':')[1]))
#             elif 'ANEES' in line:
#                 anees.append(float(line.split(':')[1]))

#     return np.mean(errors), np.mean(mahalanobis_errors), np.mean(anees)



# def run_experiments(mode='b'):
#     mean_errors = []
#     mean_mahal_errors = []
#     mean_anees = []

#     for r in r_values:
#         print(f"Running for r = {r} (mode {mode})")
#         error, mahal_error, anees_val = run_trial(r, mode)
#         mean_errors.append(error)
#         mean_mahal_errors.append(mahal_error)
#         mean_anees.append(anees_val)

#     # Subplot layout: 3 rows, 1 column
#     fig, axes = plt.subplots(3, 1, figsize=(8, 12), sharex=True)
#     fig.suptitle(f'Part {mode.upper()} - EKF Performance vs Noise Factor', fontsize=16)

#     # Subplot 1: Position Error
#     axes[0].plot(r_values, mean_errors, marker='o', color='blue')
#     axes[0].set_ylabel('Mean Position Error')
#     axes[0].grid(True)

#     # Subplot 2: Mahalanobis Error
#     axes[1].plot(r_values, mean_mahal_errors, marker='^', color='green')
#     axes[1].set_ylabel('Mean Mahalanobis Error')
#     axes[1].grid(True)

#     # Subplot 3: ANEES
#     axes[2].plot(r_values, mean_anees, marker='x', color='red')
#     axes[2].set_xlabel('r (log scale)')
#     axes[2].set_ylabel('ANEES')
#     axes[2].grid(True)

#     # Log scale for x-axis on all subplots
#     for ax in axes:
#         ax.set_xscale('log')

#     plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to make room for suptitle
#     plt.savefig(f'ekf_part_{mode}_all_metrics.png')
#     plt.show()


# if __name__ == "__main__":
#     import argparse
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--mode', choices=['b', 'c'], required=True, help="Choose part 'b' or 'c'")
#     args = parser.parse_args()

#     run_experiments(mode=args.mode)



# FOR THE SEPARATE PLOTTING OF RESULTS

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

    # Plot 1: Mean Position Error
    plt.figure(figsize=(8, 4))
    plt.plot(r_values, mean_errors, marker='o', color='blue')
    plt.xscale('log')
    plt.xlabel('r (log scale)')
    plt.ylabel('Mean Position Error')
    plt.title(f'Part {mode.upper()} - Mean Position Error vs Noise Factor')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'ekf_part_{mode}_mean_position_error.png')
    plt.show()

    # Plot 2: Mean Mahalanobis Error
    plt.figure(figsize=(8, 4))
    plt.plot(r_values, mean_mahal_errors, marker='^', color='green')
    plt.xscale('log')
    plt.xlabel('r (log scale)')
    plt.ylabel('Mean Mahalanobis Error')
    plt.title(f'Part {mode.upper()} - Mean Mahalanobis Error vs Noise Factor')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'ekf_part_{mode}_mean_mahalanobis_error.png')
    plt.show()

    # Plot 3: ANEES
    plt.figure(figsize=(8, 4))
    plt.plot(r_values, mean_anees, marker='x', color='red')
    plt.xscale('log')
    plt.xlabel('r (log scale)')
    plt.ylabel('ANEES')
    plt.title(f'Part {mode.upper()} - ANEES vs Noise Factor')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'ekf_part_{mode}_anees.png')
    plt.show()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['b', 'c'], required=True, help="Choose part 'b' or 'c'")
    args = parser.parse_args()

    run_experiments(mode=args.mode)



#     # FOR PLOTTING THE PLOTS AT EACH VALUE OF r

# import subprocess
# import numpy as np
# import matplotlib.pyplot as plt

# r_values = [1/64, 1/16, 1/4, 4, 16, 64]
# n_trials = 10

# def run_trial_all_seeds(r, mode):
#         errors = []
#         mahalanobis_errors = []
#         anees = []

#         for seed in range(n_trials):
#             if mode == 'b':
#                 args = [
#                     'python', 'localization.py', 'ekf',
#                     '--data-factor', str(r),
#                     '--filter-factor', str(r),
#                     '--seed', str(seed)
#                 ]
#             elif mode == 'c':
#                 args = [
#                     'python', 'localization.py', 'ekf',
#                     '--filter-factor', str(r),
#                     '--seed', str(seed)
#                 ]
#             else:
#                 raise ValueError("Mode must be 'b' or 'c'")

#             result = subprocess.run(
#                 args,
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 text=True
#             )

#             for line in result.stdout.split('\n'):
#                 if 'Mean position error' in line:
#                     errors.append(float(line.split(':')[1]))
#                 elif 'Mean Mahalanobis error' in line:
#                     mahalanobis_errors.append(float(line.split(':')[1]))
#                 elif 'ANEES' in line:
#                     anees.append(float(line.split(':')[1]))

#         return errors, mahalanobis_errors, anees


# def run_individual_experiments(mode='b'):
#         all_errors = []
#         all_mahalanobis = []
#         all_anees = []

#         for r in r_values:
#             print(f"Running for r = {r} (mode {mode})")
#             errors, mahal, anees = run_trial_all_seeds(r, mode)
#             all_errors.append(errors)
#             all_mahalanobis.append(mahal)
#             all_anees.append(anees)

#         # Convert to numpy for easier plotting
#         all_errors = np.array(all_errors)
#         all_mahalanobis = np.array(all_mahalanobis)
#         all_anees = np.array(all_anees)

#         metrics = {
#             'Mean Position Error': all_errors,
#             'Mean Mahalanobis Error': all_mahalanobis,
#             'ANEES': all_anees
#         }

#         for title, data in metrics.items():
#             plt.figure(figsize=(10, 5))
#             for i, r in enumerate(r_values):
#                 x_vals = np.full(n_trials, r) + (np.random.randn(n_trials) * r * 0.05)  # jitter
#                 plt.scatter(x_vals, data[i], label=f"r={r:.4f}")
#             plt.xscale('log')
#             plt.xlabel("r (log scale)")
#             plt.ylabel(title)
#             plt.title(f'{title} - Part {mode.upper()}')
#             plt.grid(True)
#             plt.legend()
#             plt.tight_layout()
#             plt.savefig(f'ekf_part_{mode}_{title.replace(" ", "_").lower()}.png')
#             plt.show()


# if __name__ == "__main__":
#         import argparse
#         parser = argparse.ArgumentParser()
#         parser.add_argument('--mode', choices=['b', 'c'], required=True)
#         args = parser.parse_args()
#         run_individual_experiments(mode=args.mode)