import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Protocol:
    
    def __init__(self, name, length, fields):
        self.name = name
        self.length = length
        self.fields = fields

    def parse(self, data):
        """
        프로토콜 정의에 따라 데이터를 파싱합니다.

        Args:
            data (bytearray): 파싱할 데이터.

        Returns:
            dict: 파싱된 데이터 필드.
        """
        parsed_data = {}
        for field_name, field_info in self.fields.items():
            byte_index = field_info["byte"]
            mask = int(field_info["mask"], 16)  # 16진수 문자열을 정수로 변환
            shift = field_info["shift"]
            if byte_index < len(data):
                value = (data[byte_index] & mask) >> shift
                parsed_data[field_name] = value
        return parsed_data

def load_protocols():
    """
    환경 변수로 지정된 JSON 파일에서 프로토콜 정의를 로드합니다.

    Returns:
        tuple: 메타 정보와 프로토콜 정의.
    """
    protocol_file_path = os.getenv('PROTOCOLS_FILE_PATH')
    if not protocol_file_path:
        raise ValueError("[!] 환경 변수 PROTOCOLS_FILE_PATH가 설정되지 않았습니다")

    try:
        with open(protocol_file_path, 'r') as file:
            config = json.load(file)
            meta = config.get("meta")
            protocols = {}
            for key, proto in config["protocols"].items():
                if key == "meta":
                    continue
                name = proto.get("name")
                length = proto.get("length")
                fields = proto.get("fields")
                key = int(key, 16)
                protocols[key] = Protocol(name, length, fields)
            return meta, protocols
    except FileNotFoundError:
        raise FileNotFoundError(f"[!] 프로토콜 파일을 찾을 수 없습니다: {protocol_file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"[!] 프로토콜 파일에서 JSON을 디코딩하는 중 오류가 발생했습니다: {protocol_file_path}")
