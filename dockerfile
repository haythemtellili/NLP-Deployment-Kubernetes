FROM python:3.9-slim-bullseye

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

# COPY requirements.txt .
COPY requirements.txt .
# Install dependencies:
RUN pip install -r requirements.txt

COPY . . 

# Run the application:
EXPOSE 9999

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9999", "--timeout", "6000", "app:app"]