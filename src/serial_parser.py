import serial
import os
import time
from protocol_loader import load_protocols
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

meta, protocols = load_protocols()

def parse_meta(data, meta):
    """
    주어진 데이터와 메타 정보를 사용하여 메타 데이터를 파싱합니다.

    Args:
        data (bytearray): 파싱할 데이터.
        meta (dict): 메타 정보.

    Returns:
        dict: 파싱된 메타 데이터.
    """
    parsed_meta = {}
    for field_name, field_info in meta.items():
        byte_index = field_info["byte"]
        mask = int(field_info["mask"], 16)  # HEX로 정의된 값을 10진수 정수로 변환
        shift = field_info["shift"]
        if byte_index < len(data):
            value = (data[byte_index] & mask) >> shift
            parsed_meta[field_name] = value
    return parsed_meta

def parse_data(data):
    """
    로드된 프로토콜과 메타 정보를 사용하여 데이터를 파싱합니다.

    Args:
        data (bytearray): 파싱할 데이터.

    Returns:
        tuple: 프로토콜 이름과 파싱된 데이터를 담고 있는 튜플.
    """
    meta_data = parse_meta(data, meta)
    protocol_key = meta_data.get('command')

    if protocol_key in protocols:
        protocol = protocols[protocol_key]
        parsed_data = protocol.parse(data[:protocol.length])
        parsed_data.update(meta_data)
        return protocol.name, parsed_data
    else:
        return '[!] Unknown Protocol', {}

def read_serial_data():
    """
    시리얼 포트에서 데이터를 읽고 로드된 프로토콜과 메타 정보를 사용하여 파싱합니다.
    """
    port = os.getenv('SERIAL_PORT')
    baudrate = int(os.getenv('SERIAL_BAUDRATE', 4800))
    timeout = float(os.getenv('SERIAL_TIMEOUT', 1))
    packet_timeout = float(os.getenv('PACKET_TIMEOUT', 0.1))

    try:
        ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
    except serial.SerialException as e:
        raise RuntimeError(f"[!] 시리얼 포트를 오픈하는데 실패하였습니다.: {e}")
    
    try:
        buffer = bytearray()
        last_byte_time = time.time()

        while True:
            if ser.in_waiting > 0:
                data = ser.read(1)
                buffer.extend(data)
                last_byte_time = time.time()
            else:
                current_time = time.time()
                if buffer and (current_time - last_byte_time > packet_timeout):
                    protocol_name, parsed_data = parse_data(buffer)
                    print(f'Protocol: {protocol_name}, Data: {parsed_data}')
                    buffer.clear()
    except KeyboardInterrupt:
        print("[!] 시리얼 포트가 닫혀있습니다.")
    finally:
        ser.close()