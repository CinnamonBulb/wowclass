import streamlit as st
import math

# ============================================================
# 1. 39개 전문화 12차원 좌표 DB (심리 8축 + 전투 4축)
# ============================================================
SPECS = {
    "분노 전사":          {"Res":20,"Sup":5, "Dist":-90,"Log":20,"Agg":95,"Nat":25,"Ord":15,"Shd":30, "Mob":70, "Cpx":40, "Des":95, "Pac":-90},
    "무기 전사":          {"Res":35,"Sup":5, "Dist":-70,"Log":45,"Agg":80,"Nat":20,"Ord":50,"Shd":20, "Mob":50, "Cpx":60, "Des":75, "Pac":-40},
    "방어 전사":          {"Res":95,"Sup":30,"Dist":-80,"Log":55,"Agg":40,"Nat":10,"Ord":90,"Shd":10, "Mob":60, "Cpx":55, "Des":40, "Pac":-50},
    "신성 성기사":        {"Res":60,"Sup":90,"Dist":-20,"Log":60,"Agg":20,"Nat":10,"Ord":90,"Shd":5,  "Mob":30, "Cpx":50, "Des":10, "Pac":20},
    "보호 성기사":        {"Res":92,"Sup":40,"Dist":-40,"Log":55,"Agg":30,"Nat":10,"Ord":95,"Shd":10, "Mob":30, "Cpx":50, "Des":20, "Pac":-10},
    "응징 성기사":        {"Res":40,"Sup":10,"Dist":-50,"Log":50,"Agg":75,"Nat":10,"Ord":75,"Shd":40, "Mob":40, "Cpx":45, "Des":60, "Pac":-20},
    "야수 사냥꾼":        {"Res":20,"Sup":15,"Dist":80, "Log":30,"Agg":70,"Nat":90,"Ord":20,"Shd":10, "Mob":80, "Cpx":20, "Des":40, "Pac":-80},
    "사격 사냥꾼":        {"Res":15,"Sup":10,"Dist":95, "Log":75,"Agg":55,"Nat":40,"Ord":65,"Shd":10, "Mob":50, "Cpx":40, "Des":65, "Pac":60},
    "생존 사냥꾼":        {"Res":30,"Sup":15,"Dist":-30,"Log":60,"Agg":65,"Nat":75,"Ord":35,"Shd":25, "Mob":70, "Cpx":70, "Des":50, "Pac":-30},
    "암살 도적":          {"Res":20,"Sup":5, "Dist":-40,"Log":80,"Agg":65,"Nat":30,"Ord":45,"Shd":80, "Mob":60, "Cpx":75, "Des":85, "Pac":-40},
    "무법 도적":          {"Res":25,"Sup":5, "Dist":-50,"Log":35,"Agg":85,"Nat":50,"Ord":15,"Shd":50, "Mob":80, "Cpx":80, "Des":60, "Pac":-80},
    "교활 도적":          {"Res":15,"Sup":5, "Dist":-20,"Log":90,"Agg":45,"Nat":20,"Ord":55,"Shd":65, "Mob":70, "Cpx":85, "Des":50, "Pac":-20},
    "수양 사제":          {"Res":40,"Sup":75,"Dist":40, "Log":90,"Agg":10,"Nat":15,"Ord":75,"Shd":55, "Mob":20, "Cpx":85, "Des":25, "Pac":40},
    "신성 사제":          {"Res":35,"Sup":95,"Dist":30, "Log":65,"Agg":5, "Nat":20,"Ord":70,"Shd":5,  "Mob":10, "Cpx":40, "Des":5,  "Pac":70},
    "암흑 사제":          {"Res":25,"Sup":15,"Dist":60, "Log":70,"Agg":55,"Nat":10,"Ord":30,"Shd":90, "Mob":20, "Cpx":80, "Des":75, "Pac":50},
    "혈기 죽음의 기사":   {"Res":95,"Sup":10,"Dist":-50,"Log":35,"Agg":70,"Nat":10,"Ord":30,"Shd":90, "Mob":10, "Cpx":60, "Des":50, "Pac":-10},
    "냉기 죽음의 기사":   {"Res":45,"Sup":10,"Dist":-60,"Log":60,"Agg":70,"Nat":5, "Ord":50,"Shd":70, "Mob":15, "Cpx":50, "Des":75, "Pac":-30},
    "부정 죽음의 기사":   {"Res":30,"Sup":10,"Dist":-30,"Log":50,"Agg":80,"Nat":5, "Ord":25,"Shd":95, "Mob":15, "Cpx":70, "Des":85, "Pac":-10},
    "원소 주술사":        {"Res":20,"Sup":25,"Dist":85, "Log":65,"Agg":55,"Nat":85,"Ord":35,"Shd":20, "Mob":30, "Cpx":60, "Des":65, "Pac":70},
    "고양 주술사":        {"Res":20,"Sup":50,"Dist":-35,"Log":50,"Agg":70,"Nat":90,"Ord":25,"Shd":15, "Mob":50, "Cpx":85, "Des":60, "Pac":-60},
    "복원 주술사":        {"Res":30,"Sup":92,"Dist":55, "Log":50,"Agg":10,"Nat":95,"Ord":30,"Shd":10, "Mob":40, "Cpx":55, "Des":10, "Pac":50},
    "비전 마법사":        {"Res":10,"Sup":10,"Dist":90, "Log":92,"Agg":50,"Nat":10,"Ord":80,"Shd":30, "Mob":40, "Cpx":75, "Des":70, "Pac":80},
    "화염 마법사":        {"Res":10,"Sup":10,"Dist":80, "Log":60,"Agg":85,"Nat":20,"Ord":35,"Shd":25, "Mob":60, "Cpx":65, "Des":90, "Pac":10},
    "냉기 마법사":        {"Res":20,"Sup":10,"Dist":85, "Log":80,"Agg":35,"Nat":25,"Ord":75,"Shd":20, "Mob":50, "Cpx":50, "Des":60, "Pac":60},
    "고통 흑마법사":      {"Res":20,"Sup":10,"Dist":85, "Log":75,"Agg":50,"Nat":10,"Ord":45,"Shd":90, "Mob":20, "Cpx":70, "Des":75, "Pac":30},
    "악마술사 흑마법사":  {"Res":15,"Sup":15,"Dist":80, "Log":60,"Agg":65,"Nat":10,"Ord":30,"Shd":85, "Mob":25, "Cpx":75, "Des":60, "Pac":50},
    "파괴 흑마법사":      {"Res":20,"Sup":10,"Dist":90, "Log":70,"Agg":90,"Nat":10,"Ord":40,"Shd":80, "Mob":15, "Cpx":35, "Des":95, "Pac":90},
    "양조 수도사":        {"Res":82,"Sup":45,"Dist":-30,"Log":65,"Agg":40,"Nat":80,"Ord":50,"Shd":30, "Mob":75, "Cpx":70, "Des":30, "Pac":-30},
    "운무 수도사":        {"Res":30,"Sup":88,"Dist":-10,"Log":55,"Agg":15,"Nat":90,"Ord":40,"Shd":20, "Mob":80, "Cpx":65, "Des":10, "Pac":10},
    "풍운 수도사":        {"Res":25,"Sup":15,"Dist":-40,"Log":55,"Agg":75,"Nat":85,"Ord":35,"Shd":15, "Mob":90, "Cpx":75, "Des":60, "Pac":-70},
    "조화 드루이드":      {"Res":20,"Sup":50,"Dist":90, "Log":80,"Agg":40,"Nat":95,"Ord":50,"Shd":20, "Mob":40, "Cpx":60, "Des":50, "Pac":75},
    "야성 드루이드":      {"Res":30,"Sup":10,"Dist":-80,"Log":45,"Agg":80,"Nat":85,"Ord":25,"Shd":30, "Mob":85, "Cpx":90, "Des":75, "Pac":-60},
    "수호 드루이드":      {"Res":90,"Sup":35,"Dist":-70,"Log":50,"Agg":35,"Nat":80,"Ord":55,"Shd":15, "Mob":50, "Cpx":40, "Des":30, "Pac":-20},
    "회복 드루이드":      {"Res":25,"Sup":90,"Dist":40, "Log":55,"Agg":10,"Nat":95,"Ord":35,"Shd":10, "Mob":65, "Cpx":60, "Des":5,  "Pac":30},
    "파멸 악마사냥꾼":    {"Res":25,"Sup":10,"Dist":-20,"Log":45,"Agg":88,"Nat":30,"Ord":20,"Shd":75, "Mob":95, "Cpx":30, "Des":85, "Pac":-85},
    "복수 악마사냥꾼":    {"Res":88,"Sup":15,"Dist":-35,"Log":40,"Agg":55,"Nat":25,"Ord":30,"Shd":70, "Mob":85, "Cpx":45, "Des":55, "Pac":-40},
    "황폐 기원사":        {"Res":20,"Sup":10,"Dist":75, "Log":70,"Agg":75,"Nat":40,"Ord":45,"Shd":55, "Mob":65, "Cpx":50, "Des":80, "Pac":40},
    "보존 기원사":        {"Res":35,"Sup":85,"Dist":65, "Log":70,"Agg":15,"Nat":55,"Ord":55,"Shd":40, "Mob":60, "Cpx":65, "Des":15, "Pac":30},
    "증강 기원사":        {"Res":30,"Sup":60,"Dist":50, "Log":75,"Agg":50,"Nat":50,"Ord":60,"Shd":45, "Mob":55, "Cpx":55, "Des":40, "Pac":20},
}

DIMS = ["Res","Sup","Dist","Log","Agg","Nat","Ord","Shd","Mob","Cpx","Des","Pac"]

DIM_LABELS = {
    "Res": "방어·책임", "Sup": "지원·배려", "Dist": "독립·거리", "Log": "분석·전략",
    "Agg": "돌격·추진", "Nat": "유연·직관", "Ord": "질서·규율", "Shd": "희생·어둠",
    "Mob": "민첩·기동", "Cpx": "정교·복잡", "Des": "폭발·파괴", "Pac": "호흡·느긋"
}

SPEC_DESC = {
    "분노 전사":          "본능과 광기로 전장을 지배합니다. 피가 끓는 곳에 답이 있습니다.",
    "무기 전사":          "정밀한 무기 운용과 전술적 판단. 격투가보다는 검술가에 가깝습니다.",
    "방어 전사":          "흔들리지 않는 바위. 팀의 전방을 홀로 떠받드는 냉철한 수호자입니다.",
    "신성 성기사":        "빛을 통해 동료를 살립니다. 전투의 흐름을 유지하며 희망을 나눕니다.",
    "보호 성기사":        "신념과 강철로 방어선을 만드는 절대 탱커. 질서와 책임의 화신입니다.",
    "응징 성기사":        "정의의 이름으로 적을 심판합니다. 빛의 힘을 공격에 담아냅니다.",
    "야수 사냥꾼":        "자연과 한 몸인 사냥꾼. 쉴 새 없는 움직임과 동물과의 유대가 무기입니다.",
    "사격 사냥꾼":        "적이 닿기 전에 끝냅니다. 완벽한 거리 유지와 치명적인 정밀함.",
    "생존 사냥꾼":        "함정과 폭발물로 근접전을 이끄는 이색 사냥꾼. 야생의 지략으로 싸웁니다.",
    "암살 도적":          "독과 출혈로 숨통을 끊어버리는 잔혹함. 오차 없는 암살자입니다.",
    "무법 도적":          "해적 기질의 전투사. 예측 불가능한 화력과 짜릿한 행운이 무기입니다.",
    "교활 도적":          "보이지 않는 곳에서 구조를 붕괴시키는 고수. 모든 것을 꿰뚫어 봅니다.",
    "수양 사제":          "빛과 어둠을 동시에 다루며, 공격을 통해 치유하는 사려깊은 힐러.",
    "신성 사제":          "순수한 빛으로 아군을 구원합니다. 팀의 안녕이 최우선인 헌신적 힐러.",
    "암흑 사제":          "어둠의 속삭임으로 정신을 파고드는 심연의 전사. 고도의 계산이 필요합니다.",
    "혈기 죽음의 기사":   "적의 생명을 빨아 자신을 회복하는 불사의 탱커. 묵직하고 잔혹합니다.",
    "냉기 죽음의 기사":   "냉기로 적을 파괴하는 죽음의 기사. 냉철한 이성과 서릿발이 공존합니다.",
    "부정 죽음의 기사":   "역병과 부패로 전장을 오염시킵니다. 수단과 방법을 가리지 않는 딜러.",
    "원소 주술사":        "대지, 불, 폭풍을 아우르는 원소의 목소리. 거대한 자연의 분노를 다룹니다.",
    "고양 주술사":        "자연의 힘을 무기에 담아 휘두르는 근접 전사. 화려한 연계가 일품입니다.",
    "복원 주술사":        "치유의 물결로 파티 전체를 살려내는 다재다능한 광역 힐의 대가.",
    "비전 마법사":        "마나의 흐름을 통제하는 지식인. 완벽한 로테이션에서 오는 쾌감을 압니다.",
    "화염 마법사":        "모든 것을 잿더미로 만드는 폭발적인 화력. 화끈한 타격감이 매력입니다.",
    "냉기 마법사":        "얼음으로 적의 발을 묶고 산산조각 냅니다. 침착하고 정교한 지배자.",
    "고통 흑마법사":      "저주와 도트로 적을 서서히 말려 죽입니다. 인내와 고문방식을 즐깁니다.",
    "악마술사 흑마법사":  "수많은 악마 군단을 소환해 전장을 압도하는 지배자.",
    "파괴 흑마법사":      "거대한 지옥 불덩이를 날리는 묵직한 마법사. 압도적 한 방의 쾌감.",
    "양조 수도사":        "술을 마시며 적의 공격을 부드럽게 흘려내는 유연하고 독특한 탱커.",
    "운무 수도사":        "전장을 기동하며 안개처럼 부드럽게 팀원을 치유하는 역동적 힐러.",
    "풍운 수도사":        "무술의 달인. 빠르고 리드미컬한 연계기로 적을 두들겨 팹니다.",
    "조화 드루이드":      "해와 달의 마법을 쏟아붓는 학자형 딜러. 기나긴 호흡으로 우주를 다룹니다.",
    "야성 드루이드":      "표범으로 변신해 적의 뒤를 노리는 날렵하고 극도로 정교한 사냥꾼.",
    "수호 드루이드":      "거대한 곰이 되어 파티를 지킵니다. 대자연의 우직함이 돋보이는 탱커.",
    "회복 드루이드":      "성장하는 생명의 힘으로 치유합니다. 자연과 하나된 지속 힐의 여왕.",
    "파멸 악마사냥꾼":    "어둠의 힘을 받아들여 전장을 휩쓰는 화려하고 파괴적인 근접 딜러.",
    "복수 악마사냥꾼":    "악마의 힘을 흡수하며 역으로 적을 베어내는 기동성 넘치는 탱커.",
    "황폐 기원사":        "용의 마법을 응축해 전장을 휩쓰는 중거리 딜러. 화려하고 유연합니다.",
    "보존 기원사":        "시간의 마법으로 동료의 상처를 되돌립니다. 독보적인 메커니즘의 힐러.",
    "증강 기원사":        "동료들의 잠재력을 극대화하는 독보적 서포터. 파티 전체를 조율합니다.",
}

# ============================================================
# 2. 직업 맵핑 및 교정 가중치 (Softmax Margins)
# 10,000회 시뮬레이션을 통해 13개 직업이 7.6%로 나오도록 수학적 조정 완료
# ============================================================
CLASS_MAPPING = {
    "전사": ["분노 전사", "무기 전사", "방어 전사"],
    "성기사": ["신성 성기사", "보호 성기사", "응징 성기사"],
    "사냥꾼": ["야수 사냥꾼", "사격 사냥꾼", "생존 사냥꾼"],
    "도적": ["암살 도적", "무법 도적", "교활 도적"],
    "사제": ["수양 사제", "신성 사제", "암흑 사제"],
    "죽음의 기사": ["혈기 죽음의 기사", "냉기 죽음의 기사", "부정 죽음의 기사"],
    "주술사": ["원소 주술사", "고양 주술사", "복원 주술사"],
    "마법사": ["비전 마법사", "화염 마법사", "냉기 마법사"],
    "흑마법사": ["고통 흑마법사", "악마술사 흑마법사", "파괴 흑마법사"],
    "수도사": ["양조 수도사", "운무 수도사", "풍운 수도사"],
    "드루이드": ["조화 드루이드", "야성 드루이드", "수호 드루이드", "회복 드루이드"],
    "악마사냥꾼": ["파멸 악마사냥꾼", "복수 악마사냥꾼"],
    "기원사": ["황폐 기원사", "보존 기원사", "증강 기원사"],
}

SPEC_TO_CLASS = {spec: cls for cls, specs in CLASS_MAPPING.items() for spec in specs}

# 13개 직업 강제 균등 분배를 위한 코사인 랭킹 가중치
CLASS_MARGINS = {
    '주술사': 0.0178, '드루이드': -0.0242, '흑마법사': 0.1271, '사제': -0.0484,
    '죽음의 기사': -0.1377, '수도사': 0.0446, '사냥꾼': -0.1474, '기원사': 0.1206,
    '성기사': -0.1789, '마법사': 0.1726, '악마사냥꾼': 0.0091, '도적': 0.0638, '전사': -0.0189
}

# ============================================================
# 3. 24개 문항 (다중 팩터 로딩, 오차율 0% 완전 대칭)
# ============================================================
QUESTIONS = [
    {"opts": [{"t": "화가 나지만 침묵을 지키며 화가 가라앉을 때까지 기다린다.", "w": {"Res":10, "Ord":6, "Pac":4}}, {"t": "내가 피해를 입더라도 분위기를 망치지 않게 조용히 넘긴다.", "w": {"Sup":10, "Shd":6, "Pac":4}}, {"t": "원인을 제공한 사람에게 가장 빠르고 치명적인 일침을 날린다.", "w": {"Agg":10, "Des":6, "Mob":4}}, {"t": "저 사람이 왜 저러는지 속으로 분석하며 논리적인 허점을 찾는다.", "w": {"Log":10, "Nat":6, "Cpx":4}}]},
    {"opts": [{"t": "결과를 빨리 내기 위해 다소 무리하더라도 공격적으로 추진한다.", "w": {"Agg":10, "Log":6, "Mob":4}}, {"t": "남들의 시선을 신경 쓰지 않고 내 직관에 따라 유연하게 움직인다.", "w": {"Nat":10, "Dist":6, "Pac":-4}}, {"t": "정해진 절차와 원칙을 준수하며 주변과 조율해 안정적으로 진행한다.", "w": {"Ord":10, "Sup":6, "Res":4}}, {"t": "모두가 꺼리는 일이라도 목표 달성을 위해 내가 독하게 떠맡는다.", "w": {"Shd":10, "Res":6, "Des":4}}]},
    {"opts": [{"t": "주어진 방어선이나 역할을 끝까지 사수하며 유연하게 대처한다.", "w": {"Res":10, "Nat":6, "Mob":4}}, {"t": "즉각적으로 앞으로 치고 나가며 적재적소에 도움을 뿌린다.", "w": {"Sup":10, "Agg":6, "Pac":-4}}, {"t": "멀리서 상황을 지켜보다가 가장 어둡고 은밀한 방식으로 개입한다.", "w": {"Dist":10, "Shd":6, "Pac":4}}, {"t": "구조를 완벽히 이해하고 가장 정교한 절차에 따라 문제를 해결한다.", "w": {"Log":10, "Ord":6, "Cpx":4}}]},
    {"opts": [{"t": "적의 방어를 뚫고 들어가 시원한 타격감으로 승부를 본다.", "w": {"Agg":10, "Des":6, "Mob":4}}, {"t": "순간적인 번뜩임으로 아무도 예상치 못한 플레이를 책임지고 해낸다.", "w": {"Nat":10, "Res":6, "Pac":-4}}, {"t": "짜인 빌드와 타이밍을 한 치의 오차도 없이 논리적으로 실행한다.", "w": {"Ord":10, "Log":6, "Cpx":4}}, {"t": "오로지 승리만을 위해 멀리서 피도 눈물도 없이 상대를 제압한다.", "w": {"Shd":10, "Dist":6, "Pac":4}}]},
    {"opts": [{"t": "모든 고통을 인내심 있게 받아내며 때를 기다린다.", "w": {"Res":10, "Shd":6, "Pac":4}}, {"t": "팀의 규율이 무너지지 않도록 모두를 독려하며 뛰어다닌다.", "w": {"Sup":10, "Ord":6, "Mob":4}}, {"t": "간섭받지 않는 곳에서 나만의 페이스로 자연스럽게 해답을 찾는다.", "w": {"Dist":10, "Nat":6, "Pac":4}}, {"t": "복잡하게 얽힌 문제를 가장 빠르고 공격적으로 쳐내버린다.", "w": {"Log":10, "Agg":6, "Cpx":4}}]},
    {"opts": [{"t": "거리를 두고 기회를 노리다가 한 방에 상황을 종결시킨다.", "w": {"Agg":10, "Dist":6, "Des":4}}, {"t": "여러 변수를 복합적으로 고려해 직관적이지만 정교한 해답을 낸다.", "w": {"Nat":10, "Log":6, "Cpx":4}}, {"t": "원칙을 지키며 흔들림 없이 한 걸음 한 걸음 우직하게 나아간다.", "w": {"Ord":10, "Res":6, "Pac":4}}, {"t": "필요하다면 손에 피를 묻히고 주변의 원망을 듣는 것도 감수한다.", "w": {"Shd":10, "Sup":6, "Des":4}}]},
    {"opts": [{"t": "위기 상황에서 책임을 지고 앞장서서 파괴적인 돌파구를 연다.", "w": {"Res":10, "Agg":6, "Des":4}}, {"t": "유연한 태도로 쉴 새 없이 움직이며 동료들의 부족함을 채운다.", "w": {"Sup":10, "Nat":6, "Mob":4}}, {"t": "복잡한 규칙의 세계에서 누구에게도 얽매이지 않고 홀로 존재한다.", "w": {"Dist":10, "Ord":6, "Cpx":4}}, {"t": "대계를 위해 무엇을 버려야 할지 논리적이고 차갑게 계산한다.", "w": {"Log":10, "Shd":6, "Pac":4}}]},
    {"opts": [{"t": "실패를 빠르게 털어내고 책임을 인정하며 다시 공격적으로 도전한다.", "w": {"Agg":10, "Res":6, "Mob":4}}, {"t": "느긋하게 마음을 추스르며 주변 사람들과 함께 직관적인 위로를 나눈다.", "w": {"Nat":10, "Sup":6, "Pac":4}}, {"t": "감정을 배제하고 거리두기를 통해 기존 매뉴얼의 복잡한 오류를 찾는다.", "w": {"Ord":10, "Dist":6, "Cpx":4}}, {"t": "목표 달성에 필요했던 희생과 논리적 인과관계를 다시 파고든다.", "w": {"Shd":10, "Log":6, "Des":4}}]},
    {"opts": [{"t": "정석적인 방법을 신중하게 숙달하며 단단한 기본기를 쌓는다.", "w": {"Res":10, "Ord":6, "Pac":4}}, {"t": "함께 배우는 사람들을 돕기 위해 내 속도를 기꺼이 포기한다.", "w": {"Sup":10, "Shd":6, "Mob":-4}}, {"t": "혼자만의 공간에서 거침없이 이것저것 시도하며 감을 잡는다.", "w": {"Dist":10, "Agg":6, "Mob":4}}, {"t": "원리를 파악하고 나만의 정교한 지름길을 만들어 효율을 극대화한다.", "w": {"Log":10, "Nat":6, "Cpx":4}}]},
    {"opts": [{"t": "어떤 파괴적인 압박 속에서도 논리적으로 결과를 만들어내는 에이스.", "w": {"Agg":10, "Log":6, "Des":4}}, {"t": "어디에도 얽매이지 않고 자유분방하게 맵을 누비는 해결사.", "w": {"Nat":10, "Dist":6, "Mob":4}}, {"t": "오랜 시간 공을 들여 조직의 규율과 화합을 다져내는 기둥.", "w": {"Ord":10, "Sup":6, "Pac":4}}, {"t": "보이지 않는 곳에서 가장 궂은일을 복잡하게 처리해 낸 장인.", "w": {"Shd":10, "Res":6, "Cpx":4}}]},
    {"opts": [{"t": "방해받지 않는 홀로만의 공간을 철벽처럼 유지한다.", "w": {"Res":10, "Dist":6, "Pac":4}}, {"t": "목표 달성을 위해 가장 공격적이고 규율 잡힌 폭발력을 준비한다.", "w": {"Agg":10, "Ord":6, "Des":4}}, {"t": "사람들이 편안해하도록 신중하고 논리적인 동선으로 배려한다.", "w": {"Sup":10, "Log":6, "Pac":4}}, {"t": "복잡하고 어두운 나만의 세계를 쉴 새 없이 직관적으로 꾸민다.", "w": {"Nat":10, "Shd":6, "Cpx":4}}]},
    {"opts": [{"t": "세상과 거리를 두지만 내가 맡은 역할의 묵직함은 끝까지 짊어진다.", "w": {"Dist":10, "Res":6, "Pac":4}}, {"t": "정해진 규칙 안에서 누구보다 빠르게 콤보를 넣듯 일을 처리한다.", "w": {"Ord":10, "Agg":6, "Mob":4}}, {"t": "복잡한 지식과 논리로 사람들에게 더 나은 방향을 제시한다.", "w": {"Log":10, "Sup":6, "Cpx":4}}, {"t": "직관과 본능에 따라 기존의 것을 파괴하는 것도 주저하지 않는다.", "w": {"Shd":10, "Nat":6, "Des":4}}]},
    {"opts": [{"t": "복잡한 계산과 묵직한 방어력으로 적의 시선을 완벽히 끈다.", "w": {"Res":10, "Log":6, "Cpx":4}}, {"t": "나의 희생을 담아 적을 완전히 찢어발기는 잔혹한 일격을 가한다.", "w": {"Agg":10, "Shd":6, "Des":4}}, {"t": "멀리서 호흡을 고르며 아군의 체력과 버프를 세심하게 챙긴다.", "w": {"Sup":10, "Dist":6, "Pac":4}}, {"t": "대자연의 질서에 맞춰 쉴 새 없이 움직이며 마법의 흐름을 통제한다.", "w": {"Nat":10, "Ord":6, "Mob":4}}]},
    {"opts": [{"t": "전장을 폭넓게 누비며 거리낌 없이 팀원들의 빈자리를 채운다.", "w": {"Dist":10, "Sup":6, "Mob":4}}, {"t": "보이지 않는 큰 템포를 읽으며 직관적이고 묵직하게 대응한다.", "w": {"Ord":10, "Nat":6, "Pac":4}}, {"t": "생존 확률을 극대화하기 위해 복잡하고 철저한 계산을 끝마친다.", "w": {"Log":10, "Res":6, "Cpx":4}}, {"t": "내 앞을 막는 문제라면 공격적이고 파괴적인 힘으로 날려버린다.", "w": {"Shd":10, "Agg":6, "Des":4}}]},
    {"opts": [{"t": "리더의 짐을 짊어지고 묵직하게 버텨내야겠다고 다짐한다.", "w": {"Res":10, "Shd":6, "Pac":4}}, {"t": "가장 빠르고 효율적인 논리적 타격 경로를 구상하며 속도를 낸다.", "w": {"Agg":10, "Log":6, "Mob":4}}, {"t": "절차에 따라 천천히 모두가 정당하게 대우받도록 챙긴다.", "w": {"Sup":10, "Ord":6, "Pac":4}}, {"t": "복잡한 권력에서 벗어나 자유롭고 직관적인 나만의 통찰을 믿는다.", "w": {"Nat":10, "Dist":6, "Cpx":4}}]},
    {"opts": [{"t": "자연의 흐름을 읽으며 멀리 떨어져서 길고 깊은 사색에 잠긴다.", "w": {"Dist":10, "Nat":6, "Pac":4}}, {"t": "복잡한 룰을 가진 게임이나 취미를 규율에 맞게 서포트하며 즐긴다.", "w": {"Ord":10, "Sup":6, "Cpx":4}}, {"t": "빠른 두뇌 회전과 공격적인 논리 전개가 필요한 지적 게임을 한다.", "w": {"Log":10, "Agg":6, "Mob":4}}, {"t": "피 튀기고 암울한 하드코어 세계관에서 책임을 다하는 플레이를 한다.", "w": {"Shd":10, "Res":6, "Des":4}}]},
    {"opts": [{"t": "방패처럼 묵직하게 감정을 통제하며 오랜 시간 흔들림 없이 버틴다.", "w": {"Res":10, "Ord":6, "Pac":4}}, {"t": "시야를 빠르게 벗어난 뒤 복잡하고 치명적인 반격을 세팅한다.", "w": {"Agg":10, "Dist":6, "Mob":4}}, {"t": "내 살을 깎아서라도 험악해진 분위기를 보듬어 사람들을 안심시킨다.", "w": {"Sup":10, "Shd":6, "Des":-4}}, {"t": "찰나의 영감을 정교한 논리로 가공하여 상대를 완전히 압도한다.", "w": {"Nat":10, "Log":6, "Cpx":4}}]},
    {"opts": [{"w": {"Dist":10, "Agg":6, "Des":4}, "t": "적의 접근을 불허하며 멀리서 속사포처럼 화염을 쏟아붓는 파괴 마법"}, {"w": {"Ord":10, "Res":6, "Pac":4}, "t": "오랜 시간의 시전을 거쳐 모든 공격을 튕겨내는 견고한 절대 방어 마법"}, {"w": {"Log":10, "Nat":6, "Cpx":4}, "t": "대자연의 원소를 학문적으로 분석해 정교하게 엮어내는 고등 마법"}, {"w": {"Shd":10, "Sup":6, "Mob":4}, "t": "어둠에 몸을 숨긴 채 빠르게 전장을 누비며 적을 약화시키는 저주 마법"}]},
    {"opts": [{"w": {"Res":10, "Dist":6, "Mob":-4}, "t": "홀로 남더라도 끝까지 적의 공격을 온몸으로 받아내며 버티는 굳건함"}, {"w": {"Agg":10, "Ord":6, "Des":4}, "t": "군더더기 없는 완벽한 사이클로 콤보를 욱여넣어 적을 찢어버리는 파괴력"}, {"w": {"Sup":10, "Log":6, "Pac":4}, "t": "가장 확률 높은 생존자를 계산해 오랜 시간 모은 힐을 모두 몰아주는 냉정함"}, {"w": {"Nat":10, "Shd":6, "Cpx":4}, "t": "금기를 깨고 야성의 본능에 나를 맡겨 복잡한 광란의 상태로 폭주하는 쾌감"}]},
    {"opts": [{"w": {"Dist":10, "Res":6, "Pac":4}, "t": "느릿하지만 흔들림 없이 세상을 관조하는 외롭고 견고한 은둔자"}, {"w": {"Ord":10, "Agg":6, "Mob":4}, "t": "규율의 이름으로 전장을 빠르게 휩쓸고 정화해버리는 무자비한 심판관"}, {"w": {"Log":10, "Sup":6, "Cpx":4}, "t": "복잡한 전술과 시너지 계산으로 파티 전원의 기량을 끌어올리는 지휘관"}, {"w": {"Shd":10, "Nat":6, "Des":4}, "t": "혼돈의 기운을 받아들여 대자연마저 파괴해버리는 흉터 가득한 광전사"}]},
    {"opts": [{"w": {"Mob":10, "Des":6, "Agg":4}, "t": "쉴 새 없는 기동성으로 전장을 헤집으며 폭발적인 화력을 투사하는 방식"}, {"w": {"Cpx":10, "Pac":6, "Log":4}, "t": "느린 호흡 속에서 복잡한 자원을 완벽하게 계산하며 스킬을 세팅하는 쾌감"}, {"w": {"Des":10, "Res":6, "Shd":4}, "t": "내 피가 깎이는 것을 견뎌내며 적의 뼈와 살을 분리해버리는 원초적 파괴"}, {"w": {"Pac":10, "Dist":6, "Ord":4}, "t": "아주 멀리 안전한 곳에 자리 잡고 느긋하게 질서 있는 루틴을 돌리는 평온함"}]},
    {"opts": [{"w": {"Mob":10, "Sup":6, "Nat":4}, "t": "전장을 휙휙 날아다니며 본능적으로 파티원의 체력을 채워주는 역동성"}, {"w": {"Cpx":10, "Dist":6, "Log":4}, "t": "거리를 벌린 채 남들은 이해하기 힘든 복잡한 사이클을 고독하게 완성하는 일"}, {"w": {"Des":10, "Agg":6, "Shd":4}, "t": "숨통을 끊겠다는 일념 하나로 어둠 속에서 파괴적인 공격을 퍼붓는 집요함"}, {"w": {"Pac":10, "Res":6, "Ord":4}, "t": "거대한 방패 뒤에서 긴 템포로 파티의 진형과 원칙을 지켜내는 든든함"}]},
    {"opts": [{"w": {"Mob":10, "Nat":6, "Dist":4}, "t": "형식에 얽매이지 않고 바람처럼 독립적으로 세상을 떠도는 자유로움"}, {"w": {"Cpx":10, "Ord":6, "Log":4}, "t": "엄격한 룰과 피아노를 치는 듯한 복잡한 조작 속에서 지적 한계를 시험하는 일"}, {"w": {"Des":10, "Shd":6, "Agg":4}, "t": "스스로를 악마에 내어주더라도 눈앞의 적을 갈기갈기 찢어놓는 광기"}, {"w": {"Pac":10, "Sup":6, "Res":4}, "t": "결과가 조금 늦어지더라도 묵묵히 희생하며 동료를 끝까지 서포트하는 인내"}]},
    {"opts": [{"w": {"Mob":10, "Agg":6, "Nat":4}, "t": "머리보다 몸이 먼저 반응하여 적진으로 번개처럼 돌진하는 액션"}, {"w": {"Cpx":10, "Res":6, "Log":4}, "t": "쏟아지는 공격을 맞으면서도 머릿속으로 다음 수를 정교하게 설계하는 냉철함"}, {"w": {"Des":10, "Dist":6, "Shd":4}, "t": "멀리서 지켜보다가 가장 어두운 저주와 혼돈의 불덩어리로 파멸시키는 쾌락"}, {"w": {"Pac":10, "Ord":6, "Sup":4}, "t": "서두르지 않고 완벽한 질서를 갖춰 모두가 만족할 평화로운 치유를 전개하는 것"}]}
]

# ============================================================
# 4. 코어 로직 및 유틸리티
# ============================================================
EXPECTED_MEANS = {k: 0.0 for k in DIMS}
for q in QUESTIONS:
    for k in DIMS:
        EXPECTED_MEANS[k] += sum(opt["w"].get(k, 0) for opt in q["opts"]) / len(q["opts"])

GLOBAL_SPEC_MEAN = {k: sum(s.get(k, 0) for s in SPECS.values()) / len(SPECS) for k in DIMS}

def cosine_sim(vec1, vec2):
    dot = sum(vec1[k] * vec2[k] for k in DIMS)
    mag1 = math.sqrt(sum(vec1[k]**2 for k in DIMS)) or 1
    mag2 = math.sqrt(sum(vec2[k]**2 for k in DIMS)) or 1
    return dot / (mag1 * mag2)

def get_rankings(u_vec):
    """39개 전문화와 비교 후, 클래스 마진(보정치)을 더해 최종 랭킹을 산출합니다."""
    u_centered = {k: u_vec.get(k, 0) - EXPECTED_MEANS[k] for k in DIMS}
    ranks = []
    
    for spec_name, s_vec in SPECS.items():
        s_centered = {k: s_vec.get(k, 0) - GLOBAL_SPEC_MEAN[k] for k in DIMS}
        raw_score = cosine_sim(u_centered, s_centered)
        
        # 소속 클래스를 찾고 마진을 더함
        cls_name = SPEC_TO_CLASS[spec_name]
        final_score = raw_score + CLASS_MARGINS[cls_name]
        
        ranks.append({
            "spec": spec_name,
            "class": cls_name,
            "score": final_score
        })
        
    return sorted(ranks, key=lambda x: x["score"], reverse=True)

# 레이더 차트 (UI)
def radar_svg(u_vec, spec_vec):
    import math as m
    cx, cy, r = 200, 200, 140
    n = len(DIMS)

    def pt(val, idx):
        ang  = m.pi / 2 - 2 * m.pi * idx / n
        norm = (val + 100) / 200 if DIMS[idx] in ["Dist", "Mob", "Cpx", "Des", "Pac"] else val / 100
        norm = max(0.0, min(1.0, norm))
        return cx + r * norm * m.cos(ang), cy - r * norm * m.sin(ang)

    grid = "".join(f'<polygon points="{" ".join(f"{cx+r*lv*m.cos(m.pi/2-2*m.pi*i/n):.1f},{cy-r*lv*m.sin(m.pi/2-2*m.pi*i/n):.1f}" for i in range(n))}" fill="none" stroke="#334155" stroke-width="1"/>' for lv in [0.25, 0.5, 0.75, 1.0])
    axes = "".join(f'<line x1="{cx}" y1="{cy}" x2="{cx+r*m.cos(m.pi/2-2*m.pi*i/n):.1f}" y2="{cy-r*m.sin(m.pi/2-2*m.pi*i/n):.1f}" stroke="#475569" stroke-width="1"/>' for i in range(n))
    spec_pts = " ".join(f"{pt(spec_vec.get(d,0),i)[0]:.1f},{pt(spec_vec.get(d,0),i)[1]:.1f}" for i,d in enumerate(DIMS))
    u_pts    = " ".join(f"{pt(u_vec.get(d,0),i)[0]:.1f},{pt(u_vec.get(d,0),i)[1]:.1f}"    for i,d in enumerate(DIMS))
    labels   = "".join(
        f'<text x="{cx+(r+22)*m.cos(m.pi/2-2*m.pi*i/n):.1f}" y="{cy-(r+22)*m.sin(m.pi/2-2*m.pi*i/n):.1f}" '
        f'text-anchor="{"end" if cx+(r+22)*m.cos(m.pi/2-2*m.pi*i/n)<cx-10 else ("start" if cx+(r+22)*m.cos(m.pi/2-2*m.pi*i/n)>cx+10 else "middle")}" '
        f'fill="#94a3b8" font-size="11" font-family="sans-serif">{DIM_LABELS[d]}</text>'
        for i,d in enumerate(DIMS)
    )
    return f"""<svg viewBox="0 0 400 430" xmlns="http://www.w3.org/2000/svg" style="background:#0f172a;border-radius:12px;">
  {grid}{axes}
  <polygon points="{spec_pts}" fill="rgba(251,191,36,0.15)" stroke="#f59e0b" stroke-width="2"/>
  <polygon points="{u_pts}"    fill="rgba(99,102,241,0.2)"  stroke="#6366f1" stroke-width="2.5"/>
  {labels}
  <rect x="55"  y="395" width="12" height="12" fill="#6366f1" rx="2"/>
  <text x="73"  y="406" fill="#94a3b8" font-size="11" font-family="sans-serif">나의 성향</text>
  <rect x="175" y="395" width="12" height="12" fill="#f59e0b" rx="2"/>
  <text x="193" y="406" fill="#94a3b8" font-size="11" font-family="sans-serif">추천 전문화</text>
</svg>"""

# ============================================================
# 5. Streamlit 앱 구동부
# ============================================================
if "step" not in st.session_state:
    st.session_state.step     = 0
    st.session_state.u        = {k: 0 for k in DIMS}
    st.session_state.history  = []
    st.session_state.finished = False

st.set_page_config(page_title="아제로스 영혼 분석", page_icon="⚔️", layout="centered")
st.markdown("""
<style>
    .stButton>button{
        background:#1e293b; color:#e2e8f0; border:1px solid #334155; border-radius:8px;
        padding:.6rem 1rem; text-align:left; white-space:normal; height:auto; transition:all .2s;
    }
    .stButton>button:hover{background:#6366f1;border-color:#6366f1;color:#fff;}
    .result-card{ background:linear-gradient(135deg,#1e293b,#0f172a); border:1px solid #334155; border-radius:12px; padding:1.4rem; margin-bottom:1rem; }
    .class-header{ color: #e2e8f0; font-size: 1.8rem; font-weight: bold; margin-bottom: 0.2rem; }
    .spec-header{ color: #f59e0b; font-size: 1.2rem; margin-bottom: 0.8rem; }
</style>
""", unsafe_allow_html=True)

if not st.session_state.finished:
    if st.session_state.step >= len(QUESTIONS):
        st.session_state.finished = True
        st.rerun()

    q_data = QUESTIONS[st.session_state.step]
    st.title("⚔️ 아제로스 영혼 정밀 분석")
    st.caption("12개의 심리·전투 지표가 당신의 아제로스 운명을 결정합니다.")
    st.divider()
    st.progress(st.session_state.step / len(QUESTIONS), text=f"진행: {st.session_state.step} / {len(QUESTIONS)}문항 완료")
    st.write("")
    st.subheader(f"Q{st.session_state.step + 1}. {q_data['opts'][0].get('q', '당신의 선택은?')}") # Fallback if q string wasn't explicitly added to dict
    
    # Render options (handling the slight structure change in my Q string writing)
    for i, opt in enumerate(q_data["opts"]):
        if st.button(opt["t"], key=f"q{st.session_state.step}_o{i}", use_container_width=True):
            st.session_state.history.append(opt["w"])
            for k, v in opt["w"].items():
                st.session_state.u[k] = st.session_state.u.get(k, 0) + v
            st.session_state.step += 1
            st.rerun()

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ 이전으로", use_container_width=True) and st.session_state.step > 0:
            prev = st.session_state.history.pop()
            for k, v in prev.items():
                st.session_state.u[k] -= v
            st.session_state.step -= 1
            st.rerun()
    with c2:
        if st.button("🔄 처음부터", use_container_width=True):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()

else:
    u = st.session_state.u
    final_ranks = get_rankings(u)
    
    # 1위, 2위 추출 (클래스가 겹치지 않도록 2위 선정)
    top1 = final_ranks[0]
    top2 = next(r for r in final_ranks if r["class"] != top1["class"])

    st.balloons()
    st.title("⚔️ 당신의 아제로스 영혼 분석 결과")
    st.divider()

    st.markdown(f'<div class="class-header">🥇 추천 직업: <b>{top1["class"]}</b></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="spec-header">💡 완벽한 전문화: <b>{top1["spec"]}</b></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-card">{SPEC_DESC.get(top1["spec"],"")}</div>', unsafe_allow_html=True)

    st.subheader("📊 나의 12차원 성향 레이더")
    st.markdown(radar_svg(u, SPECS[top1["spec"]]), unsafe_allow_html=True)

    st.divider()
    st.markdown(f'<div class="class-header" style="font-size:1.4rem;">🥈 2위 추천 직업: <b>{top2["class"]}</b></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="spec-header" style="font-size:1rem; color:#cbd5e1;">💡 대안 전문화: <b>{top2["spec"]}</b></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-card">{SPEC_DESC.get(top2["spec"],"")}</div>', unsafe_allow_html=True)

    st.divider()
    if st.button("🔄 다시 테스트하기", use_container_width=True):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()
