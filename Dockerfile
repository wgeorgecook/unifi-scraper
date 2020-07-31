FROM python:3.8

RUN pip install pipenv

ENV PROJECT_DIR /usr/local/src/unifi-scraper

WORKDIR ${PROJECT_DIR}

COPY Pipfile Pipfile.lock ${PROJECT_DIR}/

RUN pipenv install --system --deploy

COPY unifi.py ${PROJECT_DIR}

CMD ["python", "unifi.py"]