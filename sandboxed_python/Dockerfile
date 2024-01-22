FROM python:slim
WORKDIR /usr/src/app
COPY *.py /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./run.py"]
