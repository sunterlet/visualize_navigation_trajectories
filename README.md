# Trajectory Visualization for Virtual‑Arena Experiments

## Overview
`visualize_trajectories.py` turns raw log files from desktop spatial‑memory experiments into trajectory plots. For every trial the script draws the participant’s path inside the circular arena, colours it by elapsed time, and marks key locations and events such as real and annotated target location, movement onset, and exploration time. The resulting PNG images help us spot systematic navigation patterns, lapses, or biases at a glance.

Data of 4 example participants are avalible in /results_prolific. 
1 example png file is avalible in /trajectory_plots
---

## Input data
The script expects the following folder structure:

```
results_prolific/
└── <SUBFOLDER>/                # e.g. "2025-05-07_19/03/20.476610_vw1ezaxd"
    └── data/
        ├── continuous_log_<…>.csv   # time‑sampled xy positions & events
        └── discrete_log_<…>.csv     # per‑trial summary metrics
```

### Required columns

| File | Columns used by the script |
|------|----------------------------|
| *continuous_log*.csv | `participant_id`, `trial_info`, `phase`, `event`, `trial_time`, `x`, `y` |
| *discrete_log*.csv   | `participant_id`, `trial`, `assigned_delay`, `exploration_time` |

---

## Output
One PNG file per trial is saved in `trajectory_plots/` (or a directory you choose via `--output-dir`). Filenames follow `trajectory_<USER_ID>_<TRIAL_NAME>.png`.

---

## Installation

```bash
# 1. Clone the repo that contains this README
git clone https://github.com/sunterlet/visualize_navigation_trajectories
cd visualize_navigation_trajectories

# 2. (Optional) Create & activate a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt  # pandas, numpy, matplotlib
```

---

## Usage

```bash
# ID comes from the folder name segment before “_vw1ezaxd”
python visualize_trajectories.py \
       --subfolder "286584" \
       --output-dir "path/to/figs"
```

| Argument        | Required | Description |
|-----------------|----------|-------------|
| `--subfolder`   | **Yes**  | User ID inside `results_prolific/` |
| `--output-dir`  | No       | Destination for PNGs (default: `trajectory_plots`) |

After execution you should see:

```
trajectory_plots/
├── trajectory_286584_training 1.png
├── trajectory_286584_training 2.png
└── …
```

---

## Course Information
This repository serves as my final project for the **Basic programming skills (Python)** course (Spring 2025, Weizmann Institute of Science). Course materials: <https://github.com/Code-Maven/wis-python-course-2025-03>
