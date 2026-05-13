FROM python:3.10-alpine

WORKDIR /fastapi_db

ENV PYTHONPATH=/fastapi_db

RUN apk add --no-cache gcc musl-dev libffi-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x fastapi_app/src/start.sh

EXPOSE 8000

CMD ["fastapi_app/src/start.sh"]