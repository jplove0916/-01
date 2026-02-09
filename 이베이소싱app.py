import streamlit as st
import pandas as pd

# 앱 타이틀 및 회장님 환영 메시지
st.set_page_config(page_title="Program 1 - 이베이 소싱", layout="wide")
st.title("💼 Program 1: 회장님 전용 소싱 관리자")

# 1. 사이드바 - 설정
st.sidebar.header("설정")
shipping_cost_per_kg = st.sidebar.number_input("kg당 배송비 ($)", value=10.0)

# 2. 메인 검색 섹션
keyword = st.text_input("분석할 이베이 키워드를 입력하세요", placeholder="예: Vintage Watch")

if keyword:
    st.subheader(f"🔍 '{keyword}' 분석 결과")
    
    # 샘플 데이터 (실제로는 이베이 API와 연동됩니다)
    data = [
        {"item": "Rolex Submariner", "price": 12000, "weight": 1.2, "source": 10000},
        {"item": "Casio F91W", "price": 15, "weight": 0.1, "source": 5},
        {"item": "Seiko SKX", "price": 300, "weight": 0.8, "source": 200},
    ]
    
    df = pd.DataFrame(data)

    # 3. 고수 셀러의 핵심 로직: 수익성 및 무게 필터 계산
    def analyze_item(row):
        fees = row['price'] * 0.15  # 이베이 수수료 약 15%
        profit = row['price'] - row['source'] - fees - (row['weight'] * shipping_cost_per_kg)
        
        # 회장님이 말씀하신 무게 로직 적용
        # 1 미만이면 빨간 점 유지, 1 이상이면 제거
        status = "🔴 무게 주의" if row['weight'] < 1 else "✅ 통과"
        
        return pd.Series([profit, status])

    df[['예상수익', '상태']] = df.apply(analyze_item, axis=1)

    # 4. 모바일용 카드 뷰 출력
    for index, row in df.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**상품명:** {row['item']}")
                st.write(f"💰 예상 수익: ${row['예상수익']:.2f}")
            with col2:
                st.write(f"상태: {row['상태']}")
            st.divider()

else:
    st.info("회장님, 위 검색창에 키워드를 입력하시면 Program 1이 분석을 시작합니다.")
