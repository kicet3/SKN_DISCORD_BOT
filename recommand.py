import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
import math
from dotenv import load_dotenv
import os
load_dotenv()

@dataclass
class Place:
    name: str
    address: str
    road_address: Optional[str]
    phone: Optional[str]
    place_url: Optional[str]
    x: float  # 경도 (longitude)
    y: float  # 위도 (latitude)

def calculate_bounding_box(center_lat: float, center_lng: float, vertical_meters: float, horizontal_meters: float) -> str:
    METERS_PER_DEGREE_LAT = 110574 

    delta_lat_meters = vertical_meters / 2
    delta_lat_degrees = delta_lat_meters / METERS_PER_DEGREE_LAT

    lat_rad = math.radians(center_lat) 
    METERS_PER_DEGREE_LNG = 111320 * math.cos(lat_rad)
    
    delta_lng_meters = horizontal_meters / 2
    delta_lng_degrees = delta_lng_meters / METERS_PER_DEGREE_LNG

    min_y = center_lat - delta_lat_degrees
    max_y = center_lat + delta_lat_degrees
    min_x = center_lng - delta_lng_degrees
    max_x = center_lng + delta_lng_degrees

    return f"{min_x},{min_y},{max_x},{max_y}"

def search_places(keyword: str, api_key: str, rect_bounds: Optional[str] = None) -> List[Place]:
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {
        "Authorization": f"KakaoAK {api_key}"
    }
    params = {
        "query": keyword,
        "size": 15 # 카카오 API는 기본 15개, 최대 45개. 한 페이지에 가져올 수 있는 최대 개수.
    }
    
    if rect_bounds:
        params["rect"] = rect_bounds
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data["meta"]["total_count"] == 0:
            return []
            
        places = []
        
        for item in data.get("documents", []):
            print(item)
            place = Place(
                name=item.get("place_name"),
                address=item.get("address_name"),
                road_address=item.get("road_address_name"),
                phone=item.get("phone"),
                place_url=item.get("place_url"),
                x=float(item.get("x")),
                y=float(item.get("y"))
            )
            places.append(place)
            
        return places
        
    except requests.exceptions.RequestException as e:
        return []

def format_place_info(place: Place) -> str:
    info = [
        f"장소명: {place.name}",
        f"주소: {place.address}"
    ]
    
    if place.road_address:
        info.append(f"도로명 주소: {place.road_address}")
    if place.phone:
        info.append(f"전화번호: {place.phone}")
    if place.place_url:
        info.append(f"장소 상세 정보: {place.place_url}")
    return "\n".join(info)

def get_coordinates(keyword: str, api_key: str) -> Optional[tuple[float, float]]:
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {
        "Authorization": f"KakaoAK {api_key}"
    }
    params = {
        "query": keyword,
        "size": 1
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data["meta"]["total_count"] == 0:
            return None
            
        result = data["documents"][0]
        return float(result["x"]), float(result["y"])
        
    except requests.exceptions.RequestException as e:
        return None

# --- 프로그램 실행 부분 ---

def get_place_info(keyword: str, center_keyword: Optional[str] = None) -> List[Place]:
    API_KEY = os.getenv("KAKAO_API_KEY")
    if not API_KEY:
        return [] # API 키가 없으면 빈 리스트 반환

    center_lat, center_lng = None, None

    if center_keyword: # 중심 키워드가 제공된 경우
        coords = get_coordinates(center_keyword, API_KEY)
        if coords:
            center_lng, center_lat = coords # get_coordinates는 (경도, 위도)를 반환
        else:
            # 중심 키워드 좌표를 찾지 못하면 고정된 기본값 사용
            center_lat = 37.4682799445558
            center_lng = 126.886197427546
    else: # 중심 키워드가 제공되지 않은 경우
        # 고정된 기본 중심 좌표 사용
        center_lat = 37.4682799445558
        center_lng = 126.886197427546

    VERTICAL_RANGE_METERS = 500
    HORIZONTAL_RANGE_METERS = 500

    rect_bounds_string = calculate_bounding_box(
        center_lat, center_lng,
        VERTICAL_RANGE_METERS, HORIZONTAL_RANGE_METERS
    )
    places = search_places(keyword, API_KEY, rect_bounds=rect_bounds_string)

    return places # 찾은 장소 리스트 반환 (없으면 빈 리스트)


