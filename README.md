# 카카오맵 기반 장소 검색 애플리케이션

이 애플리케이션은 Flask를 사용하여 카카오맵 API를 통한 장소 검색 기능을 제공합니다.

## 설치 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. 카카오맵 API 키 설정:
- `templates/index.html` 파일에서 `YOUR_KAKAO_MAP_API_KEY`를 실제 카카오맵 API 키로 교체하세요.

## 실행 방법

```bash
python app.py
```

서버가 실행되면 웹 브라우저에서 `http://localhost:5000`으로 접속하여 애플리케이션을 사용할 수 있습니다.

### python version
```
  3.12
```
### 기본 패키지 설치
```
  pip install -r requirements.txt
```
### bot.py

변수 resuarant_url dic에 key 새로운 구내식당에 대한 카카오톡 채널 주소 posts를 추가하면 해당 구내식당의 점심 메뉴 정보도 가져올 수 있습니다.

### .env
.env copy 파일을 .env로 변경 후 discord api key를 변경하여 개인 봇으로 사용 가능합니다.
