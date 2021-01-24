FROM jordanirabor/python3.7-pip-pipenv:latest
WORKDIR /app
COPY requirements_dev.txt .
RUN pip install -r requirements_dev.txt
COPY . .
CMD ["python", "./inuinouta/manage.py", "runserver", "0.0.0.0:8000"]
