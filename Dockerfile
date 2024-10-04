
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --index-url https://mirrors.sustech.edu.cn/pypi/simple

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
