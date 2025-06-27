import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from haversine import haversine, Unit
import numpy as np

# 예제용 데이터프레임 (food_df를 대체)
np.random.seed(42)

food_df = pd.read_csv("food_df.csv")

st.title("🖱️ 지도에서 클릭하여 상권 분석하기")

# 업종 및 반경 설정
category = st.selectbox("찾고 싶은 업종 (중분류)", sorted(food_df["상권업종중분류명"].unique()))
radius = st.slider("반경 거리 (미터)", min_value=100, max_value=1000, value=300, step=50)

# 1. 지도 생성 (서울 중심)
m = folium.Map(location=[37.55, 126.98], zoom_start=13)

# 2. 지도 클릭 정보 받아오기
map_data = st_folium(m, width=700, height=500)

# 3. 클릭 위치가 있으면 분석 진행
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    target_point = (lat, lon)

    # 분석용 지도 다시 생성
    m = folium.Map(location=[lat, lon], zoom_start=16)

    # 중심 마커
    folium.Marker(
        location=[lat, lon],
        popup="선택한 지점",
        icon=folium.Icon(color="red", icon="star")
    ).add_to(m)

    # 반경 원
    folium.Circle(
        location=[lat, lon],
        radius=radius,
        color="blue",
        fill=True,
        fill_opacity=0.1
    ).add_to(m)

    # 업종 필터링
    target_df = food_df[food_df["상권업종중분류명"] == category].copy()

    # 거리 계산
    target_df["거리"] = target_df.apply(
        lambda row: haversine(target_point, (row["위도"], row["경도"]), unit=Unit.METERS),
        axis=1
    )

    nearby_df = target_df[target_df["거리"] <= radius]

    # 경쟁 점포 마커
    for _, row in nearby_df.iterrows():
        folium.Marker(
            location=[row["위도"], row["경도"]],
            popup=row["상호명"],
            icon=folium.Icon(color="green", icon="cutlery")
        ).add_to(m)

    # 결과 출력
    st.write(f"🧮 선택한 지점: 위도 {lat:.6f}, 경도 {lon:.6f}")
    st.write(f"📊 반경 {radius}m 내 `{category}` 업종 수: **{len(nearby_df)}개**")
    st.dataframe(nearby_df[['상호명', '거리']].sort_values("거리"))

    # 지도 출력
    st_folium(m, width=700, height=500)
else:
    st.info("🖱️ 지도를 클릭하면 분석이 시작됩니다!")
