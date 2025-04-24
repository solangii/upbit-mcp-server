FROM python:3.10-slim

WORKDIR /app

# 먼저 의존성 파일 복사
COPY pyproject.toml .
COPY requirements.txt* ./

# 의존성 설치 - requirements.txt가 있으면 그것을 사용, 없으면 pyproject.toml 사용
RUN if [ -f requirements.txt ]; then \
        pip install --no-cache-dir -r requirements.txt; \
    else \
        pip install --no-cache-dir build && \
        pip install --no-cache-dir .; \
    fi

# 애플리케이션 파일 복사
COPY main.py config.py ./
COPY tools/ ./tools/
COPY prompts/ ./prompts/
COPY resources/ ./resources/

# 환경 변수 설정
ENV UPBIT_ACCESS_KEY=""
ENV UPBIT_SECRET_KEY=""

EXPOSE 8000

CMD ["python", "main.py"]
