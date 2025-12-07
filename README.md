# Using the ZwiftRacing API with Python

## Prerequisites

- Linux development environment (window users, see WSL2)
- Python
- ``uv`` package manager
- ``direnv`` environment variable manager %mdash; add the ``.envrc`` file in the project root
    ```
    # Handle windows carriage-returns
    sed -i 's/\r$//' .env

    # Export .env variables
    set -a
    source .env
    set +a
    ```
- ZwiftRacing.app API key &mdash; add to a ``.env`` file
    ```
    ZRAPP_API_KEY="YOUR_KEY"
    ```
    If using git, add ``.env`` to ``.gitignore``



