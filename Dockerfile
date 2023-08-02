FROM python:3.8-slim-buster
# set work directory
WORKDIR /reg_page

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 2610

# Set the environment variable to run the Flask app
ENV FLASK_APP=app.py

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=2610"]