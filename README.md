# Dev Activity Report

**Dev Activity Report** is a tool to generate a report of commits by week and day for Git repositories.

## Description

This tool traverses all Git repositories in a specified folder and generates a report of commits by week and day for a specified number of weeks. It includes commits from the reflog, making it useful for recovering lost commits and understanding the history of changes in a repository.

## Prerequisites
- [uv from astral](https://docs.astral.sh/uv/getting-started/installation/)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/dev-activity-report.git
    cd dev-activity-report
    ```

## Usage

Run the script with the following command:

**Windows:**
```pwsh
uv run .\main.py $HOME/[FOLDER] --weeks 2
```

**Linux:**
```sh
uv run main.py ~/[FOLDER] --weeks 2
```
- `--weeks`: The number of weeks to include in the report.
  
**Output:**

![image](https://github.com/user-attachments/assets/f83b0d58-3633-4f15-a751-3217b6749d4a)

## Authors

- **VBA-N7** - *Initial work* - [VBA](https://github.com/VBA-N7)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
