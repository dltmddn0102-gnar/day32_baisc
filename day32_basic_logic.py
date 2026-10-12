RULE_VERSION = 'shipping-v1'  # 배송비 계산 규칙 버전


# 배송비 계산 함수
def calculate_shipping_fee(weight):
    # 무게는 1~20000g 사이의 정수여야 함
    if isinstance(weight, bool) or not isinstance(weight, int):
        raise ValueError('무게는 정수로 입력하세요.')

    if weight < 1 or weight > 20000:
        raise ValueError('무게를 1~20000g 사이로 입력하세요.')

    # 1000g 이하 3000원, 초과하면 시작된 1000g 구간마다 1000원 추가
    fee = 3000 + ((weight - 1) // 1000) * 1000

    return fee
