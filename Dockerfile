FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml .
COPY requirements.txt* ./

RUN if [ -f requirements.txt ]; then \
        pip install --no-cache-dir -r requirements.txt; \
    else \
        pip install --no-cache-dir build && \
        pip install --no-cache-dir .; \
    fi

COPY main.py config.py ./
COPY tools/ ./tools/
COPY prompts/ ./prompts/
COPY resources/ ./resources/

ENV UPBIT_ACCESS_KEY=""
ENV UPBIT_SECRET_KEY=""

EXPOSE 8000

CMD ["python", "main.py"]
