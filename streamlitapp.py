import streamlit as st
import pandas as pd
import numpy as np
import folium
from haversine import haversine, Unit
from streamlit_folium import st_folium

# 예시 데이터: 실제 food_df로 교체 가능
np.random.seed(42)

food_df = pd.read_csv("food_df.csv")

# 제목 및 사용자 입력
st.title("🗺️ 지도 클릭으로 상권 분석")

category = st.selectbox("분석할 업종 (중분류)", sorted(food_df["상권업종중분류명"].unique()))
radius = st.slider("반경 거리 (미터)", min_value=100, max_value=1000, value=300, step=50)

st.markdown("🖱️ 아래 지도에서 마우스로 원하는 위치를 클릭하세요.")

# 초기 지도 위치 설정 (서울 중심)
map_center = [37.55, 126.98]

# 빈 지도 생성 (클릭 여부에 따라 중심이 바뀜)
m = folium.Map(location=map_center, zoom_start=14)

# 처음 맵 렌더링
map_data = st_folium(m, width=700, height=500)

# 클릭된 지점이 있을 때만 분석
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    target_point = (lat, lon)

    # 📍 클릭 지점 지도에 마커 및 원 추가
    m = folium.Map(location=[lat, lon], zoom_start=16)
    folium.Marker([lat, lon], popup="선택한 지점", icon=folium.Icon(color="red", icon="star")).add_to(m)
    folium.Circle([lat, lon], radius=radius, color="blue", fill=True, fill_opacity=0.1).add_to(m)

    # 🔎 업종 필터링 및 거리 계산
    target_df = food_df[food_df["상권업종중분류명"] == category].copy()
    target_df["거리"] = target_df.apply(
        lambda row: haversine(target_point, (row["위도"], row["경도"]), unit=Unit.METERS),
        axis=1
    )
    nearby_df = target_df[target_df["거리"] <= radius]

    # 🏪 경쟁 점포 마커 추가
    for _, row in nearby_df.iterrows():
        folium.Marker(
            [row["위도"], row["경도"]],
            popup=row["상호명"],
            icon=folium.Icon(color="green", icon="cutlery")
        ).add_to(m)

    # 결과 출력
    st.markdown(f"📍 선택한 위치: **위도 {lat:.5f}, 경도 {lon:.5f}**")
    st.markdown(f"🔍 반경 **{radius}m** 내 `{category}` 업종 수: **{len(nearby_df)}개**")
    st.dataframe(nearby_df[["상호명", "거리"]].sort_values("거리"))

    # 결과 지도 렌더링
    st_folium(m, width=700, height=500)
