import streamlit as st
import pandas as pd
import random
from gtts import gTTS
import io

# 데이터 불러오기
df = pd.read_csv("bringen.csv", encoding="cp949").dropna(subset=["Meaning", "German"])
    
# 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
if "current_word" not in st.session_state:
    st.session_state.current_word = random.choice(df.to_dict(orient="records"))
if "feedback" not in st.session_state:
    st.session_state.feedback = ""
if "direction" not in st.session_state:
    # True: 한<->독, False: 독<->한
    st.session_state.direction = True

# 현재 문제
word = st.session_state.current_word

# 문제 표시
if st.session_state.direction:
    st.write(f"korean meaning: {word['Meaning']}")
    answer = st.text_input("in german:", key="answer_input")
else:
    st.write(f"german meaning: {word['German']}")
    answer = st.text_input("in korean:", key="answer_input")
    

# 정답 확인 함수
def check_answer():
    user_answer = str(st.session_state["answer_input"]).strip().lower()
    
    if st.session_state.direction:
        correct = str(word["German"]).strip().lower()
    else:
        correct = str(word["Meaning"]).strip().lower()

    if str(answer).strip().lower() == correct:
        st.session_state.feedback = "Good!"
        st.session_state.score += 1
    else:
        st.session_state.feedback = f"Nope! the answer is {correct}"

    # 새로운 문제와 랜덤 방향 설정
    st.session_state.current_word = random.choice(df.to_dict(orient="records"))
    st.session_state.direction = random.choice([True, False])
    st.session_state["answer_input"] = "" # 입력창 초기화

st.button("check", on_click=check_answer)

# 발음 듣기 기능 (독일어 문제 단어만)
tts = gTTS(str(word["German"]), lang="de")
mp3_fp = io.BytesIO()
tts.write_to_fp(mp3_fp)
st.audio(mp3_fp.getvalue(), format="audio/mp3")


# 결과와 점수 출력
st.write(st.session_state.feedback)
st.write(f"score: {st.session_state.score}")





