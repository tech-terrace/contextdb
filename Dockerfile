FROM python:3.12

# install poetry
RUN pip3 install poetry

# Set the working directory
WORKDIR /app

# Copy only files needed for installing dependencies
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry install --without dev

# Copy the rest of the application code
COPY . /app

# Run the application
CMD ["poetry", "run", "python", "api.py"]