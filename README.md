# llama-ui

## Overview

`llama-ui` is a web application designed to provide an intuitive user interface for interacting with the Llama system. This guide will walk you through setting up the environment, installing necessary dependencies, and running the application.

## Prerequisites

- Python 3.x installed on your system.
- `pip` package manager.

## Setup Instructions

### 1. Create a Virtual Environment

First, create a virtual environment to manage dependencies for this project. This helps in maintaining a clean environment and avoiding conflicts with other projects.

```bash
python -m venv .venv
```

### 2. Activate the Virtual Environment

Activate the virtual environment to use the Python interpreter and package manager.

- On Windows:

```bash
.venv\Scripts\activate
```

- On macOS and Linux:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

With the virtual environment activated, install the required packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Run the Application

To start the application, run the following command:

```bash
reflex run
```

This will start the application. It can be accessed at [http://localhost:3000](http://localhost:3000). This will take you to the llama-ui web interface where you can interact with any ollama models. The download feature is currently in development.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
