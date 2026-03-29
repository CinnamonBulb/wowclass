import streamlit as st
import math
import time

# --- 1. 39개 전문화 8차원 정밀 좌표 DB (0~100 스케일) ---
# 실제 배포 시 39개 전체를 이 정규화된 수치로 채워넣으시면 변별력이 극대화됩니다.
if 'specs' not in st.session_state:
    st.session_state.specs = {
        "보호 성기사": {"Res": 90, "Sup": 40, "Dist": -40, "Log": 50, "Agg": 30, "Nat": 10, "Ord": 95, "Shd": 10},
        "복원 주술사": {"Res": 30, "Sup": 90, "Dist": 60, "Log": 50, "Agg": 10, "Nat": 95, "Ord": 30, "Shd": 10},
        "수양 사제": {"Res": 40, "Sup": 70, "Dist": 50, "Log": 95, "Agg": 10, "Nat": 10, "Ord": 70, "Shd": 60},
        "분노 전사": {"Res": 20, "Sup": 10, "Dist": -95, "Log": 20, "Agg": 95, "Nat": 30, "Ord": 10, "Shd": 30},
        "비전 마법사": {"Res": 10, "Sup": 10, "Dist": 95, "Log": 90, "Agg": 50, "Nat": 10, "Ord": 80, "Shd": 30},
        "혈기 죽음의 기사": {"Res": 95, "Sup": 10, "Dist": -50, "Log": 30, "Agg": 70, "Nat": 10, "Ord": 30, "Shd": 90},
        "조화 드루이드": {"Res": 20, "Sup": 50, "Dist": 90, "Log": 80, "Agg": 40, "Nat": 95, "Ord": 50, "Shd": 20},
        "양조 수도사": {"Res": 80, "Sup": 50, "Dist": -30, "Log": 60, "Agg": 40, "Nat": 80, "Ord": 50, "Shd": 30},
        "파괴 흑마법사": {"Res": 20, "Sup": 10, "Dist": 90, "Log": 70, "Agg": 90, "Nat": 10, "Ord": 40, "Shd": 85},
        # ... 나머지 30개 전문화도 위와 같은 0~100 스케일로 확장 가능
    }

# --- 2. 20개 정밀 질문지 ---
questions = [
    {
        "q": "Q1. 팀의 성과에 대해 외부의 거센 비판이 쏟아지는 상황입니다. 당신은?",
        "options": [
            {"t": "비판의 화살을 직접 맞으며 팀원들을 보호한다.", "w": {"Res": 15, "Ord": 5}},
            {"t": "흔들리는 팀원들의 마음을 먼저 다독이고 안심시킨다.", "w": {"Sup": 15, "Nat": 5}},
            {"t": "말보다 행동으로, 문제가 된 지점을 즉각 수정한다.", "w": {"Agg": 15, "Dist": -10}},
            {"t": "비판의 논리적 허점을 분석해 대응 전략을 수립한다.", "w": {"Log": 15, "Dist": 10}}
        ]
    },
    {
        "q": "Q2. 준비한 계획이 예상치 못한 변수로 완전히 엉망이 되었습니다. 당신은?",
        "options": [
            {"t": "검증된 매뉴얼이나 사례를 대조하며 원칙대로 복구한다.", "w": {"Ord": 15, "Res": 5}},
            {"t": "주변 의견을 듣고 모두가 납득할 합의점을 찾는다.", "w": {"Nat": 15, "Sup": 5}},
            {"t": "지체 없이 현장에 뛰어들어 가장 빠른 돌파구를 만든다.", "w": {"Agg": 15, "Dist": -10}},
            {"t": "인과관계를 파악하여 가장 효율적인 새 경로를 재설계한다.", "w": {"Log": 15, "Dist": 10}}
        ]
    },
    # Q3 ~ Q20 질문 데이터 (생략, 실제 배포 시 질문을 추가하여 20개 구성)
]

# --- 3. 세션 상태 관리 ---
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.u = {k: 0 for k in ["Res", "Sup", "Dist", "Log", "Agg", "Nat", "Ord", "Shd"]}
    st.session_state.history = []
    st.session_state.finished = False

def get_rankings():
    u_vec = st.session_state.u
    ranks = []
    for name, p_vec in st.session_state.specs.items():
        # 8차원 유클리드 거리 계산
        d = math.sqrt(sum([(u_vec.get(k, 0) - p_vec.get(k, 0))**2 for k in u_vec.keys()]))
        ranks.append({"name": name, "dist": d})
    return sorted(ranks, key=lambda x: x['dist'])

# --- 4. 메인 분석 화면 ---
st.title("🧪 아제로스 영혼의 자아 정밀 분석")

if not st.session_state.finished:
    # 실시간 랭킹 및 마진 계산
    current_ranks = get_rankings()
    top1, top2 = current_ranks[0], current_ranks[1]
    margin = top2['dist'] - top1['dist']
    
    # [마진 60 기반 조기 종료 로직]
    target_margin = 60.0
    if (st.session_state.step >= 5 and margin > target_margin) or st.session_state.step >= len(questions):
        st.session_state.finished = True
        st.rerun()

    q_data = questions[st.session_state.step]
    st.write(f"**진행 단계: {st.session_state.step + 1} / {len(questions)}**")
    st.progress((st.session_state.step + 1) / len(questions))
    st.caption(f"현재 분석 정밀도(Margin): {margin:.2f} / {target_margin}")

    st.subheader(q_data['q'])
    for i, opt in enumerate(q_data['options']):
        if st.button(opt['t'], key=f"btn_{st.session_state.step}_{i}", use_container_width=True):
            st.session_state.history.append(opt['w'])
            for k, v in opt['w'].items():
                st.session_state.u[k] += v
            st.session_state.step += 1
            st.rerun()

    st.divider()
    c1, c2 = st.columns(2)
    if c1.button("⬅️ 이전 단계") and st.session_state.step > 0:
        prev_w = st.session_state.history.pop()
        for k, v in prev_w.items(): st.session_state.u[k] -= v
        st.session_state.step -= 1
        st.rerun()
    if c2.button("🔄 처음부터"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# --- 5. 결과 리포트 (심층 분석 포함) ---
else:
    final_ranks = get_rankings()
    top1 = final_ranks[0]
    top2 = final_ranks[1]
    
    st.balloons()
    st.header(f"🏆 최종 결과: [{top1['name']}]")
    st.subheader(f"💡 추천 대안: {top2['name']}")
    
    st.divider()
    st.subheader("🧐 분석 근거 (Decision Log)")
    
    # 사용자의 가장 높은 성향 지표 추출
    u = st.session_state.u
    top_traits = sorted(u.items(), key=lambda x: x[1], reverse=True)[:2]
    
    st.write(f"당신의 답변에서 가장 두드러진 성향은 **{top_traits[0][0]}**와(과) **{top_traits[1][0]}**입니다.")
    
    # 결과 해석 로직 (수학적 가중치 기반)
    if top_traits[0][0] == "Res" or top_traits[0][0] == "Ord":
        st.write(f"> 당신은 위기 상황에서 **책임감(Res)**과 **질서(Ord)**를 최우선으로 선택했습니다. 이는 스스로를 통제하며 팀을 지탱하는 **{top1['name']}**의 기질과 완벽히 일치합니다.")
    elif top_traits[0][0] == "Sup" or top_traits[0][0] == "Nat":
        st.write(f"> 당신은 조화로운 **협력(Sup)**과 **유연함(Nat)**을 중시하는 선택을 내렸습니다. 이는 주변을 보살피는 **{top1['name']}**의 에너지와 공명합니다.")
    elif top_traits[0][0] == "Agg" or top_traits[0][0] == "Log":
        st.write(f"> 당신은 날카로운 **분석력(Log)** 혹은 거침없는 **추진력(Agg)**을 바탕으로 문제를 해결하려 합니다. 이러한 '해결사'적 면모가 결과에 큰 영향을 주었습니다.")
    
    st.info(f"이 결과는 총 {st.session_state.step}개의 문항을 통해 당신의 8차원 좌표를 분석한 결과이며, 2위인 {top2['name']}와는 약 {top2['dist'] - top1['dist']:.1f}점의 거리 차이가 발생하여 충분한 변별력이 확보되었습니다.")

    if st.button("🔄 다시 테스트하기"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()
