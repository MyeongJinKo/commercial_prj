import streamlit as st
import pandas as pd
import numpy as np
import folium
from haversine import haversine, Unit
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="상권분석 프로젝트", layout="wide")

# 사이드바 페이지 목록
pages = {
    "프로젝트 소개": "intro",
    "지도 기반 상권 분석": "map",
    "모델링 결과": "model"
}

# 세션 상태로 페이지 기억
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "프로젝트 소개"

st.sidebar.title("상권분석 프로젝트")
for page_name in pages:
    if st.sidebar.button(page_name):
        st.session_state.selected_page = page_name

# (작성자 정보 등 사이드바 하단에 추가)
st.sidebar.markdown("---")
st.sidebar.markdown("### 작성자: 고명진")
st.sidebar.markdown("✉️ gkdis40@naver.com")

# 현재 페이지 분기
page = st.session_state.selected_page

if page == "프로젝트 소개":
    st.title("프로젝트 소개")
    st.image("https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=800&q=80", caption="서울의 도시 풍경", use_column_width=True)

    st.markdown("""
    ## 프로젝트 개요
    - 본 프로젝트는 **서울시 상권정보**와 상권 내 업종 데이터를 활용하여,
      업종·지역별 경쟁력과 입지 분석을 지원하는 데이터 기반 지도 분석 웹앱을 구축하는 것을 목표로 합니다.

    ## 주요 기능
    - **지도 기반 업종 분포 시각화**  
      (지도에서 위치 클릭 시, 반경 내 업종 매장 위치 및 경쟁 매장 수 표시)
    - **업종·소분류별 필터링 및 비교**
    - **향후 모델링 기반 입지 추천/성장성 예측 기능까지 확장 예정**

    ## 프로젝트 동기 및 배경
    - 창업자·소상공인의 **입지 선정 및 경쟁력 평가**에 실질적인 도움을 주는 데이터 도구가 필요
    - 공공데이터 및 민간 상권 데이터를 활용한 **현실적인 상권분석 서비스** 구축
    - 지도, 통계, 머신러닝 등 다양한 기술을 실전 프로젝트에 접목

    ## 사용 데이터 및 도구
    - **데이터:** 서울시 상권·점포정보, 공공데이터포털 API 등
    - **분석/개발:** Python, Pandas, Folium, Streamlit, Scikit-learn 등

    ## 기대 효과
    - **창업자·사업자 맞춤 상권분석 지원**
    - 데이터 기반 입지 전략 수립 및 경쟁사 분석
    - 향후 확장 시, 머신러닝 모델 기반 추천·예측 서비스로 발전 가능

    ---

    **작성자:** 고명진  
    ✉️ [gkdis40@naver.com](mailto:gkdis40@naver.com)
    """)

elif page == "지도 기반 상권 분석":
    # 👉 여기에 올려준 지도 기반 상권분석 코드 전체 복붙!
    # ---- 예시로 아래 줄만 대체 (여기에 기존 코드 넣으세요) ----
    # 데이터 불러오기
    food_df = pd.read_csv("food_commercial_data.csv")
    food_df["상호명"] = food_df["상호명"].astype(str).str.replace('\n', ' ').str.strip()

    # 1. 제목 및 사용자 입력
    st.title("🗺️ 지도 클릭으로 상권 분석")

    # 2. 1차 선택: 중분류
    mid_categories = sorted(food_df["상권업종중분류명"].unique())
    st.markdown("### 1. 분석할 업종 중분류를 선택해주세요")
    selected_mid = st.selectbox("", mid_categories)

    # 3. 2차 선택: 소분류 (중분류에 따라 필터링)
    sub_options = sorted(food_df[food_df["상권업종중분류명"] == selected_mid]["상권업종소분류명"].unique())
    st.markdown("### 2. 분석할 업종 소분류를 선택해주세요")
    selected_sub = st.selectbox("", sub_options)

    # 4. 거리 선택 슬라이더
    st.markdown("### 3. 반경 거리를 설정해주세요(미터)")
    radius = st.slider("", min_value=100, max_value=2000, value=300, step=50)

    st.markdown("### 4. 아래 지도에서 마우스로 원하는 위치를 클릭하세요.")

    # 5. 초기 지도 위치 설정
    map_center = [37.511146, 126.974786]
    m = folium.Map(location=map_center, zoom_start=12)

    # 6. 맵 렌더링
    map_data = st_folium(m, width=1200, height=700)

    # 7. 클릭된 지점이 있을 때만 분석
    if map_data and map_data.get("last_clicked"):
        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]
        target_point = (lat, lon)

        st.markdown("### 5. 분석 결과")
        # 클릭 지점 지도에 마커 및 원 추가
        m = folium.Map(location=[lat, lon], zoom_start=15)
        folium.Marker([lat, lon], popup="선택한 지점", icon=folium.Icon(color="red", icon="star")).add_to(m)
        folium.Circle([lat, lon], radius=radius, color="blue", fill=True, fill_opacity=0.1).add_to(m)

        # 업종 필터링 및 거리 계산
        target_df = food_df[
            (food_df["상권업종중분류명"] == selected_mid) &
            (food_df["상권업종소분류명"] == selected_sub)
        ].copy()

        target_df["거리"] = target_df.apply(
            lambda row: haversine(target_point, (row["위도"], row["경도"]), unit=Unit.METERS),
            axis=1
        )
        nearby_df = target_df[target_df["거리"] <= radius]

        for _, row in nearby_df.iterrows():
            # 팝업 HTML 내용 수정: div width를 늘려서 내용이 잘 보이도록 함
            popup_html = f'<div style="width:350px;"><strong>{row["상호명"]}</strong><br/>\
                주소: {row["도로명주소"]}<br/>\
                거리: {round(row["거리"], 1)}m<br/>\
                상권평균매출금액: {round(row["평균_매출_금액"])}원<br/>\
                상권평균매출건수: {round(row["평균_매출_건수"])}건</div>'
                

            folium.Marker(
                [row["위도"], row["경도"]],
                popup=folium.Popup(popup_html, max_width=450),
                icon=folium.Icon(color="green", icon="cutlery")
            ).add_to(m)
        # 결과 출력
        st.markdown(f"##### 📍 선택한 위치: **위도 {lat:.5f}, 경도 {lon:.5f}**")
        st.markdown(f"##### 🔍 반경 **{radius}m** 내 `{selected_mid} > {selected_sub}` 업종 수: **{len(nearby_df)}개**")
        st.dataframe(nearby_df[["상호명", "거리"]].sort_values("거리"))

        # 결과 지도 렌더링
        st_folium(m, width=1200, height=700)
        # --------------------------------------------------------
        # 실제로는 당신이 올린 전체 Streamlit 지도분석 코드 붙이면 됨

elif page == "모델링 결과":
    st.title("모델링 결과")
    st.markdown("### (작성예정)")
