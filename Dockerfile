FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir build && \
    pip install --no-cache-dir .

COPY . .

ENV UPBIT_ACCESS_KEY=""
ENV UPBIT_SECRET_KEY=""

EXPOSE 8000

CMD ["python", "main.py"]