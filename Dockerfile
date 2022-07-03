FROM python:3.10.4

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

RUN chmod +x ./prestart.sh

RUN chmod +x ./scripts/test.sh

RUN ./scripts/test.sh

RUN ./prestart.sh

RUN chmod +x ./scripts/start.sh

CMD ["./scripts/start.sh"]
