# day32_basic.py
# python -m streamlit run ./desktop/webservice/day32/day32_ex.py

import streamlit as st
import psycopg

from day32_basic_logic import calculate_shipping_fee, RULE_VERSION
from day32_basic_db import save_quote, list_quotes


# 페이지 설정
st.set_page_config(
    page_title="배송비 견적 기록",
    page_icon="📦",
    layout="centered"
)

st.title("배송비 견적 기록")
st.write("견적 제목과 무게를 입력하고 배송비를 계산하세요.")


# 견적 입력
with st.form("shipping_quote_form"):
    label = st.text_input(
        "견적 제목",
        max_chars=80,
        placeholder="견적 제목을 입력하세요."
    )

    weight = st.number_input(
        "무게 (g)",
        min_value=1,
        max_value=20000,
        value=1000,
        step=1
    )

    submitted = st.form_submit_button("계산하고 저장")


# 계산 및 저장
if submitted:
    label = label.strip()

    if not label:
        st.error("견적 제목을 1~80자로 입력하세요.")

    elif len(label) > 80:
        st.error("견적 제목은 1~80자로 입력하세요.")

    else:
        try:
            fee = calculate_shipping_fee(int(weight))

            quote_id = save_quote(
                label,
                int(weight),
                fee,
                RULE_VERSION
            )

            st.success("배송비 견적이 저장되었습니다.")
            st.metric("배송비", f"{fee:,}원")
            st.write(f"견적 ID: {quote_id}")
            st.write(f"견적 제목: {label}")
            st.write(f"무게: {int(weight):,}g")
            st.write(f"계산 규칙: {RULE_VERSION}")

        except ValueError as e:
            st.error(str(e))

        except psycopg.Error:
            st.error(
                "데이터베이스 연결 또는 저장에 실패했습니다. "
                "DATABASE_URL과 DB 상태를 확인하세요."
            )

        except OSError:
            st.error(
                "SQL 파일을 읽지 못했습니다. "
                "sql 폴더와 파일 이름을 확인하세요."
            )

        except RuntimeError as e:
            st.error(str(e))


# 최신 견적 목록
st.divider()
st.subheader("최근 배송비 견적")
st.caption("최신 견적 최대 100건")

try:
    quotes = list_quotes()

    if quotes:
        st.dataframe(
            quotes,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("저장된 견적이 없습니다.")

except ValueError as e:
    st.error(str(e))

except psycopg.Error:
    st.error(
        "견적 목록을 조회하지 못했습니다. "
        "DATABASE_URL을 확인하세요."
    )

except OSError:
    st.error("목록 SQL 파일을 읽지 못했습니다.")

