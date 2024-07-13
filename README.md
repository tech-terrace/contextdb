# ContextDB Project

## Overview
ContextDB is a comprehensive web application designed to manage and serve up-to-date documentation for various software frameworks. It utilizes Google Cloud Storage for efficient file management and provides a robust API for accessing the data. The project includes automated scripts for generating documentation files, ensuring that the information remains current.

Visit our website: [https://context-db.com/](https://context-db.com/)

## Features
- Centralized management of frameworks, versions, and documentation variants
- Automated documentation generation for popular frameworks like React, Vue.js, FastAPI, Angular, and more
- RESTful API for querying framework details, versions, and documentation
- Integration with Google Cloud Storage for scalable and reliable file storage
- User-friendly interface for easy access to documentation

## Installation
1. Ensure Python 3.12 and Poetry are installed on your system.
2. Clone the repository and navigate to the project directory.
3. Install dependencies using Poetry:
   ```
   poetry install
   ```
4. Set up the environment:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. Start the development server:
   ```
   python manage.py runserver
   ```

## Usage
### Admin Interface
Access the admin interface at `http://localhost:8000/admin/` to manage frameworks, versions, tags, and documentation files.

### Generating Documentation
Run the documentation generation scripts located in `get_doc_scripts/tools/` for different frameworks. For example:

```
poetry run python get_doc_scripts/tools/fast-api/make_doc.py
```

## API
The project provides a FastAPI-based API for accessing framework details and documentation. Start the API server:

```
uvicorn api:app --reload
```

Access the API documentation at `http://localhost:8000/docs`.

## Configuration
- Database and storage settings can be configured in `contextdb/settings.py`.
- Sensitive files and directories are excluded in `.gitignore`.

## Dependencies
- Backend: Django and various extensions
- Web Scraping: Playwright
- API Layer: FastAPI and Uvicorn
- Storage: Google Cloud libraries

Refer to `pyproject.toml` for a complete list of dependencies.

## Project Structure
- `core/`: Main application containing models, views, and admin configuration
- `get_doc_scripts/`: Scripts for automated documentation generation
- `api.py`: FastAPI application serving the API
- `frontend/`: Vue.js-based frontend application

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests with your changes.

## License
This project is open-source and available under the MIT License.