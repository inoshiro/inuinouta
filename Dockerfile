FROM python:3.12-slim
WORKDIR /app
COPY requirements_dev.txt .
RUN pip install -r requirements_dev.txt
COPY . .
CMD ["python", "./inuinouta/manage.py", "runserver", "0.0.0.0:8000"]
