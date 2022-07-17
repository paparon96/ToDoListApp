# To-do list administration app
Simple app for managing a to-do list using the FastAPI and SQLModel frameworks.

# Getting Started

1. Clone the repository to your environment: `git clone https://github.com/paparon96/ToDoListApp.git`
2. Create a virtual environment for the project: `python -m venv to_do_list_app_venv` (Python 3.6+ version is required for FastAPI)
3. Activate virtual environment: `source ./to_do_list_app_venv/bin/activate`
4. Install the required packages (with the tested versions): `pip install -r ./requirements.txt`
5. Run the API in your environment: `uvicorn app.main:app`

# Data models
The to-do list items have the following attributes:
* `id`: `int`, ID of the item (set automatically, not customizable by the user)
* `description`: `str`, Short description of the item
* `priority`: `int`, Item priority (higher value for more important task)
* `owner`: `str`, The person assigned to work on the item
* `deadline`: `date`, Deadline date for the item
* `progress`: `str`, Current progress on the item
* `team_id`: `int`, ID of the team to which the item is assigned
* `team`: `Team`, Attributes of the team to which the item is assigned (only shown when info for a specific item is queried due to display/transparency reasons)

There is also `Team` data model, since teams are linked to the items through the `team_id` attribute. The teams have the following attributes:
* `id`: `int`, ID of the team (set automatically, not customizable by the user)
* `name`: `str`, Name of the team
* `headquarters`: `str`, Location of the team headquarters
* `items`: `List[ToDoListItem]`, Items which are assigned to the team (only shown when info for a specific team is queried due to display/transparency reasons)


# Usage examples

Below you can find particular code snippets for the various use cases that this API supports (the same could be achieved/tested through the OpenAPI docs page as well).

## Get all the to-do list items
```
import requests

response = requests.get('http://127.0.0.1:8000/items/')
print(response)
print(response.json())
```

## Get a particular to-do item
```
import requests

item_id = 1
response = requests.get(f'http://127.0.0.1:8000/items/{item_id}')
print(response)
print(response.json())
```

## Add a new to-do item
```
import requests

new_todo_item = {
            "description": "Test task",
            "priority": 2,
            "owner": "Test user",
            "deadline": "2022-07-20",
            "progress": "Backlog",
            "team_id": 1
            }
response = requests.post('http://127.0.0.1:8000/items/',
                           json = new_todo_item)

print(response.text)
```

## Get the urgent to-do list items which will be due soon
```
import requests

date = '2022-07-19'
response = requests.get(f'http://127.0.0.1:8000/items/urgent/?date={date}')
print(response)
print(response.json())
```

## Update a to-do item
```
import requests

item_id = 1
url = f'http://127.0.0.1:8000/items/{item_id}'
payload = {'description' : 'Updated description'}

response = requests.patch(url, json=payload)
print(response)
print(response.json())
```

## Delete a to-do item
```
import requests

item_id = 2
response = requests.delete(f'http://127.0.0.1:8000/items/{item_id}')
print(response)
```

# Testing
You can run the tests from the root of the repository via `pytest tests`. The current code coverage of the tests is low, this would need to be enhanced in the future.
