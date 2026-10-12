import os
from pathlib import Path
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

# local 실행을 위한 .env 로딩
load_dotenv()

# sql 파일 경로
SQL_DIR = Path(__file__).resolve().parent / 'sql'

def execute (name, params=()):
    # 환경변수에서 데이터베이스URL 획득
    url = os.getenv('DATABASE_URL', '').strip()
    if not url:
        raise ValueError('DATABASE_URL 환경변수를 설정하세요.')
    # sql 파일의 문자열 획득
    sql = (SQL_DIR / name).read_text(encoding='utf-8')
    with psycopg.connect(
        url, # 접속 URL
        connect_timeout=15, # 접속까지 15초는 대기
        row_factory=dict_row # 행을 딕셔너리로
    ) as conn:
        # sql 실행 후 결과를 리스트로 반환
        return conn.execute(sql, params).fetchall()


# 배송비 견적 저장
def save_quote(label, weight, fee, rule_version):
    label = label.strip()

    if not label or len(label) > 80:
        raise ValueError('견적 제목은 1~80자로 입력하세요.')

    rows = execute('save.sql', (
        label,
        weight,
        fee,
        rule_version
    ))

    return rows[0]['id']


# 배송비 견적 목록
def list_quotes():
    return execute('list.sql')










