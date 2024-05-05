set dotenv-load

dev *ARGS:
    PYTHONPATH=:./app python app/main.py {{ARGS}}