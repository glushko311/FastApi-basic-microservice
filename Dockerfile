
    FROM python:3.8

    #
    WORKDIR /code

    #
    COPY ./requirements.txt /code/requirements.txt

    RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

    COPY ./migrations /code/migrations
    COPY ./src /code/src
    COPY ./tests /code/tests
    COPY ./.env /code/.env
    COPY ./config.py /code/config.py
    COPY ./alembic.ini /code/alembic.ini


#     CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80"]
