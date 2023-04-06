# Recommendation Service
This project is a microservice for course recommendations. It 
basically has two functionalities:
1. Start a webservice with 2 endpoints:
   1. `/courses-by-user/{user_id}` - retrieve courses in which a user
      has participated
   2. `/course-recommendation/{user_id}` - retrieve course 
      recommendations for a specific user
2. Load initial data into a neo4j database (this is optional and will
   be executed on server start)


## Recommendations Explained
This recommendation engine is built using a graph database and 
utilizes graph data to generate recommendations. Specifically, it uses
a Neo4j graph database to store information about users, courses, 
topics, and use cases. When a user requests recommendations, the 
algorithm looks at the courses the user has already participated in 
and identifies the use cases associated with those courses. It then 
searches for other courses that share as many use cases as possible 
with the user's past courses. The algorithm returns a list of the top 
10 courses with the most overlap in use cases.


## Usage
1. Start the application `poetry run uvicorn app.main:app --reload`
   1. you can access the docs: https://localhost:8000/docs
2. Start the neo4j database `docker-compose up neo4j`
   1. you can access neo4j GUI http://localhost:7474/

Have fun.


## Setup

**Dev Requirements**
- [python 3.9](https://www.python.org/) or higher
- [Poetry](https://python-poetry.org/) for dependency management
- [docker](https://www.docker.com/) & [docker-compose](https://docs.docker.com/compose/) is highly recommended
- a running [neo4j](https://neo4j.com/) instance (e.g. by using a [neo4j docker image](https://hub.docker.com/_/neo4j))

**Setup without docker**
- create a .env file `cp ./app/.env.example ./app/.env`
- fill your `.env` file with valid data
- This step is optional: if you have no neo4j instance running, you can start it with docker: `docker-compose up neo4j`
  in this setup you can use the default `.env` connection arguments
- copy data into project directory `cp -r ./data/ ./app/initial-csv-data`


## Cheat Sheet

### Poetry
- initialize a new project with poetry in a new directory `poetry init`
- add new project dependency `poetry add {{PACKAGE_NAME}}`
- add new deelopment dependency `poetry add -D {{PACKAGE_NAME}}`
- remove packege `poetry remove {{PACKAGE_NAME}}`
- run a command in your poetry virtualenv `poetry run {{COMMAND}}`
- access the poetry virtualenv `poetry shell`
- get local poetry env path `poetry env info --path`

Poetry will create two files in your project base directory:
- `poetry.lock` - a project manifest including detailed dependency information
- `pyproject.toml` - a project configuration file including dependencies, build information, meta information, etc.

More information:
- [Poetry Commands](https://python-poetry.org/docs/cli/)
- [Poetry Docs](https://python-poetry.org/docs/)

### Pre-Commit
- Install pre-commit for your current project `pre-commit install` - this will create a cache directory
- Clean Cache `pre-commit clean`
- Run pre-commit without committing `pre-commit run` **note** pre-commit file has to be staged or committed
- If you do not want to validate your commit: `git commit -m "Your cool message" --no-validate`

Make sure that a file named `.pre-commit-config.yaml` is placed in your project base directory, and it's well 
configured.

### Black
- exec format on specific file `black {{FILE_PATH}}` 
- dry run for file formatting `black --check {{FILE_PATH}}` 
- make usage of `# fmt: off` if you do not want to format a row by using black

More Information:
- [Black Docs](https://black.readthedocs.io/en/stable/)
- [Black Configuration Options](https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html#command-line-options)


### Flake8
- check if file is well formatted `flake8 {{FILE_PATH}}`
- Make usage of `# noqa` if a formatting issue is intendet (e.g. it 
  does not make sense to split one row into many)

More information:
- [Flake8 Docs](https://flake8.pycqa.org/en/latest/)

### Mypy
- check types in specific file `mypy {{FILE_PATH}}`

More information:
- [Mypy Docs](https://mypy-lang.org/)


### Fast API
- Start the server `uvicorn app.main:app --reload`


### Environment Setup with PyCharm
- Select the correct Python Interpreter:
  - Open Preferences
  - Choose Python Interpreter
  - Click to add new Python Interpreter
    - Choose poetry environment
    - Select existing Environment
    - Use the path you'll get with `poetry env info --path` and add 
      bin/python to your path
    - Click Apply
- Configure your debugger to run fastapi files

### Environment Setup with VSCode
- Install a plugin for `.editorconfig` files - [EditorConfig for VS Code](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig)
- create a file `.vscode/settings.json` and paste:
```json
{
  "python.defaultInterpreterPath": "{{Result of poetry env info --path}}/bin/python",
  "python.analysis.extraPaths": [
    "${workspaceFolder}/app"
  ]
}
```
- create a file `.vscode/launch.json` and paste:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Runserver",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "app.main:app",
        "--reload"
      ],
      "console": "integratedTerminal",
    },
  ]
}
```
- If you like to run any other Python file, you could also use the 
  following `launch.json` file:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run Foo",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/app/foo.py",
      "console": "integratedTerminal",
    },
  ]
}
```
