# parsers/power_parser.py
# ─────────────────────────────────────────────
# iDRAC 전원 공급 장치(PSU) 정보 파서
# ─────────────────────────────────────────────


def parse_power_info(data: dict) -> dict:
    """
    /redfish/v1/Chassis/System.Embedded.1/Power 응답 파서
    """
    if not data:
        return {}

    power_supplies = []
    for psu in data.get("PowerSupplies", []):
        power_supplies.append({
            "PSU명":        psu.get("Name", "N/A"),
            "제조사":       psu.get("Manufacturer", "N/A"),
            "모델":         psu.get("Model", "N/A"),
            "정격출력(W)":  psu.get("PowerCapacityWatts", "N/A"),
            "현재출력(W)":  psu.get("LastPowerOutputWatts", "N/A"),
            "상태":         psu.get("Status", {}).get("Health", "N/A"),
        })

    # 전체 전력 소비
    power_control = data.get("PowerControl", [{}])
    # custom ys 
    if power_control {
        data = power_control.get("data")
        print(data) 
    }
    current_power = (
        power_control[0].get("PowerConsumedWatts", "N/A")
        if power_control else "N/A"
    )

    return {
        "현재소비전력(W)": current_power,
        "전원공급장치": power_supplies,
    }


def print_power_info(parsed: dict):
    """전원 정보 출력"""
    print("\n" + "=" * 50)
    print(f"  전원 정보  (현재 소비: "
          f"{parsed.get('현재소비전력(W)', 'N/A')} W)")
    print("=" * 50)
    for psu in parsed.get("전원공급장치", []):
        print(f"  [{psu['PSU명']}]  {psu['모델']}"
              f"  정격: {psu['정격출력(W)']}W"
              f"  상태: {psu['상태']}")
    print("=" * 50)
