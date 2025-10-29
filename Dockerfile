# 1. 베이스 이미지 설정
# 가볍고 안정적인 Python 3.12 slim-buster 이미지를 사용합니다.
FROM python:3.12-slim-buster

# 2. 작업 디렉토리 설정
# 컨테이너 내에서 명령이 실행될 기본 디렉토리를 설정합니다.
WORKDIR /app

# 3. 환경 변수 설정
# Python이 .pyc 파일을 생성하지 않도록 하고, 버퍼링을 비활성화하여 로그가 즉시 출력되도록 합니다.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. 의존성 설치
# requirements.txt를 먼저 복사하여 Docker 캐시를 활용, 빌드 속도를 높입니다.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. 애플리케이션 코드 복사
COPY ./app /app

# 6. 포트 노출
# server.py에서 사용하는 8001 포트를 노출합니다.
EXPOSE 8001

# 7. 애플리케이션 실행
# 컨테이너가 시작될 때 실행할 명령어를 정의합니다.
CMD ["python", "server.py"]
