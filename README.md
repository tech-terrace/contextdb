# ContextDB Project

## Overview
ContextDB is a Django-based web application designed to manage and serve documentation for various software frameworks. It utilizes Google Cloud Storage for file management and provides an API built with FastAPI for accessing the data. The project also includes scripts for automatically generating documentation files using Playwright.

## Features
- Management of frameworks, versions, and documentation variants through a Django admin interface.
- Automated documentation generation for frameworks like React, Vue.js, FastAPI, and React-DOM.
- An API for querying framework details, versions, and documentation.
- Integration with Google Cloud Storage for storing documentation files.

## Installation
1. Ensure Python 3.12 and Poetry are installed on your system.
2. Clone the repository and navigate into the project directory.
3. Install dependencies using Poetry:
   ```
   poetry install
   ```
4. Set up the Django environment:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. Start the Django development server:
   ```
   python manage.py runserver
   ```

## Usage
### Django Admin Interface
Access the Django admin interface at http://localhost:8000/admin/ to manage frameworks, versions, tags, and documentation files.

### Generating Documentation
Run the documentation generation scripts located in `get_doc_scripts/tools/` for different frameworks. For example, to generate documentation for FastAPI:

`poetry run python get_doc_scripts/tools/fast-api/make_doc.py`


## API
The project provides a FastAPI-based API for accessing framework details and documentation. Start the FastAPI server:

`uvicorn api:app --reload`

Access the API documentation at http://localhost:8000/docs.

### Configuration
Database and storage settings can be configured in `contextdb/settings.py`.

`.gitignore` is configured to exclude sensitive files and directories such as `creds.json`, `.idea`, `venv`, and `db.sqlite3`.

### Dependencies
- Django and various Django extensions for the backend.
- Playwright for automated web scraping.
- FastAPI and Uvicorn for the API layer.
- Google Cloud libraries for storage integration.

Refer to `pyproject.toml` for a complete list of dependencies.

### Project Structure
- `core/`: Django app containing models, views, and admin configuration.
- `get_doc_scripts/`: Scripts for generating documentation files.
- `api.py`: FastAPI application for serving the API.

### Contributing
Contributions are welcome! Please fork the repository and submit pull requests with your changes.

### License
This project is open-source and available under the MIT License.
