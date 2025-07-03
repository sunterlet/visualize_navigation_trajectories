import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import os
import argparse
import glob
import re

# Constants from the experiment
ARENA_RADIUS = 1.65  # meters
SCALE = 200  # pixels per meter

def create_custom_colormap():
    """Create a custom colormap from dark blue to red."""
    colors = [(0, 0, 0.5), (1, 0, 0)]  # Dark blue to red
    return LinearSegmentedColormap.from_list('custom_cmap', colors, N=256)

def plot_trajectory(trial_data, trial_name, output_dir, discrete_data, participant_id):
    """Plot a single trial's trajectory with time-based color coding."""
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Draw arena boundary
    circle = plt.Circle((0, 0), ARENA_RADIUS, fill=False, color='black', linestyle='--')
    ax.add_artist(circle)
    
    # Get exploration data
    exploration_data = trial_data[trial_data['phase'] == 'exploration']
    annotation_data = trial_data[trial_data['phase'] == 'annotation']
    
    # Calculate time to movement start
    movement_start = exploration_data[exploration_data['event'] == 'started moving']
    time_to_movement = movement_start['trial_time'].iloc[0] if not movement_start.empty else 0
    
    # Get discrete data for this trial
    trial_discrete = discrete_data[discrete_data['trial'] == trial_name].iloc[0]
    assigned_delay = trial_discrete['assigned_delay']
    exploration_time = trial_discrete['exploration_time']
    
    # Plot exploration trajectory
    if not exploration_data.empty:
        x = exploration_data['x'].values
        y = exploration_data['y'].values
        times = exploration_data['trial_time'].values
        
        # Create color segments
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        
        # Create colormap
        cmap = create_custom_colormap()
        
        # Plot trajectory with color gradient
        norm = plt.Normalize(times.min(), times.max())
        lc = plt.matplotlib.collections.LineCollection(segments, cmap=cmap, norm=norm)
        lc.set_array(times)
        line = ax.add_collection(lc)
        
        # Add colorbar
        cbar = plt.colorbar(line, ax=ax)
        cbar.set_label('Time (seconds)')
    
    # Plot annotation trajectory
    if not annotation_data.empty:
        annot_x = annotation_data['x'].values
        annot_y = annotation_data['y'].values
        ax.plot(annot_x, annot_y, 'm--', alpha=0.5, label='Annotation Path')
    
    # Plot target location if available
    target_events = exploration_data[exploration_data['event'] == 'target_placed']
    if not target_events.empty:
        target_x = target_events['x'].iloc[0]
        target_y = target_events['y'].iloc[0]
        ax.plot(target_x, target_y, 'go', markersize=10, label='Target')
    
    # Plot annotation location if available
    annotation_events = annotation_data[annotation_data['event'] == 'target_annotated']
    if not annotation_events.empty:
        annot_x = annotation_events['x'].iloc[0]
        annot_y = annotation_events['y'].iloc[0]
        ax.plot(annot_x, annot_y, 'mo', markersize=10, label='Annotation')
    
    # Set plot properties
    ax.set_xlim(-ARENA_RADIUS*1.1, ARENA_RADIUS*1.1)
    ax.set_ylim(-ARENA_RADIUS*1.1, ARENA_RADIUS*1.1)
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_title(f'Participant: {participant_id}\nTrial: {trial_name}\nTime to movement start: {time_to_movement:.2f}s\nAssigned delay: {assigned_delay}s\nExploration time: {exploration_time:.2f}s')
    ax.set_xlabel('X position (meters)')
    ax.set_ylabel('Y position (meters)')
    
    # Add legend
    ax.legend()
    
    # Save the plot with participant ID in filename
    plt.savefig(os.path.join(output_dir, f'trajectory_{participant_id}_{trial_name}.png'), dpi=300, bbox_inches='tight')
    plt.close()

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate trajectory plots for specified participant IDs')
    parser.add_argument('--subfolder', nargs='+', required=True,
                      help='List of 6-digit participant IDs (e.g., 476610 017414 863489)')
    parser.add_argument('--output-dir', default='trajectory_plots',
                      help='Output directory for the plots')
    args = parser.parse_args()

    base_dir = '/Users/sunt/PhD/packngo/results_prolific'

    for participant_id in args.subfolder:
        # Search for the subfolder ending with _{ID}_vw1ezaxd
        found_subfolder = None
        for root, dirs, files in os.walk(base_dir):
            for d in dirs:
                if d.endswith(f'{participant_id}_vw1ezaxd'):
                    found_subfolder = os.path.relpath(os.path.join(root, d), base_dir)
                    break
            if found_subfolder:
                break
        if not found_subfolder:
            print(f"Error: No subfolder found for participant ID {participant_id}")
            continue
        input_dir = os.path.join(base_dir, found_subfolder, 'data')
        if not os.path.exists(input_dir):
            print(f"Error: Input directory not found: {input_dir}")
            continue

        # Create output directory if it doesn't exist
        os.makedirs(args.output_dir, exist_ok=True)
        
        # Find and read the continuous log file
        continuous_logs = glob.glob(os.path.join(input_dir, 'continuous_log*.csv'))
        if not continuous_logs:
            print(f"Error: No continuous log files found in {input_dir}")
            continue
        log_file = continuous_logs[0]  # Take the first matching file
        df = pd.read_csv(log_file)
        
        # Find and read the discrete log file
        discrete_logs = glob.glob(os.path.join(input_dir, 'discrete_log*.csv'))
        if not discrete_logs:
            print(f"Error: No discrete log files found in {input_dir}")
            continue
        discrete_file = discrete_logs[0]  # Take the first matching file
        discrete_data = pd.read_csv(discrete_file)
        
        # Use the participant_id directly
        
        # Group data by trial
        for trial_name, trial_data in df.groupby('trial_info'):
            plot_trajectory(trial_data, trial_name, args.output_dir, discrete_data, participant_id)
            print(f"Created plot for {trial_name} in {found_subfolder}")

if __name__ == "__main__":
    main() 
