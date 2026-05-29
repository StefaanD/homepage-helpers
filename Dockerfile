FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apk add --no-cache freeipmi

COPY . .

EXPOSE 8383

CMD ["python", "app.py"]