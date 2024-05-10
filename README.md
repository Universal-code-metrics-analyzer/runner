# UCMA | Runner

The main executable of the Universal Code Metrics Analyzer. Requires [Poetry](https://python-poetry.org/) to run.

**Install**

``` bash
# install
git clone https://github.com/Universal-code-metrics-analyzer/runner
cd runner
poetry install

# install plugins
poetry add git+https://github.com/Universal-code-metrics-analyzer/fs-git-processor@v0.1.0
poetry add git+https://github.com/Universal-code-metrics-analyzer/mock-metrics-calculator@v0.1.0
poetry add git+https://github.com/Universal-code-metrics-analyzer/json-report-generator@v0.1.0

# run
poetry shell
python main.py
```

**Configuration**

``` yaml
# config.yml

git_processor:
  # name of the Git processor plugin
  plugin: fs_git_processor
  # plugin-specific configuration
  config:
    repo: /Users/example/Documents/my-project

metrics_calculator:
  # name of the Metrics calculator plugin
  plugin: mock_metrics_calculator
  # no plugin-specific configuration required

report_generator:
  # name of the Report generator plugin
  plugin: json_report_generator
  config:
    output_dir: reports
```

**Usage**

``` bash
python main.py --help
                                                                                         
Usage: main.py [OPTIONS] COMMIT_REFS...                                                 
                                                                                         
╭─ Arguments ───────────────────────────────────────────────────────────────────────────╮
│ *    commit_refs      COMMIT_REFS...  List of one of: HEAD, tag, branch name, remote  │
│                                       branch name, hash, short hash                   │
│                                       [default: None]                                 │
│                                       [required]                                      │
╰───────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────╮
│ --dry-run               --no-dry-run      Validate plugin configuration               │
│                                           [default: no-dry-run]                       │
│ --install-completion                      Install completion for the current shell.   │
│ --show-completion                         Show completion for the current shell, to   │
│                                           copy it or customize the installation.      │
│ --help                                    Show this message and exit.                 │
╰───────────────────────────────────────────────────────────────────────────────────────╯
```