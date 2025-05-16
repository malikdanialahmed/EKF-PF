# EKF & PF Localization Experiments

This repository contains Python implementations of the Extended Kalman Filter (EKF) and Particle Filter (PF) for mobile robot localization in a simulated soccer field environment. It also includes experiment scripts to evaluate filter performance across varying noise levels and particle counts.

---

## Repository Structure

```
├── Dockerfile
├── requirements.txt
├── results              # Genrated results
├── README.md            # (this file)
├── localization.py      # Main entry point for running single-run experiments
├── ekf.py               # Extended Kalman Filter implementation
├── pf.py                # Particle Filter implementation
├── utils.py             # Helper functions and plotting utilities
├── soccer_field.py      # Environment dynamics and observation models
├── policies.py          # Motion policies for the robot
├── ekf_experiments.py   # Batch script for EKF experiments (parts b & c)
├── pf_experiments.py    # Batch script for PF experiments (parts b, c & d)
└── assignment.pdf       # Assignment specification and theoretical exercises
```

---

## Prerequisites

-   **Python 3.7+**
-   **pip**
-   **Docker** (optional but recommended for reproducibility)

External Python dependencies are listed in `requirements.txt`:

```text
numpy
matplotlib
```

---

## Local (non-Docker) Setup

1. **Clone** the repository and navigate into it:

    ```bash
    git clone https://github.com/malikdanialahmed/EKF-PF.git
    cd EKF-PF
    ```

2. **Create** and **activate** a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate       # macOS / Linux
    venv\\Scripts\\activate      # Windows PowerShell
    ```

3. **Install** dependencies:

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. **Run** single localization experiments:

    ```bash
    # No filter, just ground-truth path:
    python localization.py none --plot

    # EKF filter:
    python localization.py ekf --plot

    # PF filter:
    python localization.py pf --plot

    # Show all available flags:
    python localization.py -h
    ```

---

## Experiment Scripts

### EKF Experiments

This script evaluates the performance of the Extended Kalman Filter (EKF) under varying noise conditions.

### EKF Experiments (parts b & c)

**Output:**

-   Runs `localization.py` multiple times with different random seeds
-   Computes:

    -   Mean position error
    -   Mahalanobis error
    -   ANEES

-   Generates:

    -   `ekf_part_b_all_metrics.png`
    -   Individual metric plots:

        -   `ekf_part_b_mean_position_error.png`
        -   `ekf_part_b_mean_mahalanobis_error.png`
        -   `ekf_part_b_anees.png`

Batch-run EKF experiments under two modes:

-   **Part B**: Vary both data-factor and filter-factor (`r`) over `[1/64, 1/16, 1/4, 4, 16, 64]`:

    ```bash
    python ekf_experiments.py --mode b
    ```

    **Output:**

    -   `ekf_part_b_mean_position_error.png`
    -   `ekf_part_b_mean_mahalanobis_error.png`
    -   `ekf_part_b_anees.png`

    if you want to check the result at specific noise level use this command:

    ```bash
    python localization.py ekf --data-factor r --filter-factor r
    ```

    here you can add the value of r which is the noise.

-   **Part C**: Vary only the filter noise (keeping data noise at default):

    ```bash
    python ekf_experiments.py --mode c
    ```

    **Output:**

    -   `ekf_part_c_mean_position_error.png`
    -   `ekf_part_c_mean_mahalanobis_error.png`
    -   `ekf_part_c_anees.png`

**Tip:** Ensure all dependencies are installed (`numpy`, `matplotlib`).

### PF Experiments (parts b, c & d)

Batch-run PF experiments under three modes:

-   **Part B**: Both data and filter noise scale with r:

    ```bash
    python pf_experiments.py --mode b
    ```

    **Output:**

    -   `pf_part_b_position_error.png`
    -   `pf_part_b_mahalanobis_error.png`
    -   `pf_part_b_anees.png`

-   **Part C**: Only filter noise is scaled, data is fixed:

    ```bash
    python pf_experiments.py --mode c
    ```

    **Output:**

    -   `pf_part_c_position_error.png`
    -   `pf_part_c_mahalanobis_error.png`
    -   `pf_part_c_anees.png`

-   **Part D**: Vary measurement/filter noise and number of particles (`[20, 50, 500]`):

    ```bash
    python pf_experiments.py --mode d
    ```

    **Output:**

    -   `pf_part_d_pos_error.png`
    -   `pf_part_d_anees.png`

---

## Docker Setup

A Docker image ensures a consistent environment across platforms.

1. **Build the image** (bash / PowerShell):

    ```bash
    docker build -t ekf_pf_suite:latest .
    ```

2. **Run** the container:

    - **Default (PF experiments)**:

        ```bash
        docker run --rm ekf_pf_suite:latest
        ```

    - **EKF experiments**:

        ```bash
        docker run --rm ekf_pf_suite:latest python ekf_experiments.py --mode b
        ```

        ```bash
        docker run --rm ekf_pf_suite:latest python ekf_experiments.py --mode c
        ```

    - **PF experiments**:

        ```bash
        docker run --rm ekf_pf_suite:latest python pf_experiments.py --mode d
        ```

        ```bash
        docker run --rm ekf_pf_suite:latest python pf_experiments.py --mode b
        ```

        ```bash
        docker run --rm ekf_pf_suite:latest python pf_experiments.py --mode c
        ```

        ```bash
        docker run --rm ekf_pf_suite:latest python pf_experiments.py --mode b
        ```

        ```bash
        docker run --rm ekf_pf_suite:latest python pf_experiments.py --mode c
        ```

    - **Mount a host directory** for results/logs:

        ```bash
        # macOS/Linux
        docker run --rm -v "$(pwd)/results:/app/results" ekf_pf_suite:latest

        # Windows PowerShell
        docker run --rm -v ${PWD}\\results:/app/results ekf_pf_suite:latest
        ```

    All generated plots will appear in the mounted `./results` folder on your host.

---

## Customization & Development

-   To debug inside the container, change the last line in `Dockerfile` to use an interactive shell:

    ```dockerfile
    ENTRYPOINT ["bash", "-lc"]
    ```

    then rebuild and run:

    ```bash
    docker run --rm -it ekf_pf_suite:latest
    ```

    You can now manually invoke any script (e.g., `python localization.py ekf --plot`).

-   To adjust filter parameters, edit the `alphas` and `beta` defaults in `localization.py`.
