#!/bin/bash

if [ -z "$1" ]
then
    echo "No migration name provided"
    exit 1
fi

poetry run alembic revision --autogenerate -m "$1"