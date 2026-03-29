#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import math
import time

# --- 1. 39개 전문화 8차원 좌표 데이터베이스 (DB) ---
# Res(책임), Sup(지원), Dist(거리), Log(논리), Agg(공격), Nat(자연), Ord(질서), Shd(이면)
SPECS_DB = {
    "보호 성기사": {"Res": 10, "Sup": 5, "Dist": -5, "Log": 5, "Agg": 3, "Nat": 0, "Ord": 10, "Shd": 0},
    "복원 주술사": {"Res": 3, "Sup": 10, "Dist": 8, "Log": 5, "Agg": 0, "Nat": 10, "Ord": 3, "Shd": 0},
    "수양 사제": {"Res": 5, "Sup": 8, "Dist": 5, "Log": 10, "Agg": 0, "Nat": 0, "Ord": 8, "Shd": 5},
    "분노 전사": {"Res": 2, "Sup": 0, "Dist": -10, "Log": 0, "Agg": 10, "Nat": 3, "Ord": 0, "Shd": 5},
    "비전 마법사": {"Res": 0, "Sup": 0, "Dist": 10, "Log": 10, "Agg": 5, "Nat": 0, "Ord": 8, "Shd": 3},
    "혈기 죽음의 기사": {"Res": 10, "Sup": 0, "Dist": -5, "Log": 3, "Agg": 7, "Nat": 0, "Ord": 3, "Shd": 10},
    "조화 드루이드": {"Res": 0, "Sup": 5, "Dist": 10, "Log": 8, "Agg": 3, "Nat": 10, "Ord": 5, "Shd": 0},
    "양조 수도사": {"Res": 8, "Sup": 5, "Dist": -3, "Log": 7, "Agg": 4, "Nat": 8, "Ord": 5, "Shd": 2},
    "파괴 흑마법사": {"Res": 2, "Sup": 0, "Dist": 10, "Log": 8, "Agg": 9, "Nat": 0, "Ord": 4, "Shd": 8},
    # [공간 제약상 주요 9개만 기입, 실제 배포 시 39개 전체 좌표를 이 형식으로 확장 가능합니다]
}

# --- 2. 20개 정밀 질문지 (가중치 벡터 설계) ---
QUESTIONS = [
    {
        "q": "Q1. 팀의 프로젝트가 위기에 처했을 때, 당신이 가장 먼저 취하는 행동은?",
        "options": [
            {"t": "내가 모든 책임을 지고 전면에 나서서 상황을 수습한다.", "w": {"Res": 10, "Ord": 5}},
            {"t": "팀원들의 정서적 안정을 돕고 협력을 이끌어낸다.", "w": {"Sup": 10, "Nat": 5}},
            {"t": "문제의 핵심을 파악하기 위해 현장에 즉각 투입된다.", "w": {"Agg": 10, "Dist": -10}},
            {"t": "데이터를 분석하여 실패 원인과 대안을 논리적으로 정리한다.", "w": {"Log": 10, "Dist": 10}}
        ]
    },
    {
        "q": "Q2. 당신이 가장 선호하는 업무 환경의 분위기는 어떤가요?",
        "options": [
            {"t": "체계적이고 매뉴얼이 확실하며 질서 정연한 곳", "w": {"Ord": 10, "Log": 5}},
            {"t": "자유롭고 창의적이며 자연스러운 변화가 허용되는 곳", "w": {"Nat": 10, "Dist": 5}},
            {"t": "목표 지향적이고 경쟁적이며 빠른 결과가 중시되는 곳", "w": {"Agg": 10, "Res": 5}},
            {"t": "이면의 전략을 중시하고 독립적인 집중이 가능한 곳", "w": {"Shd": 10, "Dist": 10}}
        ]
    },
    {
        "q": "Q3. 복잡한 가구를 조립하다가 나사가 하나 남았습니다. 당신은?",
        "options": [
            {"t": "완벽을 위해 처음부터 다시 해체하고 재조립한다.", "w": {"Ord": 10, "Res": 8}},
            {"t": "일단 작동에 문제가 없다면 효율을 위해 그냥 사용한다.", "w": {"Agg": 8, "Log": 5}},
            {"t": "남은 나사의 위치를 통해 어느 단계의 누락인지 역추론한다.", "w": {"Log": 10, "Shd": 5}},
            {"t": "조립 경험이 많은 지인에게 연락해 조언을 구한다.", "w": {"Sup": 10, "Nat": 5}}
        ]
    }
    # [이후 Q20까지 동일한 구조로 질문을 확장하여 배치합니다]
]

# --- 3. 세션 상태 초기화 ---
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.u = {"Res": 0, "Sup": 0, "Dist": 0, "Log": 0, "Agg": 0, "Nat": 0, "Ord": 0, "Shd": 0}
    st.session_state.history = []
    st.session_state.finished = False

# --- 4. 핵심 분석 함수 ---
def get_rankings():
    user_vec = st.session_state.u
    rankings = []
    for name, target_vec in SPECS_DB.items():
        # 8차원 유클리드 거리 계산: d = sqrt(sum((u_i - t_i)^2))
        dist = math.sqrt(sum([(user_vec.get(k, 0) - target_vec.get(k, 0))**2 for k in user_vec.keys()]))
        rankings.append({"name": name, "dist": dist})
    rankings.sort(key=lambda x: x['dist'])
    return rankings

# --- 5. UI 구성 ---
st.set_page_config(page_title="아제로스 자아 분석기", layout="centered")
st.title("🛡️ 아제로스 영혼의 자아 분석")

if not st.session_state.finished:
    # 진행도 및 수렴 지표 표시
    rankings = get_rankings()
    margin = rankings[1]['dist'] - rankings[0]['dist']
    
    # 조기 종료 조건 (질문 5개 이상 & 1-2위 거리 차이가 10 이상)
    if (margin > 10.0 and st.session_state.step >= 5) or st.session_state.step >= len(QUESTIONS):
        st.session_state.finished = True
        st.rerun()

    # 질문 출력
    q_data = QUESTIONS[st.session_state.step]
    st.progress(st.session_state.step / len(QUESTIONS))
    st.subheader(f"{q_data['q']}")

    for i, opt in enumerate(q_data['options']):
        if st.button(f"{opt['t']}", key=f"opt_{i}", use_container_width=True):
            # 가중치 기록 및 상태 업데이트
            st.session_state.history.append(opt['w'])
            for k, v in opt['w'].items():
                st.session_state.u[k] += v
            st.session_state.step += 1
            st.rerun()

    # 제어 버튼
    st.divider()
    c1, c2, c3 = st.columns(3)
    if c1.button("⬅️ 이전 단계") and st.session_state.step > 0:
        last_w = st.session_state.history.pop()
        for k, v in last_w.items():
            st.session_state.u[k] -= v
        st.session_state.step -= 1
        st.rerun()
    if c2.button("🔄 처음부터"):
        for k in st.session_state.keys(): del st.session_state[k]
        st.rerun()
    if c3.button("🚪 종료"):
        st.stop()

# --- 6. 결과 리포트 ---
else:
    st.balloons()
    final_rank = get_rankings()
    top1 = final_rank[0]
    top2 = final_rank[1]

    st.success("✅ 당신의 성향이 특정 자아로 완전히 수렴되었습니다!")
    st.header(f"🏆 최종 메인 자아: {top1['name']}")
    st.write(f"💡 추천 대안: {top2['name']}")
    
    # 성향 차트 대용 텍스트 분석
    st.divider()
    st.subheader("📊 심층 성향 데이터")
    u = st.session_state.u
    if u['Log'] > u['Agg']:
        st.write("- 당신은 본능보다 **논리적 전략**이 앞서는 타입입니다.")
    else:
        st.write("- 당신은 계산보다 **직관적 실행력**이 앞서는 타입입니다.")
    
    if st.button("🔄 다시 테스트하기"):
        for k in st.session_state.keys(): del st.session_state[k]
        st.rerun()


# In[ ]:





# In[ ]:




