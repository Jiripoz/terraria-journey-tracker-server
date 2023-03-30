FROM python:3.10.10-bullseye

# Copy the project
COPY . /app
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Run the app
CMD ["python", "start.py"]
