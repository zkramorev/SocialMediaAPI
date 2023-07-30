FROM python:3.11

RUN mkdir /social_media_api

WORKDIR /social_media_api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /social_media_api/docker/*.sh

CMD ["gunicorn", "app.main:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]