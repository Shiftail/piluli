FROM python:3.13.3-slim
WORKDIR /src

COPY ./requirements.txt /src/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt
COPY ./app /src/app

CMD ["python", "app/main.py"]
