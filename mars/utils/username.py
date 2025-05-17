import subprocess


def get_linux_username() -> str:
    result = subprocess.run(['whoami'], capture_output=True, text=True)
    username = result.stdout.strip()
    return username
