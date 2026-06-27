FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apk add --no-cache \
    freeipmi \
    postgresql-client

COPY . .

EXPOSE 8383

HEALTHCHECK CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:8383/health || exit 1

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "-b", "0.0.0.0:8383", "app:app"]