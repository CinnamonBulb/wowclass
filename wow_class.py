import streamlit as st
import math
import json

# ============================================================
# 1. 39개 전문화 8차원 좌표 DB
# 8가지 축:
#   Res  = 책임감/방어 (내가 맞으며 버팀)         0~100
#   Sup  = 지원/보조 (타인을 살리고 돕는 것)       0~100
#   Dist = 거리감/원거리 선호 (양수=원거리, 음수=근접) -100~100
#   Log  = 분석/전략 (계획적·체계적)               0~100
#   Agg  = 공격성/추진력 (돌파, 직접 해결)          0~100
#   Nat  = 자연친화/직관 (흐름에 맡김, 유연)        0~100
#   Ord  = 질서/규율 (원칙, 안정, 통제)             0~100
#   Shd  = 어둠/희생 (금기, 대가를 치름)            0~100
# ============================================================
SPECS = {
    # ── 전사 ──────────────────────────────────────────────
    "분노 전사":        {"Res":20,"Sup":5, "Dist":-90,"Log":20,"Agg":95,"Nat":25,"Ord":15,"Shd":30},
    "무기 전사":        {"Res":35,"Sup":5, "Dist":-70,"Log":45,"Agg":80,"Nat":20,"Ord":50,"Shd":20},
    "방어 전사":        {"Res":95,"Sup":30,"Dist":-80,"Log":55,"Agg":40,"Nat":10,"Ord":90,"Shd":10},
    # ── 성기사 ────────────────────────────────────────────
    "신성 성기사":      {"Res":60,"Sup":90,"Dist":-20,"Log":60,"Agg":20,"Nat":10,"Ord":90,"Shd":5},
    "보호 성기사":      {"Res":92,"Sup":40,"Dist":-40,"Log":55,"Agg":30,"Nat":10,"Ord":95,"Shd":10},
    "응징 성기사":      {"Res":40,"Sup":10,"Dist":-50,"Log":50,"Agg":75,"Nat":10,"Ord":75,"Shd":40},
    # ── 사냥꾼 ────────────────────────────────────────────
    "야수 사냥꾼":      {"Res":20,"Sup":15,"Dist":80, "Log":30,"Agg":70,"Nat":90,"Ord":20,"Shd":10},
    "사격 사냥꾼":      {"Res":15,"Sup":10,"Dist":95, "Log":75,"Agg":55,"Nat":40,"Ord":65,"Shd":10},
    "생존 사냥꾼":      {"Res":30,"Sup":15,"Dist":-30,"Log":60,"Agg":65,"Nat":75,"Ord":35,"Shd":25},
    # ── 도적 ──────────────────────────────────────────────
    "암살 도적":        {"Res":20,"Sup":5, "Dist":-40,"Log":80,"Agg":65,"Nat":30,"Ord":45,"Shd":80},
    "무법 도적":        {"Res":25,"Sup":5, "Dist":-50,"Log":35,"Agg":85,"Nat":50,"Ord":15,"Shd":50},
    "교활 도적":        {"Res":15,"Sup":5, "Dist":-20,"Log":90,"Agg":45,"Nat":20,"Ord":55,"Shd":65},
    # ── 사제 ──────────────────────────────────────────────
    "수양 사제":        {"Res":40,"Sup":75,"Dist":40, "Log":90,"Agg":10,"Nat":15,"Ord":75,"Shd":55},
    "신성 사제":        {"Res":35,"Sup":95,"Dist":30, "Log":65,"Agg":5, "Nat":20,"Ord":70,"Shd":5},
    "암흑 사제":        {"Res":25,"Sup":15,"Dist":60, "Log":70,"Agg":55,"Nat":10,"Ord":30,"Shd":90},
    # ── 죽음의 기사 ───────────────────────────────────────
    "혈기 죽음의 기사": {"Res":95,"Sup":10,"Dist":-50,"Log":35,"Agg":70,"Nat":10,"Ord":30,"Shd":90},
    "냉기 죽음의 기사": {"Res":45,"Sup":10,"Dist":-60,"Log":60,"Agg":70,"Nat":5, "Ord":50,"Shd":70},
    "부정 죽음의 기사": {"Res":30,"Sup":10,"Dist":-30,"Log":50,"Agg":80,"Nat":5, "Ord":25,"Shd":95},
    # ── 주술사 ────────────────────────────────────────────
    "원소 주술사":      {"Res":20,"Sup":25,"Dist":85, "Log":65,"Agg":55,"Nat":85,"Ord":35,"Shd":20},
    "고양 주술사":      {"Res":20,"Sup":50,"Dist":-35,"Log":50,"Agg":70,"Nat":90,"Ord":25,"Shd":15},
    "복원 주술사":      {"Res":30,"Sup":92,"Dist":55, "Log":50,"Agg":10,"Nat":95,"Ord":30,"Shd":10},
    # ── 마법사 ────────────────────────────────────────────
    "비전 마법사":      {"Res":10,"Sup":10,"Dist":90, "Log":92,"Agg":50,"Nat":10,"Ord":80,"Shd":30},
    "화염 마법사":      {"Res":10,"Sup":10,"Dist":80, "Log":60,"Agg":85,"Nat":20,"Ord":35,"Shd":25},
    "냉기 마법사":      {"Res":20,"Sup":10,"Dist":85, "Log":80,"Agg":35,"Nat":25,"Ord":75,"Shd":20},
    # ── 흑마법사 ──────────────────────────────────────────
    "고통 흑마법사":    {"Res":20,"Sup":10,"Dist":85, "Log":75,"Agg":50,"Nat":10,"Ord":45,"Shd":90},
    "악마술사 흑마법사":{"Res":15,"Sup":15,"Dist":80, "Log":60,"Agg":65,"Nat":10,"Ord":30,"Shd":85},
    "파괴 흑마법사":    {"Res":20,"Sup":10,"Dist":90, "Log":70,"Agg":90,"Nat":10,"Ord":40,"Shd":80},
    # ── 수도사 ────────────────────────────────────────────
    "양조 수도사":      {"Res":82,"Sup":45,"Dist":-30,"Log":65,"Agg":40,"Nat":80,"Ord":50,"Shd":30},
    "운무 수도사":      {"Res":30,"Sup":88,"Dist":-10,"Log":55,"Agg":15,"Nat":90,"Ord":40,"Shd":20},
    "풍운 수도사":      {"Res":25,"Sup":15,"Dist":-40,"Log":55,"Agg":75,"Nat":85,"Ord":35,"Shd":15},
    # ── 드루이드 ──────────────────────────────────────────
    "조화 드루이드":    {"Res":20,"Sup":50,"Dist":90, "Log":80,"Agg":40,"Nat":95,"Ord":50,"Shd":20},
    "야성 드루이드":    {"Res":30,"Sup":10,"Dist":-80,"Log":45,"Agg":80,"Nat":85,"Ord":25,"Shd":30},
    "수호 드루이드":    {"Res":90,"Sup":35,"Dist":-70,"Log":50,"Agg":35,"Nat":80,"Ord":55,"Shd":15},
    "회복 드루이드":    {"Res":25,"Sup":90,"Dist":40, "Log":55,"Agg":10,"Nat":95,"Ord":35,"Shd":10},
    # ── 악마사냥꾼 ────────────────────────────────────────
    "파멸 악마사냥꾼":  {"Res":25,"Sup":10,"Dist":-20,"Log":45,"Agg":88,"Nat":30,"Ord":20,"Shd":75},
    "복수 악마사냥꾼":  {"Res":88,"Sup":15,"Dist":-35,"Log":40,"Agg":55,"Nat":25,"Ord":30,"Shd":70},
    # ── 기원사 ────────────────────────────────────────────
    "황폐 기원사":      {"Res":20,"Sup":10,"Dist":75, "Log":70,"Agg":75,"Nat":40,"Ord":45,"Shd":55},
    "보존 기원사":      {"Res":35,"Sup":85,"Dist":65, "Log":70,"Agg":15,"Nat":55,"Ord":55,"Shd":40},
    "증강 기원사":      {"Res":30,"Sup":60,"Dist":50, "Log":75,"Agg":50,"Nat":50,"Ord":60,"Shd":45},
}

DIMS = ["Res","Sup","Dist","Log","Agg","Nat","Ord","Shd"]
DIM_LABELS = {
    "Res": "책임감/방어",
    "Sup": "지원/보조",
    "Dist": "원거리선호",
    "Log": "분석/전략",
    "Agg": "추진력/공격성",
    "Nat": "자연친화/직관",
    "Ord": "질서/규율",
    "Shd": "어둠/희생",
}

# ============================================================
# 2. 20개 질문지
# ============================================================
QUESTIONS = [
    {
        "q": "Q1. 팀원이 연속으로 쓰러지는 긴급 상황, 당신의 첫 번째 본능은?",
        "options": [
            {"t": "내가 직접 앞으로 나서서 적의 시선을 모두 내게 끌어온다.",
             "w": {"Res": 14, "Ord": 6},
             "reason": "책임감·방어(Res)와 질서(Ord)를 중시하는 탱커 성향을 강하게 반영합니다."},
            {"t": "쓰러진 동료를 빠르게 부활시키고 생존을 지원한다.",
             "w": {"Sup": 14, "Nat": 6},
             "reason": "지원·보조(Sup)와 자연친화(Nat) 성향 — 힐러 기질과 직결됩니다."},
            {"t": "적을 빠르게 제압해 상황 자체를 끝내버린다.",
             "w": {"Agg": 14, "Dist": -8},
             "reason": "근접 추진력(Agg)이 높아질수록 근접 딜러에 가까워집니다."},
            {"t": "상황을 파악하고 가장 효율적인 공격 순서를 계산한다.",
             "w": {"Log": 14, "Dist": 8},
             "reason": "분석·전략(Log)과 원거리 선호(Dist)는 원거리 딜러 혹은 전략적 플레이어 성향입니다."},
        ]
    },
    {
        "q": "Q2. 당신이 가장 즐기는 전투 포지션은?",
        "options": [
            {"t": "적 한가운데에서 휘두르며 싸운다. 살갗이 맞닿는 전투가 진짜다.",
             "w": {"Agg": 10, "Dist": -15},
             "reason": "근접 선호(Dist 음수)와 공격성(Agg)이 높아집니다."},
            {"t": "안전한 거리에서 정밀하게 공격한다. 제어가 핵심이다.",
             "w": {"Log": 8, "Dist": 15},
             "reason": "원거리(Dist 양수)와 전략성(Log)이 올라갑니다."},
            {"t": "아군 곁에 머물며 보호막과 회복을 유지한다.",
             "w": {"Sup": 12, "Res": 6},
             "reason": "지원(Sup)과 책임감(Res)을 동시에 강화합니다."},
            {"t": "전장을 넓게 보며 위기 지점에 즉각 개입한다.",
             "w": {"Ord": 10, "Log": 8},
             "reason": "질서(Ord)와 분석(Log)은 전술적 유연성을 나타냅니다."},
        ]
    },
    {
        "q": "Q3. 당신의 힘의 원천에 가장 가까운 것은?",
        "options": [
            {"t": "대지와 자연의 흐름 — 내 안의 원시적인 본능",
             "w": {"Nat": 15, "Log": -5},
             "reason": "자연친화(Nat)가 강하게 올라갑니다. 드루이드·주술사·수도사 계열에 가깝습니다."},
            {"t": "빛과 신성한 의지 — 흔들리지 않는 믿음",
             "w": {"Ord": 12, "Res": 6},
             "reason": "질서(Ord)와 책임감(Res)이 오릅니다. 성기사·사제 계열에 어울립니다."},
            {"t": "순수한 마법 에너지나 원소의 힘",
             "w": {"Log": 12, "Dist": 10},
             "reason": "분석(Log)과 원거리(Dist)가 증가합니다. 마법사·흑마·주술사 성향입니다."},
            {"t": "어둠, 금기, 혹은 아무도 건드리지 않는 경계의 힘",
             "w": {"Shd": 15, "Agg": 5},
             "reason": "어둠/희생(Shd)이 대폭 증가합니다. 암흑 계열·흑마법사·죽음의 기사에 수렴합니다."},
        ]
    },
    {
        "q": "Q4. 장기 레이드에서 당신이 가장 스트레스받는 상황은?",
        "options": [
            {"t": "내가 지켜야 할 동료가 죽었을 때",
             "w": {"Res": 12, "Sup": 6},
             "reason": "책임감(Res)이 오릅니다. 탱커나 힐러 기질과 연결됩니다."},
            {"t": "계획이 완전히 무너지고 혼돈 상태가 됐을 때",
             "w": {"Ord": 14, "Log": 6},
             "reason": "질서(Ord)와 분석(Log) 성향 — 구조적 플레이를 선호하는 타입입니다."},
            {"t": "내 딜이 낮아서 팀에 기여를 못하고 있을 때",
             "w": {"Agg": 12, "Log": 6},
             "reason": "추진력(Agg)과 분석(Log)이 동시에 오릅니다. 딜러 지향 성향입니다."},
            {"t": "아군들이 각자 따로 놀며 협력이 안 될 때",
             "w": {"Nat": 10, "Sup": 8},
             "reason": "자연친화(Nat)와 지원(Sup)이 강조됩니다. 팀 조화를 중시하는 타입입니다."},
        ]
    },
    {
        "q": "Q5. 당신이 게임 외적으로 가장 즐기는 역할은?",
        "options": [
            {"t": "문제 해결사 — 막힌 상황에서 해법을 찾아낸다.",
             "w": {"Log": 14, "Agg": 4},
             "reason": "분석·전략(Log)과 추진력(Agg)이 강조됩니다."},
            {"t": "조율자 — 팀원들 의견을 모아 방향을 잡는다.",
             "w": {"Nat": 10, "Ord": 8},
             "reason": "자연친화(Nat)와 질서(Ord)가 높아집니다."},
            {"t": "선봉장 — 위험해도 제일 먼저 뛰어든다.",
             "w": {"Agg": 12, "Res": 6},
             "reason": "추진력(Agg)과 책임감(Res)이 높아집니다."},
            {"t": "서포터 — 모두가 잘 되게 뒤에서 지원한다.",
             "w": {"Sup": 14, "Ord": 4},
             "reason": "지원(Sup)과 질서(Ord)가 강조됩니다."},
        ]
    },
    {
        "q": "Q6. 전투 후 당신이 느끼는 가장 큰 만족감은?",
        "options": [
            {"t": "단 한 명의 사망자도 없이 모두가 살아 돌아왔다.",
             "w": {"Sup": 12, "Res": 8},
             "reason": "지원(Sup)과 책임감(Res)이 동시에 강조됩니다."},
            {"t": "내가 최고 딜을 뽑아내며 결정적 기여를 했다.",
             "w": {"Agg": 12, "Log": 6},
             "reason": "추진력(Agg)과 전략(Log) 성향이 강해집니다."},
            {"t": "완벽한 로테이션으로 상황을 예측하고 통제했다.",
             "w": {"Ord": 12, "Log": 8},
             "reason": "질서(Ord)와 분석(Log)이 높아집니다."},
            {"t": "팀 전체가 내 덕분에 시너지를 발휘했다.",
             "w": {"Nat": 10, "Sup": 8},
             "reason": "자연친화(Nat)와 지원(Sup)이 강조됩니다."},
        ]
    },
    {
        "q": "Q7. 새로운 클래스를 배울 때 당신의 접근 방식은?",
        "options": [
            {"t": "시뮬레이션·스탯 계산기를 먼저 돌려본다. 수치가 전부다.",
             "w": {"Log": 14, "Ord": 6},
             "reason": "분석(Log)과 질서(Ord)가 강해집니다. 마법사·도적 교활 성향."},
            {"t": "일단 던전에 뛰어들어 몸으로 익힌다.",
             "w": {"Agg": 12, "Nat": 6},
             "reason": "추진력(Agg)과 자연친화(Nat)가 오릅니다."},
            {"t": "가이드보다는 느낌을 따라가며 스킬 흐름을 파악한다.",
             "w": {"Nat": 14, "Log": -4},
             "reason": "자연친화(Nat)가 대폭 증가합니다. 드루이드·운무 수도사 성향."},
            {"t": "공략 영상과 스킬 트리를 꼼꼼하게 분석한다.",
             "w": {"Ord": 12, "Log": 8},
             "reason": "질서(Ord)와 분석(Log)이 함께 오릅니다."},
        ]
    },
    {
        "q": "Q8. 당신이 자신에게 하는 말 중 가장 공감 가는 것은?",
        "options": [
            {"t": "\"내가 죽지 않으면 진다는 법은 없다.\"",
             "w": {"Res": 14, "Ord": 6},
             "reason": "책임감(Res)과 질서(Ord)가 강조됩니다."},
            {"t": "\"주변이 살아야 나도 의미가 있다.\"",
             "w": {"Sup": 14, "Nat": 6},
             "reason": "지원(Sup)과 자연친화(Nat) — 힐러 정체성의 핵심입니다."},
            {"t": "\"빠른 것이 옳다. 머뭇거리면 기회를 잃는다.\"",
             "w": {"Agg": 14, "Dist": -6},
             "reason": "추진력(Agg)과 근접 성향(Dist 음수)이 오릅니다."},
            {"t": "\"목표를 알면 어떤 수단도 정당화된다.\"",
             "w": {"Shd": 10, "Log": 8},
             "reason": "어둠/희생(Shd)과 분석(Log)이 높아집니다."},
        ]
    },
    {
        "q": "Q9. 어떤 전투 리듬이 가장 편한가요?",
        "options": [
            {"t": "짧고 강렬하게, 한 방에 끝내는 버스트 스타일",
             "w": {"Agg": 12, "Log": 6},
             "reason": "추진력(Agg)과 분석(Log)이 강조됩니다."},
            {"t": "도트와 지속 피해로 차분하게 쌓아가는 스타일",
             "w": {"Log": 10, "Dist": 10},
             "reason": "원거리 선호(Dist)와 분석(Log)이 올라갑니다. 암살 도적·고통 흑마 성향."},
            {"t": "방어막·도발을 유지하며 쫄쫄하게 버티는 스타일",
             "w": {"Res": 14, "Ord": 6},
             "reason": "책임감(Res)과 질서(Ord)가 오릅니다. 탱커 전반에 수렴합니다."},
            {"t": "핵심 순간에만 강력한 힐을 넣는 타이밍 스타일",
             "w": {"Sup": 10, "Log": 8},
             "reason": "지원(Sup)과 분석(Log)이 강조됩니다. 수양 사제·보존 기원사 성향."},
        ]
    },
    {
        "q": "Q10. 당신의 이상적인 무기 또는 전투 도구는?",
        "options": [
            {"t": "거대한 방패 또는 두꺼운 갑옷 — 버텨야 이긴다.",
             "w": {"Res": 14, "Ord": 6},
             "reason": "책임감(Res)과 질서(Ord)가 오릅니다."},
            {"t": "마법서나 지팡이 — 마법으로 모든 것을 해결한다.",
             "w": {"Log": 10, "Dist": 12},
             "reason": "원거리(Dist)와 분석(Log)이 강조됩니다."},
            {"t": "쌍검 또는 대검 — 빠르고 치명적이어야 한다.",
             "w": {"Agg": 12, "Dist": -8},
             "reason": "근접(Dist 음수)과 추진력(Agg)이 높아집니다."},
            {"t": "활 또는 총 — 거리 두고 정밀하게 노려야 한다.",
             "w": {"Dist": 14, "Log": 8},
             "reason": "원거리(Dist)가 크게 오릅니다. 사냥꾼·마법사 계열과 잘 맞습니다."},
        ]
    },
    {
        "q": "Q11. 팀이 와이프(전멸)됐을 때 당신의 반응은?",
        "options": [
            {"t": "\"내 실수야. 내가 더 잘 버텼어야 했어.\"",
             "w": {"Res": 14, "Shd": 4},
             "reason": "책임감(Res)이 강하게 오릅니다. 탱커 마인드."},
            {"t": "\"힐이 부족했네. 다음엔 타이밍을 다르게 가겠어.\"",
             "w": {"Sup": 10, "Log": 8},
             "reason": "지원(Sup)과 분석(Log)이 강화됩니다."},
            {"t": "\"좀 더 빠르게 눌렀으면 됐는데. 스킬 쿨 조절 실패.\"",
             "w": {"Agg": 8, "Log": 10},
             "reason": "추진력(Agg)과 분석(Log)이 오릅니다. 딜러 기질."},
            {"t": "\"팀 전체가 위치 선정을 잘못했어. 다시 전략 짜자.\"",
             "w": {"Ord": 12, "Log": 8},
             "reason": "질서(Ord)와 분석(Log)이 강조됩니다."},
        ]
    },
    {
        "q": "Q12. 어떤 환경에서 싸울 때 가장 강해지나요?",
        "options": [
            {"t": "숲, 황야, 자연 속 — 주변과 하나가 되는 느낌",
             "w": {"Nat": 14, "Log": -4},
             "reason": "자연친화(Nat)가 대폭 증가합니다."},
            {"t": "성채, 신전 — 빛이 가득한 신성한 공간",
             "w": {"Ord": 12, "Res": 6},
             "reason": "질서(Ord)와 책임감(Res)이 오릅니다."},
            {"t": "어둠, 지하 던전 — 아무것도 보이지 않는 곳",
             "w": {"Shd": 14, "Log": 4},
             "reason": "어둠/희생(Shd)이 크게 높아집니다."},
            {"t": "도시, 전장 — 혼돈 속에서도 냉철하게 움직인다.",
             "w": {"Log": 12, "Agg": 6},
             "reason": "분석(Log)과 추진력(Agg)이 강조됩니다."},
        ]
    },
    {
        "q": "Q13. 당신이 선호하는 파티원 스타일은?",
        "options": [
            {"t": "내가 다 막을 테니 마음껏 때려. 믿어줘.",
             "w": {"Res": 12, "Ord": 6},
             "reason": "책임감(Res)과 질서(Ord)가 높아집니다."},
            {"t": "다 같이 호흡 맞춰서 깔끔하게 클리어하면 돼.",
             "w": {"Nat": 10, "Sup": 8},
             "reason": "자연친화(Nat)와 지원(Sup)이 강화됩니다."},
            {"t": "각자 역할만 제대로 하면 클리어는 따라온다.",
             "w": {"Log": 12, "Ord": 6},
             "reason": "분석(Log)과 질서(Ord)가 오릅니다."},
            {"t": "딜 높은 사람이 제일 빠른 결과를 만든다.",
             "w": {"Agg": 14, "Dist": -4},
             "reason": "추진력(Agg)이 강하게 오릅니다."},
        ]
    },
    {
        "q": "Q14. 어떤 직업적 상상 속 자아가 더 끌리나요?",
        "options": [
            {"t": "전장의 기둥 — 모두가 무너져도 나만은 서있는",
             "w": {"Res": 14, "Shd": 4},
             "reason": "책임감(Res)이 매우 강하게 증가합니다."},
            {"t": "마지막 치유자 — 절망 속에서 생명의 불을 살리는",
             "w": {"Sup": 14, "Nat": 4},
             "reason": "지원(Sup)과 자연친화(Nat)가 강조됩니다."},
            {"t": "어둠의 칼날 — 금기를 넘어 목표를 제거하는",
             "w": {"Shd": 12, "Agg": 6},
             "reason": "어둠/희생(Shd)과 추진력(Agg)이 오릅니다."},
            {"t": "지식의 화신 — 마법과 이론으로 세계를 해석하는",
             "w": {"Log": 14, "Dist": 6},
             "reason": "분석(Log)과 원거리(Dist)가 강해집니다."},
        ]
    },
    {
        "q": "Q15. 당신의 가장 두드러진 성격 특성은?",
        "options": [
            {"t": "책임감이 강하다. 맡은 것은 반드시 끝낸다.",
             "w": {"Res": 12, "Ord": 8},
             "reason": "책임감(Res)과 질서(Ord) 모두 강화됩니다."},
            {"t": "감수성이 풍부하다. 상대의 상태를 먼저 느낀다.",
             "w": {"Sup": 12, "Nat": 8},
             "reason": "지원(Sup)과 자연친화(Nat)가 오릅니다."},
            {"t": "추진력이 강하다. 막히면 일단 밀어붙인다.",
             "w": {"Agg": 14, "Ord": -4},
             "reason": "추진력(Agg)이 크게 오르고 질서는 약간 줄어듭니다."},
            {"t": "분석적이다. 결정 전에 충분히 계산한다.",
             "w": {"Log": 14, "Agg": -4},
             "reason": "분석(Log)이 강해지고 추진력은 약간 줄어듭니다."},
        ]
    },
    {
        "q": "Q16. 적이 당신에게 다가올 때 반응은?",
        "options": [
            {"t": "더 가까이 와. 나는 여기서 절대 밀리지 않는다.",
             "w": {"Res": 12, "Dist": -10},
             "reason": "책임감(Res)과 근접 선호(Dist 음수)가 오릅니다."},
            {"t": "거리를 유지하며 안정적인 위치를 먼저 잡는다.",
             "w": {"Dist": 14, "Ord": 6},
             "reason": "원거리(Dist)와 질서(Ord)가 강조됩니다."},
            {"t": "내가 먼저 뛰어들어 선빵을 날린다.",
             "w": {"Agg": 14, "Dist": -6},
             "reason": "추진력(Agg)과 근접(Dist 음수)이 오릅니다."},
            {"t": "패턴을 읽고 허점을 기다린다.",
             "w": {"Log": 14, "Nat": 4},
             "reason": "분석(Log)과 자연친화(Nat)가 높아집니다."},
        ]
    },
    {
        "q": "Q17. 당신에게 '강하다'는 의미는?",
        "options": [
            {"t": "어떤 타격도 버텨낼 수 있는 것",
             "w": {"Res": 14, "Ord": 4},
             "reason": "책임감(Res)이 강조됩니다."},
            {"t": "힘이 아니라 팀이 살아남게 하는 것",
             "w": {"Sup": 12, "Nat": 6},
             "reason": "지원(Sup)과 자연친화(Nat)가 오릅니다."},
            {"t": "적을 가장 빠르게 제압하는 것",
             "w": {"Agg": 14, "Dist": -4},
             "reason": "추진력(Agg)이 강하게 오릅니다."},
            {"t": "대가를 치르더라도 결과를 만드는 것",
             "w": {"Shd": 12, "Agg": 6},
             "reason": "어둠/희생(Shd)과 추진력(Agg)이 높아집니다."},
        ]
    },
    {
        "q": "Q18. 캐릭터의 외관을 선택할 때 가장 중요한 요소는?",
        "options": [
            {"t": "두껍고 빛나는 갑옷 — 위압감과 신뢰감",
             "w": {"Res": 10, "Ord": 10},
             "reason": "책임감(Res)과 질서(Ord)가 강조됩니다."},
            {"t": "자연을 연상케 하는 색감과 유기적인 형태",
             "w": {"Nat": 14, "Shd": -4},
             "reason": "자연친화(Nat)가 크게 오릅니다."},
            {"t": "어둡고 날카롭고 위험해 보이는 디자인",
             "w": {"Shd": 14, "Agg": 4},
             "reason": "어둠/희생(Shd)이 크게 높아집니다."},
            {"t": "빛, 마법 이펙트, 신비로운 룩",
             "w": {"Log": 8, "Dist": 10},
             "reason": "분석(Log)과 원거리(Dist)가 오릅니다."},
        ]
    },
    {
        "q": "Q19. 가장 이상적인 '한 방'의 느낌은?",
        "options": [
            {"t": "도발 — 내게 달려오는 적들, 공포에 떠는 그 눈빛",
             "w": {"Res": 12, "Agg": 6},
             "reason": "책임감(Res)과 추진력(Agg)이 오릅니다."},
            {"t": "기적 같은 힐 — 1% HP에서 살려냈을 때의 짜릿함",
             "w": {"Sup": 14, "Log": 4},
             "reason": "지원(Sup)이 크게 강조됩니다."},
            {"t": "크리티컬 — 숫자가 터질 때의 쾌감",
             "w": {"Agg": 14, "Dist": -4},
             "reason": "추진력(Agg)이 강하게 오릅니다."},
            {"t": "완벽한 CC — 보스를 멈추고 전장을 통제했을 때",
             "w": {"Ord": 12, "Log": 8},
             "reason": "질서(Ord)와 분석(Log)이 강조됩니다."},
        ]
    },
    {
        "q": "Q20. 마지막으로 — 당신이 게임에서 진정 바라는 것은?",
        "options": [
            {"t": "내가 없으면 안 되는 존재가 되는 것",
             "w": {"Res": 10, "Sup": 8},
             "reason": "책임감(Res)과 지원(Sup) 모두 높아집니다."},
            {"t": "최고 효율로 콘텐츠를 클리어하는 것",
             "w": {"Log": 12, "Ord": 8},
             "reason": "분석(Log)과 질서(Ord)가 강조됩니다."},
            {"t": "스트레스 없이 즐겁게 플레이하는 것",
             "w": {"Nat": 14, "Agg": -4},
             "reason": "자연친화(Nat)가 크게 오릅니다."},
            {"t": "내가 선택한 어둠의 길을 끝까지 걷는 것",
             "w": {"Shd": 14, "Nat": -4},
             "reason": "어둠/희생(Shd)이 크게 강조됩니다."},
        ]
    },
]

# 결과 설명 텍스트
SPEC_DESC = {
    "분노 전사": "본능과 광기로 전장을 지배합니다. 생각보다 몸이 먼저 움직이는 당신, 피가 끓는 곳에 답이 있습니다.",
    "무기 전사": "정밀한 무기 운용과 전술적 판단이 조화를 이룹니다. 격투가보다는 검술가에 가깝습니다.",
    "방어 전사": "흔들리지 않는 바위. 팀의 전방을 홀로 떠받드는 냉철한 수호자입니다.",
    "신성 성기사": "빛을 통해 동료를 살립니다. 전투의 흐름을 유지하며 희망을 나눠주는 존재입니다.",
    "보호 성기사": "신념과 강철로 방어선을 만드는 절대 탱커. 질서와 책임의 화신입니다.",
    "응징 성기사": "정의의 이름으로 적을 심판합니다. 빛의 힘을 공격에 담아내는 솔로잉의 왕.",
    "야수 사냥꾼": "자연과 한 몸인 사냥꾼. 동물과의 유대가 전투력의 원천입니다.",
    "사격 사냥꾼": "적이 닿기 전에 끝냅니다. 거리와 정밀함이 최고의 무기입니다.",
    "생존 사냥꾼": "罠과 폭발물로 근접전을 이끄는 이색 사냥꾼. 야생의 지략으로 싸웁니다.",
    "암살 도적": "독과 그림자로 표적을 제거하는 냉혹한 암살자. 계획 없는 행동은 없습니다.",
    "무법 도적": "해적 기질의 전투사. 예측 불가능한 화력과 짜릿한 행운이 무기입니다.",
    "교활 도적": "모든 것을 꿰뚫는 전략가. 적의 허점을 찾아 침투하는 고수입니다.",
    "수양 사제": "내면의 빛과 어둠을 동시에 다루는 균형의 힐러. 사려깊고 강인합니다.",
    "신성 사제": "순수한 빛으로 치유합니다. 팀의 안녕이 곧 나의 기쁨인 헌신적 힐러입니다.",
    "암흑 사제": "어둠의 속삭임을 무기로 삼는 딜러. 정신을 파고드는 심연의 전사입니다.",
    "혈기 죽음의 기사": "적의 생명을 빨아 자신의 것으로 만드는 죽음의 탱커. 어둠 속 불사의 존재.",
    "냉기 죽음의 기사": "냉기로 적을 저지하고 파괴하는 죽음의 기사. 냉철한 이성과 서릿발이 공존합니다.",
    "부정 죽음의 기사": "역병과 부패로 전장을 오염시킵니다. 가장 공격적인 죽음의 기사 전문화.",
    "원소 주술사": "대지·불·폭풍을 아우르는 원소의 목소리. 자연과 마법의 경계에 섭니다.",
    "고양 주술사": "영혼의 힘으로 팀원을 강화하는 독특한 서포터 딜러. 협력이 화력입니다.",
    "복원 주술사": "대지의 숨결로 치유합니다. 여러 명을 동시에 살리는 광역 힐의 전문가.",
    "비전 마법사": "마법의 본질을 탐구하는 지식인. 완벽한 로테이션에서 오는 쾌감을 압니다.",
    "화염 마법사": "불꽃으로 전장을 태웁니다. 화끈한 폭발감이 매력인 마법사입니다.",
    "냉기 마법사": "얼음으로 적을 통제하고 파괴합니다. 냉정한 판단으로 기회를 만듭니다.",
    "고통 흑마법사": "저주와 도트로 적을 서서히 무너뜨립니다. 인내와 계산이 미덕.",
    "악마술사 흑마법사": "악마를 소환해 전장을 가득 채웁니다. 세력을 키워 지배하는 타입.",
    "파괴 흑마법사": "혼돈의 불꽃을 마음껏 터뜨립니다. 어둠 속 화력 딜러의 극한입니다.",
    "양조 수도사": "술을 마시며 싸우는 독특한 탱커. 자연의 흐름처럼 유연하게 피해를 흘려냅니다.",
    "운무 수도사": "흐르는 안개처럼 치유합니다. 움직임과 힐이 하나가 되는 역동적 힐러.",
    "풍운 수도사": "권각의 달인. 빠르고 리드미컬한 근접전에서 최고의 쾌감을 느낍니다.",
    "조화 드루이드": "별빛과 달빛으로 원거리 공격을 펼칩니다. 자연의 섭리를 이해하는 학자형 딜러.",
    "야성 드루이드": "맹수가 되어 싸웁니다. 본능과 속도가 지배하는 근접 딜러.",
    "수호 드루이드": "곰 형태로 팀을 지킵니다. 자연의 견고함이 방어선이 되는 탱커.",
    "회복 드루이드": "성장하는 생명의 힘으로 치유합니다. 지속 힐의 여왕, 자연과 하나.",
    "파멸 악마사냥꾼": "어둠의 힘을 받아들여 적을 베어냅니다. 화려하고 파괴적인 근접 딜러.",
    "복수 악마사냥꾼": "악마의 힘을 흡수하며 적의 공격을 역이용합니다. 독특한 리소스 탱커.",
    "황폐 기원사": "용의 마법으로 전장을 휩씁니다. 원소 화력과 도트를 결합한 원거리 딜러.",
    "보존 기원사": "시간을 다루며 동료를 되살립니다. 독특한 메커니즘의 힐러.",
    "증강 기원사": "아군을 강화하는 독보적 서포터. 팀 전체의 성능을 올리는 특이한 딜러.",
}

# ============================================================
# 3. 유틸 함수
# ============================================================
def euclidean(u, p):
    return math.sqrt(sum((u.get(k, 0) - p.get(k, 0)) ** 2 for k in DIMS))

def get_rankings(u_vec):
    results = [{"name": name, "dist": euclidean(u_vec, p)} for name, p in SPECS.items()]
    return sorted(results, key=lambda x: x["dist"])

def radar_svg(u_vec, top_spec_vec):
    """8차원 레이더 차트를 SVG로 반환 (사용자 vs 추천 전문화)"""
    import math as m
    cx, cy, r = 200, 200, 140
    n = len(DIMS)
    labels = [DIM_LABELS[d] for d in DIMS]

    def point(val, idx, scale=100):
        angle = m.pi / 2 - 2 * m.pi * idx / n
        # Dist는 -100~100이므로 정규화
        norm = (val + 100) / 200 if DIMS[idx] == "Dist" else val / 100
        norm = max(0, min(1, norm))
        rx = cx + r * norm * m.cos(angle)
        ry = cy - r * norm * m.sin(angle)
        return rx, ry

    # 배경 그리드
    grid_lines = ""
    for level in [0.25, 0.5, 0.75, 1.0]:
        pts = " ".join(f"{cx + r*level*m.cos(m.pi/2 - 2*m.pi*i/n):.1f},{cy - r*level*m.sin(m.pi/2 - 2*m.pi*i/n):.1f}" for i in range(n))
        grid_lines += f'<polygon points="{pts}" fill="none" stroke="#334155" stroke-width="1"/>\n'

    # 축 선
    axis_lines = ""
    for i in range(n):
        angle = m.pi / 2 - 2 * m.pi * i / n
        x2 = cx + r * m.cos(angle)
        y2 = cy - r * m.sin(angle)
        axis_lines += f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#475569" stroke-width="1"/>\n'

    # 추천 전문화 폴리곤
    spec_pts = " ".join(f"{point(top_spec_vec.get(d, 0), i)[0]:.1f},{point(top_spec_vec.get(d, 0), i)[1]:.1f}" for i, d in enumerate(DIMS))
    spec_poly = f'<polygon points="{spec_pts}" fill="rgba(251,191,36,0.15)" stroke="#f59e0b" stroke-width="2"/>\n'

    # 사용자 폴리곤
    u_pts = " ".join(f"{point(u_vec.get(d, 0), i)[0]:.1f},{point(u_vec.get(d, 0), i)[1]:.1f}" for i, d in enumerate(DIMS))

    # 사용자 Dist를 표시용으로 변환 (음수면 근접)
    u_display = dict(u_vec)

    u_poly = f'<polygon points="{u_pts}" fill="rgba(99,102,241,0.2)" stroke="#6366f1" stroke-width="2.5"/>\n'

    # 레이블
    label_text = ""
    for i, label in enumerate(labels):
        angle = m.pi / 2 - 2 * m.pi * i / n
        lx = cx + (r + 22) * m.cos(angle)
        ly = cy - (r + 22) * m.sin(angle)
        anchor = "middle"
        if lx < cx - 10:
            anchor = "end"
        elif lx > cx + 10:
            anchor = "start"
        label_text += f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" fill="#94a3b8" font-size="11" font-family="sans-serif">{label}</text>\n'

    svg = f"""<svg viewBox="0 0 400 420" xmlns="http://www.w3.org/2000/svg" style="background:#0f172a;border-radius:12px;">
  {grid_lines}
  {axis_lines}
  {spec_poly}
  {u_poly}
  {label_text}
  <!-- 범례 -->
  <rect x="60" y="380" width="12" height="12" fill="#6366f1" rx="2"/>
  <text x="78" y="391" fill="#94a3b8" font-size="11" font-family="sans-serif">나의 성향</text>
  <rect x="180" y="380" width="12" height="12" fill="#f59e0b" rx="2"/>
  <text x="198" y="391" fill="#94a3b8" font-size="11" font-family="sans-serif">추천 전문화</text>
</svg>"""
    return svg

# ============================================================
# 4. 세션 상태 초기화
# ============================================================
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.u = {k: 0 for k in DIMS}
    st.session_state.history = []  # [(weights_dict, option_idx), ...]
    st.session_state.finished = False
    st.session_state.last_reason = ""

# ============================================================
# 5. 페이지 설정 & 스타일
# ============================================================
st.set_page_config(page_title="아제로스 영혼 정밀 분석", page_icon="⚔️", layout="centered")

st.markdown("""
<style>
    .main { background-color: #0f172a; }
    .stButton > button {
        background-color: #1e293b;
        color: #e2e8f0;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        transition: all 0.2s;
        text-align: left;
        white-space: normal;
        height: auto;
    }
    .stButton > button:hover {
        background-color: #6366f1;
        border-color: #6366f1;
        color: white;
    }
    .result-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .reason-box {
        background-color: #1e293b;
        border-left: 3px solid #6366f1;
        border-radius: 4px;
        padding: 0.6rem 1rem;
        color: #94a3b8;
        font-size: 0.88rem;
        margin-top: 0.4rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 6. 퀴즈 화면
# ============================================================
if not st.session_state.finished:

    current_ranks = get_rankings(st.session_state.u)
    margin = current_ranks[1]["dist"] - current_ranks[0]["dist"] if len(current_ranks) > 1 else 0

    # 조기 종료: 5문항 이상 & 마진 80 초과
    TARGET_MARGIN = 80.0
    if (st.session_state.step >= 5 and margin > TARGET_MARGIN) or st.session_state.step >= len(QUESTIONS):
        st.session_state.finished = True
        st.rerun()

    q_data = QUESTIONS[st.session_state.step]

    st.title("⚔️ 아제로스 영혼 정밀 분석")
    st.caption("당신의 선택이 39개 전문화 중 당신에게 맞는 하나를 찾아냅니다.")
    st.divider()

    prog = (st.session_state.step) / len(QUESTIONS)
    st.progress(prog, text=f"진행: {st.session_state.step} / {len(QUESTIONS)}문항")

    st.subheader(q_data["q"])
    st.write("")

    for i, opt in enumerate(q_data["options"]):
        if st.button(opt["t"], key=f"q{st.session_state.step}_o{i}", use_container_width=True):
            st.session_state.history.append((opt["w"], i))
            for k, v in opt["w"].items():
                st.session_state.u[k] = st.session_state.u.get(k, 0) + v
            st.session_state.last_reason = opt["reason"]
            st.session_state.step += 1
            st.rerun()

    # 방금 선택한 이유 표시
    if st.session_state.last_reason:
        st.markdown(f'<div class="reason-box">💡 이전 선택의 분석 근거: {st.session_state.last_reason}</div>', unsafe_allow_html=True)

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ 이전으로", use_container_width=True) and st.session_state.step > 0:
            prev_w, _ = st.session_state.history.pop()
            for k, v in prev_w.items():
                st.session_state.u[k] -= v
            st.session_state.step -= 1
            st.session_state.last_reason = ""
            st.rerun()
    with col2:
        if st.button("🔄 처음부터", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

# ============================================================
# 7. 결과 화면
# ============================================================
else:
    final_ranks = get_rankings(st.session_state.u)
    top1 = final_ranks[0]
    top2 = final_ranks[1]
    top1_vec = SPECS[top1["name"]]
    top2_vec = SPECS[top2["name"]]
    u = st.session_state.u

    st.balloons()
    st.title("⚔️ 당신의 아제로스 영혼 분석 결과")
    st.divider()

    # 1위
    st.markdown(f"## 🏆 추천 전문화: **{top1['name']}**")
    st.markdown(f'<div class="result-card">{SPEC_DESC.get(top1["name"], "")}</div>', unsafe_allow_html=True)

    # 레이더 차트
    st.subheader("📊 나의 성향 vs 추천 전문화 비교")
    svg_code = radar_svg(u, top1_vec)
    st.markdown(svg_code, unsafe_allow_html=True)

    # 2위
    st.markdown(f"### 🥈 대안 추천: **{top2['name']}**")
    st.markdown(f'<div class="result-card">{SPEC_DESC.get(top2["name"], "")}</div>', unsafe_allow_html=True)
    diff = top2["dist"] - top1["dist"]
    st.caption(f"1위와 2위의 점수 차이: {diff:.1f}점 — {'거의 근소한 차이' if diff < 20 else '명확한 차이'}입니다.")

    # 내 성향 분석
    st.divider()
    st.subheader("🧐 내 성향 요약")
    top_traits = sorted(
        [(DIM_LABELS[k], v) for k, v in u.items()],
        key=lambda x: x[1], reverse=True
    )[:3]
    for label, val in top_traits:
        st.write(f"- **{label}** 성향이 강합니다.")

    # 전체 순위 (접기)
    with st.expander("📋 전체 전문화 순위 보기"):
        for i, r in enumerate(final_ranks):
            bar = "█" * max(1, int(20 - r["dist"] / 15))
            st.write(f"{i+1:2d}위  **{r['name']}**  (거리: {r['dist']:.1f})")

    st.divider()
    if st.button("🔄 다시 테스트하기", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
