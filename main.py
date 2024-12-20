from pathlib import Path
from datetime import datetime, timedelta
from git import Repo
from collections import defaultdict
import argparse
import logging
from prettytable import PrettyTable

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('git').setLevel(logging.WARNING)

def get_commits_by_week(base_path, num_weeks):
    """
    Traverse all Git repos in a folder and generate a report of commits
    by week and day for the specified number of weeks, including commits
    from the reflog.
    """
    now = datetime.now()
    start_of_current_week = now - timedelta(days=now.weekday()) # Get the start of the current week
    end_of_current_week = start_of_current_week + timedelta(days=6) # Get the end of the current week
    start_of_period = start_of_current_week - timedelta(weeks=num_weeks - 1) # Get the start of the analysis period
    logging.info(f'Search period: {start_of_period.date()} - {end_of_current_week.date()}')

    report = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    # Structure: week -> day -> project -> number of commits

    base_path = Path(base_path)
    for repo_path in base_path.rglob('.git'):
        repo_path = repo_path.parent
        repo = Repo(repo_path)

        for entry in repo.git.reflog().splitlines():
            commit_hash = entry.split()[0]
            commit = repo.commit(commit_hash)
            commit_date = datetime.fromtimestamp(commit.committed_date)

            if start_of_period <= commit_date <= end_of_current_week:
                week_start = commit_date - timedelta(days=commit_date.weekday())
                day = commit_date.strftime('%A')
                project_name = repo_path.name
                report[week_start.date()][day][project_name] += 1

                first_line_of_commit = str(commit.message).split('\n')[0]
                logging.debug(f"{f'[ {repo_path.name.upper()} ]':^20.20} - {first_line_of_commit:<20.20} ({commit.hexsha[:7]}) on {commit_date}")

    return report

def generate_report(report):
    """
    Generate a structured report from commit data.
    """
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    projects_colors = defaultdict(lambda: len(projects_colors) + 1)

    table = PrettyTable()
    table.field_names = ["Week"] + days_of_week

    for week, days in sorted(report.items()):
        row = [week]
        for day in days_of_week:
            cell = ""
            for project in days.get(day, {}):
                color = projects_colors[project]
                cell += f"\033[48;5;{color}m X \033[0m"
            row.append(cell.strip())
        table.add_row(row)

    print(table)

    # Print legend
    print("\nLegend:")
    for project, color in projects_colors.items():
        print(f"\t{project:<20.20} : \033[48;5;{color}m   \033[0m")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a report of Git commits by week.")
    parser.add_argument("base_path", type=str, help="Path to the directory containing Git repositories")
    parser.add_argument("--weeks", type=int, default=2, help="Number of weeks to include in the report")
    args = parser.parse_args()

    base_path = Path(args.base_path)
    num_weeks = args.weeks
    if not base_path.is_dir():
        print("The specified path does not exist or is not a valid directory.")
    else:
        report = get_commits_by_week(base_path, num_weeks)
        if report:
            generate_report(report)
        else:
            print("No commits found for the specified weeks.")
