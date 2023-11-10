# Job Trend
개발자 채용공고 데이터 추출 파이프라인 구축 및 응용 프로젝트

## Background
🤔 _데이터 엔지니어 직무는 어떤 기술스택이 필요할까?_<br>
🧐 _Python을 다룰 줄 알면 어떤 직무에서 일할 수 있을까?_

Job Trend 프로젝트는 이러한 궁금증에서 시작하게 되었습니다.<br>
각 채용공고 사이트 정보를 통해 개발자 직무별/기술스택별 유의미한 정보를 추출하여     
성장을 꿈꾸는 개발자들에게 도움이 되고자 합니다 🚀

![Dashboard](./img/dashboard.jpg)

## Install & Run
```bash
# install prerequisites
./initialize.sh

# run
./run.sh
```

## Architecture
![Architecture](./img/architecture.png)

### _Data Sources_
- 여러 채용공고 사이트들로부터 개발자 채용공고 정보를 추출합니다.
  - [x] Jumpit
  - [ ] 잡플래닛
  - [ ] 원티드
  - [ ] 잡코리아
  - [ ] ...

### _Extract_
- `Selenium`을 이용하여 동적 크롤링을 진행합니다.
- 직무별 채용공고 url을 추출한 뒤, 각 url에 접근하여 page source를 추출합니다.

### _Transform_
- 추출한 각 사이트 채용공고별 page source들을 아래와 같은 정보로 변환합니다.  
    - 공고 제목
    - 회사명
    - 직무
    - 기술스택
    - 마감일
    - 복지 및 혜택
    - ...

### _Load_
- 변환된 데이터를 Data Warehouse에 저장합니다.
- Data Warehouse로는 `Google BigQuery`를 이용합니다. 

### _Batch Processing (future work)_
- `Airflow`를 통해 기반으로 일별 batch processing을 통해 데이터를 업데이트 합니다.
- `Kubernetes(k8s)` 또는 `Google Cloud Composer`를 통해 Airflow를 구동시킵니다.

### _Visualization_
- `Redash`를 통해 SQL문을 기반으로 대시보드를 생성합니다.
- 직무별 상위 기술스택 및 기술스택별 상위 직무 등의 정보를 Bar 및 Pie chart 뿐만 아니라, Sankey 및 Sunburst Sequence chart 등을 통해 제공합니다. 
- 직무(JOB), 기술스택(TECH STACK), 마감일(DEADLINE) parameter를 통해 동적으로 반응하는 대시보드를 구현합니다.

### _Chatbot with LLM (future work)_
- 추출된 채용공고 내용을 LLM에 학습시킨 뒤, 개발자 채용과 관련된 내용을 답할 수 있는 챗봇을 생성합니다. 
- NAVER Cloud Platform에서 제공하는 `CLOVA Studio API`를 이용합니다.

