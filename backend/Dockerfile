FROM python:3.13
WORKDIR /usr/local/app

COPY . ./backend
RUN pwd && ls
RUN pip install --no-cache-dir -r backend/requirements.txt

EXPOSE 8000

RUN useradd app
USER app

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
