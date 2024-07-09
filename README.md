# SerialProtocolParser
JSON 형식으로 사전에 저장된 프로토콜 정의를 기반으로 시리얼 통신 데이터를 동적으로 파싱하는 툴입니다.

## Configuration

사전에 정의된 프로토콜은 config/protocols.json 파일에서 수정 및 추가할 수 있습니다. 이 파일은 ACP 명령들만 적용될 수 있도록 구현되어 있습니다. 이 파일의 경로는 .env 파일에 추가해야 합니다.

## Environment Variables

`.env` 파일을 통해서 JSON 파일의 경로와 시리얼 포트 설정을 해주세요.

## Running the Project

1. 필수 라이브러리 설치
   ```sh
   `pip install pyserial python-dotenv`

2. `python src/main.py`
