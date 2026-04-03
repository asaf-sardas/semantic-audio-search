FROM python:3.13
WORKDIR /usr/local/app

COPY . ./processor
RUN pip install --no-cache-dir -r processor/requirements.txt

EXPOSE 8001

RUN useradd app
USER app

CMD ["uvicorn", "processor.main:app", "--host", "0.0.0.0", "--port", "8001"]
