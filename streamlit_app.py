import streamlit as st
import time
import random

# --- 초기 설정 ---
st.set_page_config(page_title="민사재판 마스터: 퀴즈 & 게임", page_icon="⚖️")

# --- 세션 상태 초기화 ---
if 'stage' not in st.session_state:
    st.session_state.stage = 1  # 현재 단계 (1~15)
if 'mode' not in st.session_state:
    st.session_state.mode = 'quiz'  # 현재 모드: 'quiz' 또는 'game'
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_start_time' not in st.session_state:
    st.session_state.game_start_time = None
if 'game_problem' not in st.session_state:
    st.session_state.game_problem = None

# --- 퀴즈 데이터 (민사재판 관련 15문제) ---
quizzes = [
    {"q": "민사소송을 제기하는 사람(소를 제기하는 측)을 무엇이라 부릅니까?", "o": ["원고", "피고", "증인", "판사"], "a": "원고"},
    {"q": "원고가 법원에 제출해야 하는 소송의 첫 번째 서류는 무엇입니까?", "o": ["소장", "답변서", "준비서면", "판결문"], "a": "소장"},
    {"q": "민사재판에서 당사자가 주장하지 않은 사실은 판결의 기초로 삼을 수 없다는 원칙은?", "o": ["변론주의", "직권주의", "공개재판주의", "구술주의"], "a": "변론주의"},
    {"q": "사실의 인정은 반드시 증거에 의해야 한다는 원칙은?", "o": ["증거재판주의", "자유심증주의", "당사자주의", "직권탐지주의"], "a": "증거재판주의"},
    {"q": "제1심 판결에 불복하여 상급 법원에 재판을 신청하는 것을 무엇이라 합니까?", "o": ["항소", "상고", "항고", "재심"], "a": "항소"},
    {"q": "민사소송법상 소송대리인이 될 수 있는 자격이 있는 사람은 원칙적으로 누구입니까?", "o": ["변호사", "법무사", "행정사", "세무사"], "a": "변호사"},
    {"q": "금전 지급을 목적으로 하는 청구에 대해, 법원이 채권자의 신청만으로 채무자에게 지급을 명하는 간이 절차는?", "o": ["지급명령", "조정", "화해", "공탁"], "a": "지급명령"},
    {"q": "소송물 가액이 3,000만 원을 초과하지 않는 사건을 심판하는 간이한 민사절차는?", "o": ["소액사건심판", "가사소송", "행정소송", "형사소송"], "a": "소액사건심판"},
    {"q": "판결이 확정되면 동일한 사건에 대해 다시 소송을 제기할 수 없게 하는 효력은?", "o": ["기판력", "집행력", "형성력", "구속력"], "a": "기판력"},
    {"q": "법률상 원인 없이 타인의 재산이나 노무로 인하여 이익을 얻고, 이로 인해 타인에게 손해를 가한 것을 무엇이라 합니까?", "o": ["부당이득", "불법행위", "채무불이행", "사무관리"], "a": "부당이득"},
    {"q": "고의 또는 과실로 인한 위법행위로 타인에게 손해를 가한 경우 성립하는 것은?", "o": ["불법행위", "채무불이행", "계약위반", "무권대리"], "a": "불법행위"},
    {"q": "채무자가 빚을 갚지 않을 때, 국가의 힘을 빌려 채무자의 재산을 압류하고 매각하는 절차는?", "o": ["강제집행", "보전처분", "가압류", "가처분"], "a": "강제집행"},
    {"q": "금전 채권의 강제집행을 보전하기 위해 미리 채무자의 재산을 동결시켜 두는 제도는?", "o": ["가압류", "가처분", "가등기", "공증"], "a": "가압류"},
    {"q": "권리를 일정 기간 행사하지 않으면 그 권리를 소멸시키는 제도는?", "o": ["소멸시효", "취득시효", "제척기간", "실효"], "a": "소멸시효"},
    {"q": "대법원(3심)에 불복하여 재판을 신청하는 것을 무엇이라 합니까?", "o": ["상고", "항소", "항고", "재심"], "a": "상고"}
]

# --- 게임 생성 로직 ---
def generate_game_problem(stage):
    """단계별로 난이도가 올라가는 산수/논리 문제를 생성합니다."""
    # 난이도 조절: 단계가 높을수록 숫자 범위가 커지고 연산이 복잡해짐
    difficulty = stage
    
    if difficulty <= 5: # 1-5단계: 간단한 덧셈/뺄셈 (제한시간 7초)
        num1 = random.randint(1, 10 + difficulty)
        num2 = random.randint(1, 10 + difficulty)
        op = random.choice(['+', '-'])
        ans = num1 + num2 if op == '+' else num1 - num2
        problem_text = f"{num1} {op} {num2} = ?"
        time_limit = 7
        
    elif difficulty <= 10: # 6-10단계: 곱셈 추가 (제한시간 6초)
        num1 = random.randint(2, 9)
        num2 = random.randint(2, 9 + (difficulty-5))
        op = random.choice(['+', '-', '*'])
        if op == '+': ans = num1 + num2
        elif op == '-': ans = num1 - num2
        else: ans = num1 * num2
        problem_text = f"{num1} {op} {num2} = ?"
        time_limit = 6
        
    else: # 11-15단계: 복합 연산 (제한시간 5초)
        num1 = random.randint(5, 20)
        num2 = random.randint(2, 10)
        num3 = random.randint(1, 10)
        op1 = random.choice(['+', '-', '*'])
        op2 = random.choice(['+', '-'])
        # 식 생성 (괄호 없이 순차 계산이 아니라 파이썬 연산자 우선순위 따름)
        # 헷갈림 방지를 위해 단순 3항 연산
        if op1 == '*': 
            ans = eval(f"{num1} * {num2} {op2} {num3}")
            problem_text = f"{num1} x {num2} {op2} {num3} = ?"
        else:
            ans = eval(f"{num1} {op1} {num2} {op2} {num3}")
            problem_text = f"{num1} {op1} {num2} {op2} {num3} = ?"
        time_limit = 5

    return {"text": problem_text, "answer": ans, "limit": time_limit}

# --- UI 함수 ---
def show_header():
    st.markdown(f"""
    <div style='text-align: center; padding: 10px; background-color: #f0f2f6; border-radius: 10px; margin-bottom: 20px;'>
        <h3>🏛️ 민사재판 마스터 - 단계 {st.session_state.stage}/15</h3>
        <p>현재 점수: {st.session_state.score}점</p>
    </div>
    """, unsafe_allow_html=True)

# --- 1. 퀴즈 화면 ---
def show_quiz():
    show_header()
    idx = st.session_state.stage - 1
    if idx >= len(quizzes):
        st.success("🎉 모든 단계를 완료했습니다! 축하합니다!")
        st.balloons()
        if st.button("처음부터 다시 하기"):
            st.session_state.stage = 1
            st.session_state.score = 0
            st.session_state.mode = 'quiz'
            st.rerun()
        return

    q_data = quizzes[idx]
    
    st.markdown(f"#### Q{st.session_state.stage}. {q_data['q']}")
    
    # 정답 제출 폼
    with st.form(key=f"quiz_form_{st.session_state.stage}"):
        # 라디오 버튼 선택 초기화 방지를 위한 키 관리
        choice = st.radio("정답을 선택하세요:", q_data['o'], index=None)
        submit_btn = st.form_submit_button("제출")
        
    if submit_btn:
        if choice == q_data['a']:
            st.success("정답입니다! ⭕")
            st.info("다음 단계로 넘어가기 위한 미니 게임을 준비합니다...")
            time.sleep(1.5)
            st.session_state.mode = 'game'
            st.session_state.game_problem = None # 게임 문제 초기화
            st.rerun()
        elif choice is None:
            st.warning("보기 중 하나를 선택해주세요.")
        else:
            st.error("오답입니다. ❌ 다시 시도해보세요.")

# --- 2. 게임 화면 ---
def show_game():
    show_header()
    
    st.markdown("### 🎮 스피드 미니 게임!")
    st.markdown("다음 단계로 넘어가려면 제한 시간 내에 문제를 풀어야 합니다.")
    
    # 게임 문제가 없으면 생성
    if st.session_state.game_problem is None:
        st.session_state.game_problem = generate_game_problem(st.session_state.stage)
        st.session_state.game_start_time = time.time() # 타이머 시작

    problem = st.session_state.game_problem
    elapsed_time = time.time() - st.session_state.game_start_time
    remaining_time = problem['limit'] - elapsed_time
    
    # 프로그레스 바 표시
    progress = max(0.0, min(1.0, remaining_time / problem['limit']))
    st.progress(progress)
    
    st.markdown(f"<h1 style='text-align: center; color: #ff4b4b;'>{problem['text']}</h1>", unsafe_allow_html=True)
    st.caption(f"제한 시간: {problem['limit']}초 | 남은 시간: {remaining_time:.1f}초")

    if remaining_time <= 0:
        st.error("⏰ 시간 초과! 게임 실패.")
        if st.button("게임 재도전"):
            st.session_state.game_problem = None # 문제 재생성
            st.session_state.game_start_time = None
            st.rerun()
        return

    # 게임 답안 제출
    with st.form(key=f"game_form_{st.session_state.stage}"):
        user_ans = st.number_input("정답을 입력하세요", value=0, step=1)
        game_submit = st.form_submit_button("확인")
        
    if game_submit:
        # 시간 재확인
        if time.time() - st.session_state.game_start_time > problem['limit']:
            st.error("제출 직전 시간이 초과되었습니다!")
        elif user_ans == problem['answer']:
            st.balloons()
            st.success(f"성공! 🚀 {st.session_state.stage}단계 클리어!")
            time.sleep(1.5)
            st.session_state.stage += 1
            st.session_state.score += 10
            st.session_state.mode = 'quiz'
            st.session_state.game_problem = None
            st.rerun()
        else:
            st.error(f"틀렸습니다! 정답은 {problem['answer']} 입니다. 다시 도전하세요.")
            # 틀리면 즉시 재시작 버튼 유도
            if st.button("다시 도전"):
                st.session_state.game_problem = None
                st.rerun()

    # 실시간 타이머 갱신을 위해 rerun (1초 미만 간격은 성능 이슈가 있을 수 있으나 게임감을 위해)
    time.sleep(0.1) 
    st.rerun()

# --- 메인 로직 분기 ---
def main():
    if st.session_state.mode == 'quiz':
        show_quiz()
    elif st.session_state.mode == 'game':
        show_game()

if __name__ == "__main__":
    main()
