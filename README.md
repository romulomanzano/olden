# Olden

Sample app to allow adult day care facilities to remain connected with their customers during the pandemic.


# Backend

## Technologies
- Python3.7 + Flask

## DB
Mongo DB

## Creating a local development environment

### Python3.7 Environment
- Create a virtual env
  - Upgrade pip
  - Install pip-tools: `pip install pip-tools`
  - If requirements-dev.txt and requirements.txt file not generated, run:
    - pip-compile requirement-dev.in
    - pip-compile requirements.txt
  - Run:
    - pip install -r requirements-dev.txt
    - pip install -r requirements.txt
  - Run:
    - pre-commit install

## Server deployment

Hosted on render.com. Use the below build command:

`pip install wheel && pip install --upgrade pip && pip install -r requirements.txt`


### Stack:
- Flask
- Gunicorn

# Frontend

- VueJs + Javascript


# Relevant API SaaS integrations

- https://daily.co
- https://cotter.app
- https://courier.com (and Twilio + Postmark to handle comms)
- https://cloud.mongodb.com

## Secret Management
- https://doppler.com

