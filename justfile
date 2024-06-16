set dotenv-load

run *ARGS:
    PYTHONPATH=:./runner python runner/__main__.py {{ARGS}}