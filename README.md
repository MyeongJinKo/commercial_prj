# 서울시 상권분석 프로젝트 v1

프로젝트 기간: 2025. 06. 24 ~ 2025. 07. 03

----------
## 1. 주제
특정 지점의 식당, 카페, 주점 등 특정 음식점 업종이 어떻게 분포되어 있는지 앱/웹을 통해 간단히 확인한다.

----------
## 2. 구현 방법
1. 쉽게 배포가 가능한 streamlit을 사용하여 앱/웹으로 구현하였으며, 배포는 github cloud를 통해 무료 배포로 한다.
2. 음식점 카테고리 선택창을 가독성 있게 구분하기 위해, 현재는 음식점 중분류명으로 구분한다.
3. 중심점으로부터 원하는 반경을 m로 선택할 수 있다.
<div align="center">
<img src="https://github.com/MyeongJinKo/commercial_prj/blob/main/images/v2_1.png" width="500" height="400" alt="사용법1">
<img src="https://github.com/MyeongJinKo/commercial_prj/blob/main/images/v2_2.png" width="500" height="400" alt="사용법2">
<img src="https://github.com/MyeongJinKo/commercial_prj/blob/main/images/v2_3.png" width="500" height="400" alt="사용법3">
<img src="https://github.com/MyeongJinKo/commercial_prj/blob/main/images/v2_4.png" width="500" height="400" alt="사용법4">
</div>

----------
## 3. 향후 업데이트 방안
### 3-1. 검색 후 발견된 상점들의 주변 상권에 대한 정보
상권마다 존재하는 예상 매출액 혹은 방문하는 소비자 패턴 정보 추가
### 3-2. 예측 모델링 생성
특정 지점에 특정 업종의 음식점을 오픈할 경우, 다양한 변수를 고려하여 창업 오픈과 관련하여 추천 시스템 구현
