#!/bin/bash

if [[ "${1}" == "celery" ]]; then
  celery --app=src.Tasks.app_celery:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
  celery --app=src.Tasks.app_celery:celery flower
fi