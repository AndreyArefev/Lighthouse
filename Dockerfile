FROM python:latest

RUN mkdir /lighthouse

WORKDIR /lighthouse

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x ./scripts/*.sh

CMD ["gunicorn", "src.pass_main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]