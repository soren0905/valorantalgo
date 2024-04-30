import subprocess
import sys


def run_script(script_path):
    """Run a script located at 'script_path' using the Python interpreter."""
    print(f"Running script: {script_path} using {sys.executable}")
    try:
        result = subprocess.run([sys.executable, script_path], check=True, text=True, capture_output=True)
        print(f"Script {script_path} ran successfully.\nOutput:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running script {script_path}: {e}")
        print(f"Output:\n{e.stdout}")
        print(f"Errors:\n{e.stderr}")


def main():
    scripts_to_run = [
        'C:/Users/soren/Projects/ValAlgo/scripts/functions/delete.py',
        'C:/Users/soren/Projects/ValAlgo/scripts/functions/upcoming_matches.py',
        'C:/Users/soren/Projects/ValAlgo/scripts/functions/upcoming_players.py',
        'C:/Users/soren/Projects/ValAlgo/scripts/functions/all_map_stats.py',
        'C:/Users/soren/Projects/ValAlgo/scripts/data collection/data_merge/combine_map_stats.py',
        'C:/Users/soren/Projects/ValAlgo/scripts/functions/upcoming_stats.py',
        'C:/Users/soren/Projects/ValAlgo/scripts/functions/Matches_2.py'
    ]

    for script in scripts_to_run:
        run_script(script)


if __name__ == "__main__":
    main()
