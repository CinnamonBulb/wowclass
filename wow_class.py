import streamlit as st
import math

# ============================================================
# 1. 39개 전문화 8차원 좌표 DB
# ============================================================
SPECS = {
    "분노 전사":          {"Res":20,"Sup":5, "Dist":-90,"Log":20,"Agg":95,"Nat":25,"Ord":15,"Shd":30},
    "무기 전사":          {"Res":35,"Sup":5, "Dist":-70,"Log":45,"Agg":80,"Nat":20,"Ord":50,"Shd":20},
    "방어 전사":          {"Res":95,"Sup":30,"Dist":-80,"Log":55,"Agg":40,"Nat":10,"Ord":90,"Shd":10},
    "신성 성기사":        {"Res":60,"Sup":90,"Dist":-20,"Log":60,"Agg":20,"Nat":10,"Ord":90,"Shd":5},
    "보호 성기사":        {"Res":92,"Sup":40,"Dist":-40,"Log":55,"Agg":30,"Nat":10,"Ord":95,"Shd":10},
    "응징 성기사":        {"Res":40,"Sup":10,"Dist":-50,"Log":50,"Agg":75,"Nat":10,"Ord":75,"Shd":40},
    "야수 사냥꾼":        {"Res":20,"Sup":15,"Dist":80, "Log":30,"Agg":70,"Nat":90,"Ord":20,"Shd":10},
    "사격 사냥꾼":        {"Res":15,"Sup":10,"Dist":95, "Log":75,"Agg":55,"Nat":40,"Ord":65,"Shd":10},
    "생존 사냥꾼":        {"Res":30,"Sup":15,"Dist":-30,"Log":60,"Agg":65,"Nat":75,"Ord":35,"Shd":25},
    "암살 도적":          {"Res":20,"Sup":5, "Dist":-40,"Log":80,"Agg":65,"Nat":30,"Ord":45,"Shd":80},
    "무법 도적":          {"Res":25,"Sup":5, "Dist":-50,"Log":35,"Agg":85,"Nat":50,"Ord":15,"Shd":50},
    "교활 도적":          {"Res":15,"Sup":5, "Dist":-20,"Log":90,"Agg":45,"Nat":20,"Ord":55,"Shd":65},
    "수양 사제":          {"Res":40,"Sup":75,"Dist":40, "Log":90,"Agg":10,"Nat":15,"Ord":75,"Shd":55},
    "신성 사제":          {"Res":35,"Sup":95,"Dist":30, "Log":65,"Agg":5, "Nat":20,"Ord":70,"Shd":5},
    "암흑 사제":          {"Res":25,"Sup":15,"Dist":60, "Log":70,"Agg":55,"Nat":10,"Ord":30,"Shd":90},
    "혈기 죽음의 기사":   {"Res":95,"Sup":10,"Dist":-50,"Log":35,"Agg":70,"Nat":10,"Ord":30,"Shd":90},
    "냉기 죽음의 기사":   {"Res":45,"Sup":10,"Dist":-60,"Log":60,"Agg":70,"Nat":5, "Ord":50,"Shd":70},
    "부정 죽음의 기사":   {"Res":30,"Sup":10,"Dist":-30,"Log":50,"Agg":80,"Nat":5, "Ord":25,"Shd":95},
    "원소 주술사":        {"Res":20,"Sup":25,"Dist":85, "Log":65,"Agg":55,"Nat":85,"Ord":35,"Shd":20},
    "고양 주술사":        {"Res":20,"Sup":50,"Dist":-35,"Log":50,"Agg":70,"Nat":90,"Ord":25,"Shd":15},
    "복원 주술사":        {"Res":30,"Sup":92,"Dist":55, "Log":50,"Agg":10,"Nat":95,"Ord":30,"Shd":10},
    "비전 마법사":        {"Res":10,"Sup":10,"Dist":90, "Log":92,"Agg":50,"Nat":10,"Ord":80,"Shd":30},
    "화염 마법사":        {"Res":10,"Sup":10,"Dist":80, "Log":60,"Agg":85,"Nat":20,"Ord":35,"Shd":25},
    "냉기 마법사":        {"Res":20,"Sup":10,"Dist":85, "Log":80,"Agg":35,"Nat":25,"Ord":75,"Shd":20},
    "고통 흑마법사":      {"Res":20,"Sup":10,"Dist":85, "Log":75,"Agg":50,"Nat":10,"Ord":45,"Shd":90},
    "악마술사 흑마법사":  {"Res":15,"Sup":15,"Dist":80, "Log":60,"Agg":65,"Nat":10,"Ord":30,"Shd":85},
    "파괴 흑마법사":      {"Res":20,"Sup":10,"Dist":90, "Log":70,"Agg":90,"Nat":10,"Ord":40,"Shd":80},
    "양조 수도사":        {"Res":82,"Sup":45,"Dist":-30,"Log":65,"Agg":40,"Nat":80,"Ord":50,"Shd":30},
    "운무 수도사":        {"Res":30,"Sup":88,"Dist":-10,"Log":55,"Agg":15,"Nat":90,"Ord":40,"Shd":20},
    "풍운 수도사":        {"Res":25,"Sup":15,"Dist":-40,"Log":55,"Agg":75,"Nat":85,"Ord":35,"Shd":15},
    "조화 드루이드":      {"Res":20,"Sup":50,"Dist":90, "Log":80,"Agg":40,"Nat":95,"Ord":50,"Shd":20},
    "야성 드루이드":      {"Res":30,"Sup":10,"Dist":-80,"Log":45,"Agg":80,"Nat":85,"Ord":25,"Shd":30},
    "수호 드루이드":      {"Res":90,"Sup":35,"Dist":-70,"Log":50,"Agg":35,"Nat":80,"Ord":55,"Shd":15},
    "회복 드루이드":      {"Res":25,"Sup":90,"Dist":40, "Log":55,"Agg":10,"Nat":95,"Ord":35,"Shd":10},
    "파멸 악마사냥꾼":    {"Res":25,"Sup":10,"Dist":-20,"Log":45,"Agg":88,"Nat":30,"Ord":20,"Shd":75},
    "복수 악마사냥꾼":    {"Res":88,"Sup":15,"Dist":-35,"Log":40,"Agg":55,"Nat":25,"Ord":30,"Shd":70},
    "황폐 기원사":        {"Res":20,"Sup":10,"Dist":75, "Log":70,"Agg":75,"Nat":40,"Ord":45,"Shd":55},
    "보존 기원사":        {"Res":35,"Sup":85,"Dist":65, "Log":70,"Agg":15,"Nat":55,"Ord":55,"Shd":40},
    "증강 기원사":        {"Res":30,"Sup":60,"Dist":50, "Log":75,"Agg":50,"Nat":50,"Ord":60,"Shd":45},
}

DIMS = ["Res","Sup","Dist","Log","Agg","Nat","Ord","Shd"]

DIM_LABELS = {
    "Res": "책임감·방어", "Sup": "지원·배려", "Dist": "거리·독립", "Log": "분석·전략",
    "Agg": "추진력·실행", "Nat": "직관·유연성", "Ord": "질서·규율", "Shd": "희생·어둠",
}

DIM_RESULT_DESC = {
    "Res": "위기 상황에서 책임을 자처하고 끝까지 자리를 지키는 성향이 강합니다.",
    "Sup": "타인을 먼저 생각하고 뒤에서 든든하게 받쳐주는 배려심이 두드러집니다.",
    "Dist": "독립적이고 거리를 두며 상황을 관찰하는 방식을 선호합니다.",
    "Log": "체계적으로 분석하고 전략을 세운 뒤 움직이는 논리파입니다.",
    "Agg": "생각보다 행동이 앞서는 강한 추진력과 실행력을 가지고 있습니다.",
    "Nat": "감각과 직관을 믿으며 상황에 유연하게 적응하는 성향이 강합니다.",
    "Ord": "원칙과 규율을 중시하고 안정적인 구조 안에서 최고의 역량을 발휘합니다.",
    "Shd": "대가를 치르더라도 목표를 달성하려는 집중력과 헌신이 강합니다.",
}

SPEC_DESC = {
    "분노 전사":          "본능과 광기로 전장을 지배합니다. 몸이 먼저 움직이는 당신, 피가 끓는 곳에 답이 있습니다.",
    "무기 전사":          "정밀한 무기 운용과 전술적 판단이 조화를 이룹니다. 격투가보다는 검술가에 가깝습니다.",
    "방어 전사":          "흔들리지 않는 바위. 팀의 전방을 홀로 떠받드는 냉철한 수호자입니다.",
    "신성 성기사":        "빛을 통해 동료를 살립니다. 전투의 흐름을 유지하며 희망을 나눠주는 존재입니다.",
    "보호 성기사":        "신념과 강철로 방어선을 만드는 절대 탱커. 질서와 책임의 화신입니다.",
    "응징 성기사":        "정의의 이름으로 적을 심판합니다. 빛의 힘을 공격에 담아내는 솔로잉의 왕.",
    "야수 사냥꾼":        "자연과 한 몸인 사냥꾼. 동물과의 유대가 전투력의 원천입니다.",
    "사격 사냥꾼":        "적이 닿기 전에 끝냅니다. 거리와 정밀함이 최고의 무기입니다.",
    "생존 사냥꾼":        "함정과 폭발물로 근접전을 이끄는 이색 사냥꾼. 야생의 지략으로 싸웁니다.",
    "암살 도적":          "독과 그림자로 표적을 제거하는 냉혹한 암살자. 계획 없는 행동은 없습니다.",
    "무법 도적":          "해적 기질의 전투사. 예측 불가능한 화력과 짜릿한 행운이 무기입니다.",
    "교활 도적":          "모든 것을 꿰뚫는 전략가. 적의 허점을 찾아 침투하는 고수입니다.",
    "수양 사제":          "내면의 빛과 어둠을 동시에 다루는 균형의 힐러. 사려깊고 강인합니다.",
    "신성 사제":          "순수한 빛으로 치유합니다. 팀의 안녕이 곧 나의 기쁨인 헌신적 힐러입니다.",
    "암흑 사제":          "어둠의 속삭임을 무기로 삼는 딜러. 정신을 파고드는 심연의 전사입니다.",
    "혈기 죽음의 기사":   "적의 생명을 빨아 자신의 것으로 만드는 죽음의 탱커. 어둠 속 불사의 존재.",
    "냉기 죽음의 기사":   "냉기로 적을 저지하고 파괴하는 죽음의 기사. 냉철한 이성과 서릿발이 공존합니다.",
    "부정 죽음의 기사":   "역병과 부패로 전장을 오염시킵니다. 가장 공격적인 죽음의 기사 전문화.",
    "원소 주술사":        "대지·불·폭풍을 아우르는 원소의 목소리. 자연과 마법의 경계에 섭니다.",
    "고양 주술사":        "영혼의 힘으로 팀원을 강화하는 독특한 서포터 딜러. 협력이 화력입니다.",
    "복원 주술사":        "대지의 숨결로 치유합니다. 여러 명을 동시에 살리는 광역 힐의 전문가.",
    "비전 마법사":        "마법의 본질을 탐구하는 지식인. 완벽한 로테이션에서 오는 쾌감을 압니다.",
    "화염 마법사":        "불꽃으로 전장을 태웁니다. 화끈한 폭발감이 매력인 마법사입니다.",
    "냉기 마법사":        "얼음으로 적을 통제하고 파괴합니다. 냉정한 판단으로 기회를 만듭니다.",
    "고통 흑마법사":      "저주와 도트로 적을 서서히 무너뜨립니다. 인내와 계산이 미덕.",
    "악마술사 흑마법사":  "악마를 소환해 전장을 가득 채웁니다. 세력을 키워 지배하는 타입.",
    "파괴 흑마법사":      "혼돈의 불꽃을 마음껏 터뜨립니다. 어둠 속 화력 딜러의 극한입니다.",
    "양조 수도사":        "술을 마시며 싸우는 독특한 탱커. 자연의 흐름처럼 유연하게 피해를 흘려냅니다.",
    "운무 수도사":        "흐르는 안개처럼 치유합니다. 움직임과 힐이 하나가 되는 역동적 힐러.",
    "풍운 수도사":        "권각의 달인. 빠르고 리드미컬한 근접전에서 최고의 쾌감을 느낍니다.",
    "조화 드루이드":      "별빛과 달빛으로 원거리 공격을 펼칩니다. 자연의 섭리를 이해하는 학자형 딜러.",
    "야성 드루이드":      "맹수가 되어 싸웁니다. 본능과 속도가 지배하는 근접 딜러.",
    "수호 드루이드":      "곰 형태로 팀을 지킵니다. 자연의 견고함이 방어선이 되는 탱커.",
    "회복 드루이드":      "성장하는 생명의 힘으로 치유합니다. 지속 힐의 여왕, 자연과 하나.",
    "파멸 악마사냥꾼":    "어둠의 힘을 받아들여 적을 베어냅니다. 화려하고 파괴적인 근접 딜러.",
    "복수 악마사냥꾼":    "악마의 힘을 흡수하며 적의 공격을 역이용합니다. 독특한 리소스 탱커.",
    "황폐 기원사":        "용의 마법으로 전장을 휩씁니다. 원소 화력과 도트를 결합한 원거리 딜러.",
    "보존 기원사":        "시간을 다루며 동료를 되살립니다. 독특한 메커니즘의 힐러.",
    "증강 기원사":        "아군을 강화하는 독보적 서포터. 팀 전체의 성능을 올리는 특이한 딜러.",
}

# ============================================================
# 2. 20개 일상 질문지
# ============================================================
QUESTIONS = [
    {
        "q": "Q1. 모두가 기대하던 일이 예상치 못한 문제로 엉망이 됐습니다. 당신은?",
        "opts": [
            {"t": "상황의 책임자로 나서서 문제를 정면으로 수습한다.",            "w": {"Res":14, "Ord":4}},
            {"t": "동요한 사람들을 먼저 안심시키고 감정을 다독인다.",            "w": {"Sup":14, "Nat":4}},
            {"t": "원인 분석보다 당장 실행 가능한 해결책을 찾아 뛰어든다.",      "w": {"Agg":12, "Dist":-6}},
            {"t": "왜 이런 일이 벌어졌는지 구조를 파악해 근본 원인을 짚는다.",  "w": {"Log":14, "Dist":4}},
        ],
    },
    {
        "q": "Q2. 꼼꼼히 준비한 계획이 예상치 못한 변수로 완전히 틀어졌습니다. 당신은?",
        "opts": [
            {"t": "기존 원칙과 절차를 기준 삼아 하나씩 복구한다.",               "w": {"Ord":14, "Res":4}},
            {"t": "주변 사람들의 의견을 들으며 모두가 납득할 새 방향을 찾는다.", "w": {"Nat":12, "Sup":6}},
            {"t": "고민 없이 일단 움직이며 가장 빠른 돌파구를 만든다.",          "w": {"Agg":14, "Dist":-6}},
            {"t": "인과관계를 냉정하게 따져 가장 효율적인 새 경로를 설계한다.", "w": {"Log":14, "Dist":4}},
        ],
    },
    {
        "q": "Q3. 처음 가는 낯선 장소에서 길을 잃었습니다. 당신의 첫 번째 행동은?",
        "opts": [
            {"t": "주변 지형과 이정표를 분석해 경로를 혼자 추론한다.",          "w": {"Log":12, "Dist":8}},
            {"t": "일단 걷기 시작하며 몸으로 감을 익힌다.",                      "w": {"Agg":10, "Nat":6, "Dist":-6}},
            {"t": "지나가는 사람에게 먼저 말을 걸어 도움을 구한다.",            "w": {"Sup":12, "Nat":6}},
            {"t": "새로운 공간을 탐색하는 과정 자체를 흥미롭게 즐긴다.",        "w": {"Nat":12, "Shd":4}},
        ],
    },
    {
        "q": "Q4. 일이나 관계에서 당신이 가장 중요하게 생각하는 가치는?",
        "opts": [
            {"t": "어떤 어려움이 있어도 약속을 끝까지 지켜내는 책임감",         "w": {"Res":12, "Ord":6}},
            {"t": "함께하는 사람들과 성장하고 따뜻하게 지내는 협동",            "w": {"Sup":12, "Nat":6}},
            {"t": "목표를 세우면 지체 없이 밀어붙이는 추진력",                  "w": {"Agg":12, "Ord":-4}},
            {"t": "오차 없는 완벽한 결과를 만드는 지적 전문성",                  "w": {"Log":12, "Ord":6}},
        ],
    },
    {
        "q": "Q5. 주변 친한 사람들 간에 갈등이 생겼습니다. 당신은?",
        "opts": [
            {"t": "양쪽 입장을 모두 듣고 유연하게 중재한다.",                    "w": {"Sup":12, "Nat":6}},
            {"t": "규칙과 원칙을 기준으로 시시비비를 가린다.",                   "w": {"Ord":12, "Log":6}},
            {"t": "갈등에 휘말리지 않고 각자 역할에 집중하도록 돌린다.",         "w": {"Dist":10, "Log":6}},
            {"t": "갈등의 근본 원인이 무엇인지 구조적으로 파악해 제안한다.",    "w": {"Log":12, "Shd":4}},
        ],
    },
    {
        "q": "Q6. 처음 접하는 낯선 도구나 프로그램을 써야 합니다. 당신의 스타일은?",
        "opts": [
            {"t": "설명서와 작동 원리부터 완전히 파악한 뒤 시작한다.",          "w": {"Log":12, "Ord":6}},
            {"t": "일단 이것저것 눌러보며 직접 몸으로 익힌다.",                  "w": {"Agg":10, "Dist":-6}},
            {"t": "주변 사람의 후기나 조언을 먼저 참고한다.",                    "w": {"Sup":8, "Nat":8}},
            {"t": "핵심 기능 하나만 빠르게 파악해 즉시 실무에 적용한다.",       "w": {"Agg":10, "Log":6}},
        ],
    },
    {
        "q": "Q7. 오늘은 진짜 쉬고 싶습니다. 당신이 선택하는 환경은?",
        "opts": [
            {"t": "익숙한 루틴과 정해진 공간에서 안정감을 느낀다.",              "w": {"Ord":12, "Res":4}},
            {"t": "자연 속 조용한 곳에서 아무 생각 없이 걷는다.",                "w": {"Nat":12, "Dist":6}},
            {"t": "에너지를 마음껏 발산할 수 있는 활동적인 공간.",                "w": {"Agg":12, "Dist":-6}},
            {"t": "아무에게도 방해받지 않고 나만의 세계에 완전히 몰입한다.",    "w": {"Dist":12, "Log":6}},
        ],
    },
    {
        "q": "Q8. 중요한 마감을 앞두고 치명적인 실수를 발견했습니다. 당신은?",
        "opts": [
            {"t": "내가 혼자 끝까지 책임지고 밤을 새워서라도 고친다.",            "w": {"Res":12, "Agg":6}},
            {"t": "즉시 팀원들에게 상황을 공유하고 역할을 나눠 함께 해결한다.", "w": {"Sup":12, "Nat":6}},
            {"t": "가장 급한 부분부터 임기응변으로 빠르게 처리한다.",            "w": {"Agg":12, "Log":4}},
            {"t": "실수가 생긴 구조를 먼저 파악해 근본 보완책을 마련한다.",      "w": {"Log":12, "Shd":4}},
        ],
    },
    {
        "q": "Q9. 주변 사람들이 당신을 가장 자주 어떻게 표현하나요?",
        "opts": [
            {"t": "어떤 상황에서도 자리를 지키는 믿음직한 사람",                 "w": {"Res":12, "Ord":6}},
            {"t": "주변을 세심하게 챙기고 에너지를 북돋아 주는 따뜻한 사람",   "w": {"Sup":12, "Nat":6}},
            {"t": "일 처리가 시원시원하고 추진력이 강한 사람",                   "w": {"Agg":12, "Dist":-4}},
            {"t": "이성적이고 깊이 있는 통찰을 가진 스마트한 사람",              "w": {"Log":12, "Dist":4}},
        ],
    },
    {
        "q": "Q10. 평소 당신의 개인 공간(책상, 방)은 어떤 상태인가요?",
        "opts": [
            {"t": "모든 물건이 제자리에 놓인 정갈한 상태",                       "w": {"Ord":12, "Log":4}},
            {"t": "취향과 소품들이 어우러진 편안하고 조화로운 상태",             "w": {"Nat":12, "Sup":4}},
            {"t": "집중 중인 도구들이 활발하게 펼쳐진 역동적인 상태",            "w": {"Agg":12, "Dist":-4}},
            {"t": "필요한 것만 남겨둔 지극히 심플하고 조용한 상태",              "w": {"Dist":10, "Shd":6}},
        ],
    },
    {
        "q": "Q11. 누군가 당신이 잘 아는 분야에 대해 명백히 틀린 말을 합니다. 당신은?",
        "opts": [
            {"t": "단호하게 근거를 들어 즉시 바로잡는다.",                       "w": {"Ord":12, "Agg":6}},
            {"t": "상대가 상처받지 않게 조심스럽게 의견을 전한다.",              "w": {"Sup":12, "Nat":6}},
            {"t": "굳이 불필요한 논쟁을 피하고 속으로만 판단한다.",              "w": {"Dist":12, "Log":4}},
            {"t": "저 사람이 왜 저런 결론에 도달했는지 배경을 분석한다.",        "w": {"Log":10, "Shd":8}},
        ],
    },
    {
        "q": "Q12. 오랜 노력 끝에 결실을 맺었습니다. 당신이 가장 크게 느끼는 보람은?",
        "opts": [
            {"t": "나의 헌신과 실력이 인정받는 명예로운 성취감",                 "w": {"Res":12, "Ord":6}},
            {"t": "함께 고생한 사람들과 기쁨을 나누는 진한 유대감",              "w": {"Sup":12, "Nat":6}},
            {"t": "목표를 달성했다는 날카로운 만족감과 결과 자체",               "w": {"Agg":10, "Shd":6}},
            {"t": "지식과 통찰이 확장됐다는 지적 성취감",                        "w": {"Log":12, "Dist":4}},
        ],
    },
    {
        "q": "Q13. 오랜 시간 들여 완성한 작업물에서 사소한 오류 하나를 발견했습니다. 당신은?",
        "opts": [
            {"t": "완벽하게 처음부터 다시 점검하고 수정한다.",                    "w": {"Ord":12, "Res":6}},
            {"t": "전체 기능에 영향이 없다면 그대로 진행한다.",                  "w": {"Agg":10, "Nat":6}},
            {"t": "오류가 어디서 발생했는지 구조적으로 역추론한다.",              "w": {"Log":12, "Shd":4}},
            {"t": "경험 많은 사람에게 의견을 구해 판단한다.",                    "w": {"Sup":12, "Nat":4}},
        ],
    },
    {
        "q": "Q14. 오래 기다려야 하는 상황에 처했습니다. 당신은?",
        "opts": [
            {"t": "목표가 있으니 묵묵히 기다린다. 기다림도 실력이다.",            "w": {"Res":10, "Ord":8}},
            {"t": "비슷한 대안을 빠르게 찾아 상황을 바꾼다.",                    "w": {"Log":10, "Dist":6}},
            {"t": "기다리는 시간도 생산적으로 활용하거나 딴 일을 한다.",          "w": {"Agg":10, "Nat":6}},
            {"t": "동행이 있다면 그의 선택을 따른다.",                           "w": {"Sup":12, "Nat":4}},
        ],
    },
    {
        "q": "Q15. 들어주기 어려운 부탁을 거절해야 하는 상황입니다. 당신은?",
        "opts": [
            {"t": "원칙적으로 불가능한 이유를 단호하게 설명한다.",               "w": {"Ord":12, "Log":4}},
            {"t": "최대한 완곡하게 표현해 상대가 상처받지 않게 한다.",            "w": {"Sup":12, "Nat":6}},
            {"t": "논리적으로 이유를 구조화해 상대를 납득시킨다.",                "w": {"Log":12, "Dist":4}},
            {"t": "직접 돕기는 어렵지만 대안이나 다른 사람을 연결해준다.",        "w": {"Nat":10, "Res":6}},
        ],
    },
    {
        "q": "Q16. 내일 중요한 발표나 평가가 있습니다. 오늘 밤 당신은?",
        "opts": [
            {"t": "완벽한 시나리오를 그리며 반복적으로 점검한다.",                "w": {"Ord":12, "Res":6}},
            {"t": "차 한 잔 마시며 심리적으로 안정을 취한다.",                   "w": {"Nat":12, "Dist":4}},
            {"t": "마지막까지 하나라도 더 보완하려고 무섭게 몰입한다.",          "w": {"Agg":10, "Log":6}},
            {"t": "가까운 사람들과 이야기하며 에너지를 얻는다.",                  "w": {"Sup":12, "Nat":4}},
        ],
    },
    {
        "q": "Q17. 어린 시절의 당신은 주로 어떤 아이였나요?",
        "opts": [
            {"t": "예의 바르고 어른 말씀을 잘 따르는 모범적인 아이",              "w": {"Ord":12, "Res":6}},
            {"t": "친구들과 어울리기 좋아하고 정이 넘치는 따뜻한 아이",          "w": {"Sup":10, "Nat":8}},
            {"t": "호기심 많아 무엇이든 직접 해봐야 했던 아이",                  "w": {"Agg":10, "Shd":6}},
            {"t": "혼자 생각에 잠기거나 뭔가를 조용히 관찰하는 아이",            "w": {"Log":10, "Dist":8}},
        ],
    },
    {
        "q": "Q18. 정말 화가 났을 때 당신의 주된 감정 처리 방식은?",
        "opts": [
            {"t": "침묵을 지키며 감정을 가라앉힌 뒤 상황이 지나가길 기다린다.", "w": {"Res":10, "Ord":8}},
            {"t": "서운함을 진솔하게 이야기하고 대화로 풀어낸다.",               "w": {"Sup":10, "Nat":8}},
            {"t": "즉각 표출해 쌓인 감정을 털어내고 뒤끝 없이 끝낸다.",          "w": {"Agg":12, "Dist":-4}},
            {"t": "논리적으로 조목조목 따지며 상대의 논리적 오류를 짚는다.",    "w": {"Log":10, "Shd":8}},
        ],
    },
    {
        "q": "Q19. 당신이 무언가를 가르칠 때 가장 중요하게 생각하는 것은?",
        "opts": [
            {"t": "기본기와 원칙을 먼저 탄탄하게 쌓는 것",                       "w": {"Ord":12, "Log":6}},
            {"t": "스스로 깨달을 때까지 인내심 있게 기다리는 것",                "w": {"Nat":10, "Sup":8}},
            {"t": "일단 현장에 부딪히며 직접 감각을 익히게 하는 것",             "w": {"Agg":12, "Dist":-4}},
            {"t": "핵심 메커니즘을 완벽하게 이해시키는 것",                      "w": {"Log":12, "Shd":4}},
        ],
    },
    {
        "q": "Q20. 하루를 마치고 잠들기 직전, 당신은 무엇을 떠올리나요?",
        "opts": [
            {"t": "오늘 계획한 일들을 완수했는지 체크하며 만족감을 느낀다.",    "w": {"Ord":12, "Res":4}},
            {"t": "만났던 사람들과의 대화나 감정을 되새기며 잠든다.",             "w": {"Sup":10, "Nat":8}},
            {"t": "새로 알게 된 정보나 아직 풀리지 않은 고민을 복기한다.",       "w": {"Log":10, "Shd":6}},
            {"t": "내일의 효율적인 동선과 스케줄을 미리 머릿속에 그린다.",       "w": {"Dist":8,  "Log":8}},
        ],
    },
]

# ============================================================
# 3. 알고리즘 고도화 및 클래스 맵핑
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

EXPECTED_MEANS = {k: 0.0 for k in DIMS}
for q in QUESTIONS:
    for k in DIMS:
        EXPECTED_MEANS[k] += sum(opt["w"].get(k, 0) for opt in q["opts"]) / len(q["opts"])

GLOBAL_SPEC_MEAN = {k: sum(s.get(k, 0) for s in SPECS.values()) / len(SPECS) for k in DIMS}
CLASS_VECS = {}
for cls, specs in CLASS_MAPPING.items():
    CLASS_VECS[cls] = {k: sum(SPECS[s].get(k, 0) for s in specs) / len(specs) for k in DIMS}

def cosine_sim(vec1, vec2):
    dot = sum(vec1[k] * vec2[k] for k in DIMS)
    mag1 = math.sqrt(sum(vec1[k]**2 for k in DIMS)) or 1
    mag2 = math.sqrt(sum(vec2[k]**2 for k in DIMS)) or 1
    return dot / (mag1 * mag2)

def get_class_rankings(u_vec):
    u_centered = {k: u_vec.get(k, 0) - EXPECTED_MEANS[k] for k in DIMS}
    ranks = []
    for cls, c_vec in CLASS_VECS.items():
        c_centered = {k: c_vec.get(k, 0) - GLOBAL_SPEC_MEAN[k] for k in DIMS}
        score = cosine_sim(u_centered, c_centered)
        ranks.append({"name": cls, "score": score})
    return sorted(ranks, key=lambda x: x["score"], reverse=True)

def get_best_spec_for_class(u_vec, cls_name):
    specs_in_cls = CLASS_MAPPING[cls_name]
    best_spec = None
    min_dist = float('inf')
    
    for s in specs_in_cls:
        dist = math.sqrt(sum((u_vec.get(k, 0) - SPECS[s].get(k, 0)) ** 2 for k in DIMS))
        if dist < min_dist:
            min_dist = dist
            best_spec = s
    return best_spec

def radar_svg(u_vec, spec_vec):
    import math as m
    cx, cy, r = 200, 200, 140
    n = len(DIMS)

    def pt(val, idx):
        ang  = m.pi / 2 - 2 * m.pi * idx / n
        norm = (val + 100) / 200 if DIMS[idx] == "Dist" else val / 100
        norm = max(0.0, min(1.0, norm))
        return cx + r * norm * m.cos(ang), cy - r * norm * m.sin(ang)

    grid = "".join(
        f'<polygon points="{" ".join(f"{cx+r*lv*m.cos(m.pi/2-2*m.pi*i/n):.1f},{cy-r*lv*m.sin(m.pi/2-2*m.pi*i/n):.1f}" for i in range(n))}" fill="none" stroke="#334155" stroke-width="1"/>'
        for lv in [0.25, 0.5, 0.75, 1.0]
    )
    axes = "".join(
        f'<line x1="{cx}" y1="{cy}" x2="{cx+r*m.cos(m.pi/2-2*m.pi*i/n):.1f}" y2="{cy-r*m.sin(m.pi/2-2*m.pi*i/n):.1f}" stroke="#475569" stroke-width="1"/>'
        for i in range(n)
    )
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
# 4. 세션 초기화
# ============================================================
if "step" not in st.session_state:
    st.session_state.step     = 0
    st.session_state.u        = {k: 0 for k in DIMS}
    st.session_state.history  = []
    st.session_state.finished = False

# ============================================================
# 5. 페이지 설정 & CSS
# ============================================================
st.set_page_config(page_title="아제로스 영혼 분석", page_icon="⚔️", layout="centered")
st.markdown("""
<style>
    .stButton>button{
        background:#1e293b; color:#e2e8f0;
        border:1px solid #334155; border-radius:8px;
        padding:.6rem 1rem; text-align:left;
        white-space:normal; height:auto; transition:all .2s;
    }
    .stButton>button:hover{background:#6366f1;border-color:#6366f1;color:#fff;}
    .result-card{
        background:linear-gradient(135deg,#1e293b,#0f172a);
        border:1px solid #334155; border-radius:12px;
        padding:1.4rem; margin-bottom:1rem;
    }
    .trait-box{
        background:#1e293b; border-left:3px solid #6366f1;
        border-radius:4px; padding:.6rem 1rem;
        color:#94a3b8; font-size:.88rem; margin:.3rem 0;
    }
    .class-header{ color: #e2e8f0; font-size: 1.8rem; font-weight: bold; margin-bottom: 0.2rem; }
    .spec-header{ color: #f59e0b; font-size: 1.2rem; margin-bottom: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 6. 퀴즈 화면
# ============================================================
if not st.session_state.finished:
    if st.session_state.step >= len(QUESTIONS):
        st.session_state.finished = True
        st.rerun()

    q_data = QUESTIONS[st.session_state.step]

    st.title("⚔️ 아제로스 영혼 정밀 분석")
    st.caption("당신의 일상적인 선택이 아제로스의 직업을 결정합니다.")
    st.divider()
    st.progress(st.session_state.step / len(QUESTIONS),
                text=f"진행: {st.session_state.step} / {len(QUESTIONS)}문항 완료")
    st.write("")
    st.subheader(q_data["q"])
    st.write("")

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

# ============================================================
# 7. 결과 화면
# ============================================================
else:
    u = st.session_state.u
    
    final_classes = get_class_rankings(u)
    top1_cls = final_classes[0]
    top2_cls = final_classes[1]
    
    top1_spec = get_best_spec_for_class(u, top1_cls["name"])
    top2_spec = get_best_spec_for_class(u, top2_cls["name"])

    st.balloons()
    st.title("⚔️ 당신의 아제로스 영혼 분석 결과")
    st.divider()

    st.markdown('<div class="class-header">🥇 추천 직업: <b>{}</b></div>'.format(top1_cls['name']), unsafe_allow_html=True)
    st.markdown('<div class="spec-header">💡 당신을 위한 완벽한 특성: <b>{}</b></div>'.format(top1_spec), unsafe_allow_html=True)
    st.markdown(f'<div class="result-card">{SPEC_DESC.get(top1_spec,"")}</div>', unsafe_allow_html=True)

    st.subheader("📊 나의 성향 vs 추천 전문화 비교")
    st.markdown(radar_svg(u, SPECS[top1_spec]), unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="class-header" style="font-size:1.4rem;">🥈 2위 추천 직업: <b>{}</b></div>'.format(top2_cls['name']), unsafe_allow_html=True)
    st.markdown('<div class="spec-header" style="font-size:1rem; color:#cbd5e1;">💡 대안 추천 특성: <b>{}</b></div>'.format(top2_spec), unsafe_allow_html=True)
    st.markdown(f'<div class="result-card">{SPEC_DESC.get(top2_spec,"")}</div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("🔍 내 성향 요약")
    top_traits = sorted(u.items(), key=lambda x: x[1], reverse=True)[:3]
    for k, _ in top_traits:
        st.markdown(
            f'<div class="trait-box"><strong>{DIM_LABELS[k]}</strong><br>{DIM_RESULT_DESC[k]}</div>',
            unsafe_allow_html=True
        )

    st.divider()
    if st.button("🔄 다시 테스트하기", use_container_width=True):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()
