FROM python:3.12.0-alpine3.18

# install poetry
RUN pip3 install poetry

# Copy source code to the working directory
COPY . /app

# Set the working directory
WORKDIR /app

# install dependencies
RUN poetry install --without dev

# Run the application
CMD ["poetry", "run", "python", "api.py"]


