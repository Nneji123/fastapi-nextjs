# Use an official Python runtime as a base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /prod

# Copy the requirements file into the container at /prod
COPY requirements.txt /prod/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container at /prod
COPY . /prod/

# Expose the port that Uvicorn listens to
EXPOSE 8090

# Run Uvicorn when the container launches
# CMD ["python", "api.asgi:api", "--host", "0.0.0.0", "--port", "8090", "--reload"]

CMD ["python", "api/app.py"]
