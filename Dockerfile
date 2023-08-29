FROM python:3.10.5 as builder

WORKDIR /telegram_bot

COPY . /telegram_bot

FROM python:3.10.5

WORKDIR /telegram_bot

COPY --from=builder /telegram_bot /telegram_bot

RUN pip install --user -r requirements.txt

CMD ["python", "main.py"]
