FROM python:3.10-slim-bookworm

WORKDIR /app

COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["bash", "entrypoint.sh"]
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
