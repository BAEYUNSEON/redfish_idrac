# config.py
# ─────────────────────────────────────────────
# iDRAC 연결 설정값을 이 파일에서 관리합니다.
# 실제 IP와 인증 정보로 교체하세요.
# ─────────────────────────────────────────────

IDRAC_CONFIG = {
    "ip": "192.168.1.100",          # ← 실제 iDRAC IP 주소로 변경
    "username": "root",              # ← iDRAC 사용자명
    "password": "calvin",           # ← iDRAC 패스워드
    "verify_ssl": False,            # 자체 서명 인증서 무시 (테스트용)
    "timeout": 30,                  # 요청 타임아웃 (초)
    "protocol": "https",            # iDRAC은 HTTPS 사용
}

# Redfish API 엔드포인트 목록 (확장 가능)
REDFISH_ENDPOINTS = {
    "root":         "/redfish/v1",
    "system":       "/redfish/v1/Systems/System.Embedded.1",
    "thermal":      "/redfish/v1/Chassis/System.Embedded.1/Thermal",
    "power":        "/redfish/v1/Chassis/System.Embedded.1/Power",
    "bios":         "/redfish/v1/Systems/System.Embedded.1/Bios",
    "idrac_attrs":  "/redfish/v1/Managers/iDRAC.Embedded.1/Attributes",
}

# JSON 저장 경로
OUTPUT_DIR = "./output"
