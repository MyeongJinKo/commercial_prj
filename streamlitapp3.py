import streamlit as st
import pandas as pd
import numpy as np
import folium
from haversine import haversine, Unit
from streamlit_folium import st_folium

# Streamlit 설정 와이드
st.set_page_config(layout="wide")

# 데이터 불러오기
food_df = pd.read_csv("food_df.csv")
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
map_data = st_folium(m, width=700, height=500)

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
            거리: {round(row["거리"], 1)}m</div>'

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
    st_folium(m, width=700, height=500)
