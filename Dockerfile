FROM python:3.10.10-bullseye

# Create the player file to mount
WORKDIR /opt
RUN touch /opt/player.plr

# Copy the project
COPY . /app
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 4777

# Run the app
ENTRYPOINT [ "python", "start.py" ]
CMD [ "" ]