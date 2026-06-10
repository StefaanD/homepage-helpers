FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apk add --no-cache freeipmi

COPY . .

EXPOSE 8383

HEALTHCHECK CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:8383/health || exit 1

CMD ["gunicorn", "-b", "0.0.0.0:8383", "app:app"]