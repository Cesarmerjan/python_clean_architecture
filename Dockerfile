# Use the Python3.7 container image
FROM python:3.7

# Set the working directory to Docker as /app
WORKDIR /src

# Copy the current directory contents into the container at /app that was created in the line acima
ADD . /src

# Install the dependencies
RUN pip install -r requirements/prod.txt

# Run the command to start uWSGI
CMD gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 8 --timeout 0 src.make_a_comment.adapters.controllers.api:'create_api()'