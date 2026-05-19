# utils/file_utils.py
# ─────────────────────────────────────────────
# JSON 파일 저장 및 로드 유틸리티
# VSCode에서 바로 열어볼 수 있도록 pretty-print 포맷으로 저장
# ─────────────────────────────────────────────

import json
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def save_json(data: dict, name: str,
              output_dir: str = "./output") -> str:
    """
    딕셔너리를 JSON 파일로 저장 (타임스탬프 포함)

    Args:
        data (dict): 저장할 데이터
        name (str): 파일 이름 prefix (예: "system", "thermal")
        output_dir (str): 저장 경로

    Returns:
        str: 저장된 파일 경로
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    logger.info(f"JSON 저장 완료: {filepath}")
    return filepath


def load_json(filepath: str) -> dict:
    """
    JSON 파일을 불러옵니다.

    Args:
        filepath (str): 불러올 JSON 파일 경로

    Returns:
        dict: 파싱된 JSON 딕셔너리
    """
    if not os.path.exists(filepath):
        logger.error(f"파일 없음: {filepath}")
        return {}

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    logger.info(f"JSON 로드 완료: {filepath}")
    return data


def save_raw_response(data: dict, name: str,
                      output_dir: str = "./output") -> str:
    """
    iDRAC 원본 응답 JSON을 그대로 저장 (파싱 전 raw 데이터)
    """
    return save_json(data, f"raw_{name}", output_dir)
