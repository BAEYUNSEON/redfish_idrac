# parsers/thermal_parser.py
# ─────────────────────────────────────────────
# iDRAC 온도 및 팬 정보 파서
# ─────────────────────────────────────────────


def parse_thermal_info(data: dict) -> dict:
    """
    /redfish/v1/Chassis/System.Embedded.1/Thermal 응답 파서

    Returns:
        dict: 온도 센서 및 팬 정보
    """
    if not data:
        return {}

    # 온도 센서 파싱
    temperatures = []
    for temp in data.get("Temperatures", []):
        temperatures.append({
            "센서명":        temp.get("Name", "N/A"),
            "현재온도(C)":   temp.get("ReadingCelsius", "N/A"),
            "상한경고(C)":   temp.get("UpperThresholdNonCritical", "N/A"),
            "상한위험(C)":   temp.get("UpperThresholdCritical", "N/A"),
            "상태":          temp.get("Status", {}).get("Health", "N/A"),
        })

    # 팬 정보 파싱
    fans = []
    for fan in data.get("Fans", []):
        fans.append({
            "팬명":       fan.get("Name", "N/A"),
            "RPM":        fan.get("Reading", "N/A"),
            "단위":       fan.get("ReadingUnits", "N/A"),
            "상태":       fan.get("Status", {}).get("Health", "N/A"),
        })

    return {"온도센서": temperatures, "팬": fans}


def print_thermal_info(parsed: dict):
    """온도 및 팬 정보 출력"""
    print("\n" + "=" * 50)
    print("  온도 센서")
    print("=" * 50)
    for t in parsed.get("온도센서", []):
        print(f"  [{t['센서명']}]  {t['현재온도(C)']}C"
              f"  (경고: {t['상한경고(C)']}C"
              f" | 위험: {t['상한위험(C)']}C)"
              f"  상태: {t['상태']}")

    print("\n" + "=" * 50)
    print("  팬 상태")
    print("=" * 50)
    for f in parsed.get("팬", []):
        print(f"  [{f['팬명']}]  {f['RPM']} {f['단위']}"
              f"  상태: {f['상태']}")
    print("=" * 50)
