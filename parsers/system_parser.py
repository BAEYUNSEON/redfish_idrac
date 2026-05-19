# parsers/system_parser.py
# ─────────────────────────────────────────────
# iDRAC 시스템 정보 JSON 파서
# ─────────────────────────────────────────────


def parse_system_info(data: dict) -> dict:
    """
    /redfish/v1/Systems/System.Embedded.1 응답에서
    주요 시스템 정보를 추출합니다.

    Args:
        data (dict): iDRAC API에서 받은 JSON 딕셔너리

    Returns:
        dict: 파싱된 시스템 정보
    """
    if not data:
        return {}

    parsed = {
        "서버명":          data.get("HostName", "N/A"),
        "모델":            data.get("Model", "N/A"),
        "제조사":          data.get("Manufacturer", "N/A"),
        "서비스태그":      data.get("SKU", "N/A"),
        "시리얼번호":      data.get("SerialNumber", "N/A"),
        "전원상태":        data.get("PowerState", "N/A"),
        "상태":            data.get("Status", {}).get("Health", "N/A"),
        "CPU수":           data.get("ProcessorSummary", {}).get("Count", "N/A"),
        "총메모리(GB)":    data.get("MemorySummary", {}).get("TotalSystemMemoryGiB", "N/A"),
        "BIOS버전":        data.get("BiosVersion", "N/A"),
    }
    return parsed


def print_system_info(parsed: dict):
    """시스템 정보를 보기 좋게 출력"""
    print("\n" + "=" * 50)
    print("  시스템 정보")
    print("=" * 50)
    for key, value in parsed.items():
        print(f"  {key:<18}: {value}")
    print("=" * 50)
