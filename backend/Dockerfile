# Use an official Python runtime as a parent image
FROM python:3.11.3-slim-buster

# Set the working directory to /app
ENV PYTHONUNBUFFERED=1

WORKDIR /api

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install  -r /api/requirements.txt

# Run migrations and collect static files
RUN python /api/manage.py collectstatic --noinput

# Expose port 8000 for the Django app
EXPOSE 8000

# Start the Django app
CMD ["python", "/api/manage.py", "runserver", "0.0.0.0:8000"]
