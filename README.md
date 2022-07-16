# ToDoListApp
Simple app for managing a to-do list using the FastAPI and SQLModel frameworks

# Getting Started

1. Clone the repository to your environment: `git clone https://github.com/paparon96/ToDoListApp.git`
2. Create a virtual environment for the project: `python -m venv to_do_list_app_venv`
3. Install the required packages (with the tested versions): `pip install -r ./requirements.txt`
4. Run the API in your environment: `uvicorn app.main:app`

# API structure

# Usage examples

Below you can find particular code snippets for the various use cases that this API supports.

## Get all the to-do list items
```
import requests

response = requests.get('http://127.0.0.1:8000/items/')
print(response)
print(response.json())
```

## Get the urgent to-do list items which will be due soon

# Testing
You can run the tests from the root of the repository via `pytest tests`. The current code coverage of the tests is low, this would need to be enhanced in the future.
