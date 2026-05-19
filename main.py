# main.py
# ─────────────────────────────────────────────
# iDRAC JSON 파서 미니 프로젝트 - 메인 실행 파일
# 사용법: python main.py
# ─────────────────────────────────────────────

import argparse
import sys
import json
from idrac_client import IDRACClient
from parsers.system_parser import parse_system_info, print_system_info
from parsers.thermal_parser import parse_thermal_info, print_thermal_info
from parsers.power_parser import parse_power_info, print_power_info
from utils.file_utils import save_json, save_raw_response, load_json
from config import OUTPUT_DIR


def run_all(client: IDRACClient, save: bool = True):
    """모든 엔드포인트 데이터를 가져와 파싱하고 출력"""

    results = {}

    # ── 1. 시스템 정보 ────────────────────────
    raw_system = client.get_named("system")
    if raw_system:
        if save:
            save_raw_response(raw_system, "system", OUTPUT_DIR)
        parsed_system = parse_system_info(raw_system)
        print_system_info(parsed_system)
        results["system"] = parsed_system

    # ── 2. 온도/팬 정보 ───────────────────────
    raw_thermal = client.get_named("thermal")
    if raw_thermal:
        if save:
            save_raw_response(raw_thermal, "thermal", OUTPUT_DIR)
        parsed_thermal = parse_thermal_info(raw_thermal)
        print_thermal_info(parsed_thermal)
        results["thermal"] = parsed_thermal

    # ── 3. 전원 정보 ──────────────────────────
    raw_power = client.get_named("power")
    if raw_power:
        if save:
            save_raw_response(raw_power, "power", OUTPUT_DIR)
        parsed_power = parse_power_info(raw_power)
        print_power_info(parsed_power)
        results["power"] = parsed_power

    # ── 결과 통합 저장 ────────────────────────
    if save and results:
        saved_path = save_json(results, "all_parsed", OUTPUT_DIR)
        print(f"\n전체 파싱 결과 저장됨: {saved_path}")
    return results


def run_single(client: IDRACClient,
               endpoint_name: str, save: bool = True):
    """특정 엔드포인트 하나만 실행"""
    raw_data = client.get_named(endpoint_name)
    if raw_data:
        if save:
            save_raw_response(raw_data, endpoint_name, OUTPUT_DIR)
        print(f"\n [{endpoint_name}] 원본 JSON:")
        print(json.dumps(raw_data, indent=4, ensure_ascii=False))


def load_and_view(filepath: str):
    """저장된 JSON 파일 불러와서 출력"""
    data = load_json(filepath)
    if data:
        print(json.dumps(data, indent=4, ensure_ascii=False))


# ── 명령행 인자 파서 ─────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(
        description="iDRAC Redfish API JSON 파서 미니 프로젝트"
    )
    parser.add_argument(
        "--mode",
        choices=["all", "system", "thermal",
                 "power", "bios", "load"],
        default="all",
        help="실행 모드 선택 (기본값: all)"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="JSON 파일 저장 안 함"
    )
    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="로드할 JSON 파일 경로 (--mode load 사용 시)"
    )
    return parser.parse_args()


# ── 메인 진입점 ──────────────────────────────
if __name__ == "__main__":
    args = parse_args()
    save = not args.no_save

    print("=" * 60)
    print("  iDRAC Redfish JSON 파서  |  Mini Project")
    print("=" * 60)

    # 로드 모드: 저장된 파일만 읽기 (iDRAC 연결 불필요)
    if args.mode == "load":
        if not args.file:
            print("--file 옵션으로 JSON 파일 경로를 지정하세요.")
            sys.exit(1)
        load_and_view(args.file)
        sys.exit(0)

    # iDRAC 클라이언트 생성
    client = IDRACClient()

    try:
        if args.mode == "all":
            run_all(client, save=save)
        else:
            run_single(client, args.mode, save=save)
    finally:
        client.close()
