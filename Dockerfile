FROM python:3.8-slim-buster
# set work directory
WORKDIR /regFlask

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 2610


# Run the Flask app
CMD ["python", "app.py"]