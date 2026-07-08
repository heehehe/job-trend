FROM apache/airflow:2.8.2

# Firefox 설치
USER root
RUN apt-get update && \
    apt-get install -y firefox-esr && \
    apt-get install -y wget && \
    apt-get clean

# geckodriver 설치
#ARG GECKODRIVER_VERSION=0.30.0
#RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz && \
#    tar -xzf geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
#    rm geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz

# Python selenium 패키지 설치
#RUN pip install selenium==3.141.0

# 사용자를 다시 airflow로 전환
USER airflow


#COPY requirements.txt /
#RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
