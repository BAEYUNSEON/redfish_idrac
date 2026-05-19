# idrac_client.py
# ─────────────────────────────────────────────
# iDRAC에 HTTP(S) 연결하여 JSON 응답을 파싱하는 클라이언트
# ─────────────────────────────────────────────

import requests
import json
import urllib3
import logging
from config import IDRAC_CONFIG, REDFISH_ENDPOINTS

# SSL 경고 억제 (자체 서명 인증서 사용 시)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


class IDRACClient:
    """
    iDRAC Redfish API 클라이언트 클래스
    - HTTP GET 요청으로 JSON 데이터를 가져옴
    - 응답 JSON 파싱 및 반환
    - 확장 가능한 엔드포인트 구조
    """

    def __init__(self, config: dict = None):
        self.config = config or IDRAC_CONFIG
        self.base_url = (
            f"{self.config['protocol']}://{self.config['ip']}"
        )
        self.auth = (
            self.config["username"],
            self.config["password"]
        )
        self.session = requests.Session()
        self.session.verify = self.config.get("verify_ssl", False)
        self.session.auth = self.auth
        self.timeout = self.config.get("timeout", 30)

    def get(self, endpoint: str) -> dict:
        """
        지정한 Redfish 엔드포인트에 GET 요청을 보내고 JSON 반환

        Args:
            endpoint (str): Redfish URI 경로
                            (예: /redfish/v1/Systems/...)

        Returns:
            dict: 파싱된 JSON 딕셔너리 / 실패 시 None
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"연결 중: {url}")

        try:
            response = self.session.get(url, timeout=self.timeout)

            # HTTP 상태 코드 확인
            if response.status_code == 200:
                logger.info(f"성공 (HTTP {response.status_code})")
                return response.json()

            elif response.status_code == 401:
                logger.error("인증 실패: 사용자명/패스워드를 확인하세요.")
            elif response.status_code == 403:
                logger.error("권한 없음: iDRAC 라이선스 또는 권한을 확인하세요.")
            elif response.status_code == 404:
                logger.error(f"엔드포인트 없음: {endpoint}")
            else:
                logger.error(f"HTTP 오류: {response.status_code}")

        except requests.exceptions.ConnectionError:
            logger.error(f"연결 실패: {self.base_url} 에 도달할 수 없습니다.")
        except requests.exceptions.Timeout:
            logger.error(f"타임아웃: {self.timeout}초 초과")
        except requests.exceptions.RequestException as e:
            logger.error(f"요청 오류: {e}")

        return None

    def get_named(self, name: str) -> dict:
        """
        config.py의 REDFISH_ENDPOINTS에 정의된 이름으로 데이터 가져오기

        Args:
            name (str): 엔드포인트 이름 (예: "system", "thermal")

        Returns:
            dict: 파싱된 JSON 딕셔너리
        """
        endpoint = REDFISH_ENDPOINTS.get(name)
        if not endpoint:
            logger.error(f"알 수 없는 엔드포인트: '{name}'")
            return None
        return self.get(endpoint)

    def close(self):
        """세션 닫기"""
        self.session.close()
        logger.info("세션 종료")
