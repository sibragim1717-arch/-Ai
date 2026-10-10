
import json
import random
import time
import datetime as dt

import requests
import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# LinguaQuest — языковая игра
# ============================================================

st.set_page_config(
    page_title="LinguaQuest",
    page_icon="🦊",
    layout="centered",
)

LANGUAGES = ["en", "ru", "uz", "fr", "de", "zh"]

NAME = {
    "en": "English 🇬🇧",
    "ru": "Русский 🇷🇺",
    "uz": "O'zbek 🇺🇿",
    "fr": "Français 🇫🇷",
    "de": "Deutsch 🇩🇪",
    "zh": "中文 🇨🇳",
}

VOICE = {
    "en": "en-US",
    "ru": "ru-RU",
    "uz": "uz-UZ",
    "fr": "fr-FR",
    "de": "de-DE",
    "zh": "zh-CN",
}


def parse(text):
    """Преобразует словарь в список строк."""
    return [
        line.split("|")
        for line in text.strip().splitlines()
        if line.strip()
    ]


# Порядок языков: английский | русский | узбекский |
# французский | немецкий | китайский

WORDS = {
    1: parse("""
hello|привет|salom|bonjour|hallo|你好
thank you|спасибо|rahmat|merci|danke|谢谢
yes|да|ha|oui|ja|是
no|нет|yo'q|non|nein|不
water|вода|suv|eau|Wasser|水
bread|хлеб|non|pain|Brot|面包
house|дом|uy|maison|Haus|房子
cat|кот|mushuk|chat|Katze|猫
dog|собака|it|chien|Hund|狗
mother|мама|ona|mère|Mutter|妈妈
father|папа|ota|père|Vater|爸爸
friend|друг|do'st|ami|Freund|朋友
one|один|bir|un|eins|一
two|два|ikki|deux|zwei|二
red|красный|qizil|rouge|rot|红色
blue|синий|ko'k|bleu|blau|蓝色
"""),
    2: parse("""
book|книга|kitob|livre|Buch|书
sun|солнце|quyosh|soleil|Sonne|太阳
city|город|shahar|ville|Stadt|城市
apple|яблоко|olma|pomme|Apfel|苹果
school|школа|maktab|école|Schule|学校
car|машина|mashina|voiture|Auto|汽车
tea|чай|choy|thé|Tee|茶
morning|утро|ertalab|matin|Morgen|早上
night|ночь|tun|nuit|Nacht|夜晚
love|любовь|sevgi|amour|Liebe|爱
milk|молоко|sut|lait|Milch|牛奶
fish|рыба|baliq|poisson|Fisch|鱼
table|стол|stol|table|Tisch|桌子
door|дверь|eshik|porte|Tür|门
money|деньги|pul|argent|Geld|钱
time|время|vaqt|temps|Zeit|时间
"""),
    3: parse("""
I love you|Я люблю тебя|Men seni sevaman|Je t'aime|Ich liebe dich|我爱你
How are you?|Как дела?|Ishlaringiz qalay?|Comment ça va ?|Wie geht's?|你好吗？
I am hungry|Я голоден|Men ochman|J'ai faim|Ich habe Hunger|我饿了
I want water|Я хочу воды|Men suv xohlayman|Je veux de l'eau|Ich will Wasser|我想喝水
What is your name?|Как тебя зовут?|Ismingiz nima?|Comment tu t'appelles ?|Wie heißt du ?|你叫什么名字？
Where is the station?|Где вокзал?|Vokzal qayerda?|Où est la gare ?|Wo ist der Bahnhof ?|车站在哪里？
See you tomorrow|До завтра|Ertagacha|À demain|Bis morgen|明天见
Thank you very much|Большое спасибо|Katta rahmat|Merci beaucoup|Vielen Dank|非常感谢
I don't understand|Я не понимаю|Men tushunmayapman|Je ne comprends pas|Ich verstehe nicht|我不明白
How much is this?|Сколько это стоит?|Bu qancha turadi?|Combien ça coûte ?|Wie viel kostet das ?|这个多少钱？
Can you help me?|Вы можете мне помочь?|Menga yordam bera olasizmi?|Pouvez-vous m'aider ?|Können Sie mir helfen ?|你能帮我吗？
Good night|Спокойной ночи|Xayrli tun|Bonne nuit|Gute Nacht|晚安
"""),
}

LEVEL_NAMES = {
    "ru": ["Лёгкий 🌱", "Средний 🔥", "Сложный 💎"],
    "uz": ["Oson 🌱", "O'rta 🔥", "Qiyin 💎"],
    "en": ["Easy 🌱", "Medium 🔥", "Hard 💎"],
}

TEXTS = {
    "play": ("Играть", "O'ynash", "Play"),
    "cards": ("Карточки", "Kartochkalar", "Cards"),
    "tutor": ("ИИ-тьютор", "AI ustoz", "AI Tutor"),
    "league": ("Лига", "Liga", "League"),
    "me": ("Профиль", "Profil", "Profile"),
    "level": ("Уровень сложности", "Qiyinlik darajasi", "Difficulty"),
    "start": ("Начать урок", "Darsni boshlash", "Start lesson"),
    "check": ("Проверить", "Tekshirish", "Check"),
    "next": ("Дальше", "Keyingi", "Next"),
    "ok": ("Верно!", "To'g'ri!", "Correct!"),
    "bad": ("Правильный ответ", "To'g'ri javob", "Correct answer"),
    "tn": ("Переведи", "Tarjima qil", "Translate"),
    "nt": ("Переведи", "Tarjima qil", "Translate"),
    "ls": (
        "Послушай и выбери перевод",
        "Eshit va tarjimasini tanla",
        "Listen and pick the translation",
    ),
    "ty": ("Напиши перевод", "Tarjimani yoz", "Type the translation"),
    "bd": ("Составь перевод", "Tarjimani tuz", "Build the translation"),
    "clear": ("Очистить", "Tozalash", "Clear"),
    "done": ("Урок пройден!", "Dars tugadi!", "Lesson complete!"),
    "perf": ("Без ошибок! +20 XP", "Xatosiz! +20 XP", "Perfect! +20 XP"),
    "nohp": (
        "Сердца закончились 💔 Подождите 10 минут "
        "или восстановите за 20 💎",
        "Yuraklar tugadi 💔 10 daqiqa kuting "
        "yoki 20 💎 ga tiklang",
        "Out of hearts 💔 Wait or refill for 20 💎",
    ),
    "refill": ("Восстановить ❤️", "❤️ tiklash", "Refill ❤️"),
    "nat": ("Я говорю на", "Men so'zlashaman", "I speak"),
    "lrn": ("Хочу выучить", "O'rganmoqchiman", "I want to learn"),
    "reset": ("Сбросить прогресс", "Jarayonni o'chirish", "Reset progress"),
    "flip": ("Показать перевод", "Tarjimani ko'rsat", "Show translation"),
    "ph": ("Спроси что угодно…", "Xohlagan narsani so'ra…", "Ask anything…"),
    "nokey": (
        "Введите API-ключ Anthropic в боковой панели.",
        "Anthropic API kalitini yon panelga kiriting.",
        "Enter your Anthropic API key in the sidebar.",
    ),
    "hello": (
        "Привет! Я твой ИИ-тьютор. Объясню грамматику, "
        "проверю фразу и проведу викторину. С чего начнём?",
        "Salom! Men AI ustozingman. Grammatikani tushuntiraman, "
        "iboralarni tekshiraman va viktorina o'tkazaman. "
        "Nimadan boshlaymiz?",
        "Hi! I'm your AI tutor. I can explain grammar, "
        "check phrases and run quizzes. Where shall we start?",
    ),
    "lv": ("Уровень", "Daraja", "Level"),
    "you": ("Вы", "Siz", "You"),
    "back": ("К урокам", "Darslarga", "Back to lessons"),
}

CHIPS = {
    "ru": ["Объясни грамматику", "Мини-диалог", "Викторина"],
    "uz": ["Grammatikani tushuntir", "Mini-dialog", "Viktorina"],
    "en": ["Explain grammar", "Mini dialogue", "Quiz me"],
}


# ============================================================
# Состояние приложения
# ============================================================

S = st.session_state

DEFAULTS = {
    "ui": "",
    "tl": "",
    "xp": 0,
    "gems": 30,
    "streak": 0,
    "last": "",
    "hearts": 5,
    "heart_time": 0.0,
    "weekly_xp": 0,
    "total_lessons": 0,
    "perfect_lessons": 0,
    "questions": None,
    "question_index": 0,
    "feedback": None,
    "lesson_xp": 0,
    "mistakes": 0,
    "combo": 0,
    "build": [],
    "chat": [],
    "card_index": 0,
    "result": None,
}

for key, value in DEFAULTS.items():
    S.setdefault(key, value)


def tr(key):
    """Перевод интерфейса на язык пользователя."""
    ui = S.ui or "ru"
    return TEXTS[key][["ru", "uz", "en"].index(ui)]


def sync_hearts():
    """Восстанавливает одно сердце каждые 10 минут."""
    if S.hearts >= 5:
        return

    if not S.heart_time:
        S.heart_time = time.time()
        return

    elapsed = int((time.time() - S.heart_time) // 600)

    if elapsed > 0:
        S.hearts = min(5, S.hearts + elapsed)

        if S.hearts >= 5:
            S.heart_time = 0.0
        else:
            S.heart_time += elapsed * 600


# ============================================================
# Оформление
# ============================================================

st.markdown(
    """
    <style>
    .stButton > button[kind="primary"] {
        background: #58cc02 !important;
        color: white !important;
        border: none !important;
        border-bottom: 4px solid #3f9a00 !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
    }
    .title {
        font-size: 34px;
        font-weight: 900;
        background: linear-gradient(90deg, #58cc02, #1cb0f6, #a560ff);
        -webkit-background-clip: text;
        color: transparent;
        margin-bottom: 15px;
    }
    .big {
        font-size: 28px;
        font-weight: 800;
        text-align: center;
        padding: 18px 10px;
        border: 2px solid #6574cd;
        border-radius: 18px;
        margin: 8px 0 16px 0;
        overflow-wrap: anywhere;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def header():
    st.markdown(
        '<div class="title">🦊 LinguaQuest</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# Первый запуск
# ============================================================

if not (S.ui and S.tl):
    header()

    ui = st.radio(
        "Я говорю на / Men so'zlashaman / I speak",
        ["ru", "uz", "en"],
        format_func=lambda x: NAME[x],
        horizontal=True,
    )

    available = [
        lang for lang in LANGUAGES
        if lang != ui
    ]

    tl = st.radio(
        "Хочу выучить / O'rganmoqchiman / I want to learn",
        available,
        format_func=lambda x: NAME[x],
        horizontal=True,
    )

    if st.button(
        "▶ Start",
        type="primary",
        use_container_width=True,
    ):
        S.ui = ui
        S.tl = tl
        st.rerun()

    st.stop()


sync_hearts()

NATIVE_INDEX = LANGUAGES.index(S.ui)
TARGET_INDEX = LANGUAGES.index(S.tl)


# ============================================================
# Озвучивание слов через браузер
# ============================================================

def speak(text, lang):
    safe_text = json.dumps(text, ensure_ascii=False)
    safe_text = safe_text.replace("</", "<\\/")

    html = f"""
    <button
        style="
            font-size:18px;
            padding:9px 18px;
            border-radius:12px;
            border:0;
            background:#1cb0f6;
            color:white;
            cursor:pointer;
        "
        onclick="speakWord()">
        🔊 Прослушать
    </button>

    <script>
    function speakWord() {{
        if (!('speechSynthesis' in window)) {{
            alert('Speech synthesis is not supported.');
            return;
        }}

        const utterance = new SpeechSynthesisUtterance({safe_text});
        utterance.lang = '{VOICE[lang]}';

        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utterance);
    }}
    </script>
    """

    components.html(html, height=55)


# ============================================================
# Генератор заданий
# ============================================================

def tokenize(text):
    if S.tl == "zh":
        return list(text.replace(" ", ""))
    return text.split()


def make_options(pool, correct, column):
    """Создаёт варианты ответов без повторяющихся значений."""
    wrong = list(dict.fromkeys(
        row[column]
        for row in pool
        if row[column] != correct
    ))

    count = min(3, len(wrong))
    options = random.sample(wrong, count)
    options.append(correct)
    random.shuffle(options)

    return options


def make_lesson(level):
    pool = WORDS[level]
    questions = []

    selected = random.sample(
        pool,
        min(8, len(pool)),
    )

    for word in selected:
        if level == 1:
            kind = random.choice(["tn", "nt"])
        elif level == 2:
            kind = random.choice(["tn", "nt", "ls", "ty"])
        else:
            kind = random.choice(["bd", "tn"])

        if kind == "ty" and S.tl == "zh":
            kind = "nt"

        if kind == "tn":
            questions.append({
                "kind": kind,
                "prompt": word[TARGET_INDEX],
                "answer": word[NATIVE_INDEX],
                "options": make_options(
                    pool, word[NATIVE_INDEX], NATIVE_INDEX
                ),
            })

        elif kind == "nt":
            questions.append({
                "kind": kind,
                "prompt": word[NATIVE_INDEX],
                "answer": word[TARGET_INDEX],
                "options": make_options(
                    pool, word[TARGET_INDEX], TARGET_INDEX
                ),
            })

        elif kind == "ls":
            questions.append({
                "kind": kind,
                "say": word[TARGET_INDEX],
                "answer": word[NATIVE_INDEX],
                "options": make_options(
                    pool, word[NATIVE_INDEX], NATIVE_INDEX
                ),
            })

        elif kind == "ty":
            questions.append({
                "kind": kind,
                "prompt": word[NATIVE_INDEX],
                "answer": word[TARGET_INDEX],
                "say": word[TARGET_INDEX],
            })

        elif kind == "bd":
            answer_tokens = tokenize(word[TARGET_INDEX])

            other_tokens = list(dict.fromkeys(
                token
                for row in pool
                if row is not word
                for token in tokenize(row[TARGET_INDEX])
                if token not in answer_tokens
            ))

            extra_count = min(3, len(other_tokens))
            extras = random.sample(
                other_tokens,
                extra_count,
            )

            word_pool = answer_tokens + extras
            random.shuffle(word_pool)

            questions.append({
                "kind": kind,
                "prompt": word[NATIVE_INDEX],
                "answer": answer_tokens,
                "say": word[TARGET_INDEX],
                "pool": word_pool,
            })

    return questions


def normalize(text):
    """Нормализует ответ для проверки."""
    text = text.lower().strip()

    for char in ".,!?¿¡'’":
        text = text.replace(char, "")

    return " ".join(text.split())


# ============================================================
# Проверка ответов и награды
# ============================================================

def grade(correct, answer):
    S.feedback = (bool(correct), answer)

    if correct:
        S.combo += 1
        S.lesson_xp += 10 + (5 if S.combo >= 3 else 0)
    else:
        S.combo = 0
        S.mistakes += 1

        if S.hearts > 0:
            if S.hearts == 5:
                S.heart_time = time.time()

            S.hearts -= 1

    st.rerun()


def award():
    lesson_xp = S.lesson_xp

    if S.mistakes == 0:
        lesson_xp += 20

    gems = 5 + (5 if S.mistakes == 0 else 0)

    today = dt.date.today()
    today_str = str(today)
    yesterday_str = str(today - dt.timedelta(days=1))

    if S.last != today_str:
        if S.last == yesterday_str:
            S.streak += 1
        else:
            S.streak = 1

        S.last = today_str

    S.xp += lesson_xp
    S.weekly_xp += lesson_xp
    S.gems += gems
    S.total_lessons += 1

    if S.mistakes == 0:
        S.perfect_lessons += 1

    S.result = (
        lesson_xp,
        gems,
        S.mistakes == 0,
    )


# ============================================================
# Уроки
# ============================================================

def lesson():
    if S.hearts <= 0 and S.feedback is None:
        st.error(tr("nohp"))

        if S.gems >= 20 and st.button(tr("refill")):
            S.gems -= 20
            S.hearts = 5
            S.heart_time = 0.0
            S.questions = None
            st.rerun()

        return

    if S.questions is None:
        level = st.radio(
            tr("level"),
            [1, 2, 3],
            format_func=lambda value: LEVEL_NAMES[S.ui][value - 1],
            horizontal=True,
        )

        if st.button(
            tr("start"),
            type="primary",
            use_container_width=True,
        ):
            S.questions = make_lesson(level)
            S.question_index = 0
            S.feedback = None
            S.lesson_xp = 0
            S.mistakes = 0
            S.combo = 0
            S.build = []
            S.result = None
            st.rerun()

        return

    if S.question_index >= len(S.questions):
        if S.result is None:
            award()

        xp, gems, perfect = S.result

        st.balloons()
        st.success(tr("done"))

        if perfect:
            st.info(tr("perf"))

        columns = st.columns(3)
        columns[0].metric("⭐ XP", f"+{xp}")
        columns[1].metric("💎", f"+{gems}")
        columns[2].metric("🔥", S.streak)

        if st.button(
            tr("back"),
            type="primary",
            use_container_width=True,
        ):
            S.questions = None
            S.result = None
            st.rerun()

        return

    question = S.questions[S.question_index]

    st.progress(
        S.question_index / len(S.questions),
        text=f"{S.question_index + 1} / {len(S.questions)}",
    )

    if S.combo >= 2:
        st.caption(f"🔥 Combo x{S.combo}")

    st.subheader(tr(question["kind"]))

    kind = question["kind"]

    if kind == "ls":
        st.write(tr("ls"))
        speak(question["say"], S.tl)

    elif kind != "bd":
        st.markdown(
            f"<div class='big'>{question['prompt']}</div>",
            unsafe_allow_html=True,
        )

    if S.feedback is None:

        if kind in ("tn", "nt", "ls"):
            choice = st.radio(
                "answer",
                question["options"],
                index=None,
                key=f"answer_{S.question_index}",
                label_visibility="collapsed",
            )

            if st.button(
                tr("check"),
                disabled=choice is None,
                type="primary",
                use_container_width=True,
            ):
                grade(
                    choice == question["answer"],
                    question["answer"],
                )

        elif kind == "ty":
            typed = st.text_input(
                "answer",
                key=f"typed_{S.question_index}",
                label_visibility="collapsed",
            )

            if st.button(
                tr("check"),
                disabled=not typed.strip(),
                type="primary",
                use_container_width=True,
            ):
                grade(
                    normalize(typed) == normalize(question["answer"]),
                    question["answer"],
                )

        elif kind == "bd":
            separator = "" if S.tl == "zh" else " "

            st.markdown(
                f"<div class='big'>{question['prompt']}</div>",
                unsafe_allow_html=True,
            )

            assembled = separator.join(
                question["pool"][i] for i in S.build
            )

            st.info(assembled or "…")

            columns = st.columns(3)

            for index, token in enumerate(question["pool"]):
                if index in S.build:
                    continue

                if columns[index % 3].button(
                    token,
                    key=f"word_{S.question_index}_{index}",
                ):
                    S.build.append(index)
                    st.rerun()

            left, right = st.columns(2)

            if left.button(tr("clear")):
                S.build = []
                st.rerun()

            if right.button(
                tr("check"),
                disabled=not S.build,
                type="primary",
            ):
                built_tokens = [
                    question["pool"][i] for i in S.build
                ]

                grade(
                    built_tokens == question["answer"],
                    separator.join(question["answer"]),
                )

    else:
        correct, answer = S.feedback

        if question.get("say"):
            speak(question["say"], S.tl)

        if correct:
            st.success("✅ " + tr("ok"))
        else:
            st.error(f"❌ {tr('bad')}: {answer}")

        if st.button(
            tr("next"),
            type="primary",
            use_container_width=True,
        ):
            S.question_index += 1
            S.feedback = None
            S.build = []

            if S.question_index >= len(S.questions):
                award()

            st.rerun()


# ============================================================
# Карточки
# ============================================================

def cards():
    level = st.radio(
        tr("level"),
        [1, 2, 3],
        format_func=lambda value: LEVEL_NAMES[S.ui][value - 1],
        horizontal=True,
        key="card_level",
    )

    pool = WORDS[level]
    S.card_index %= len(pool)

    word = pool[S.card_index]

    st.markdown(
        f"<div class='big'>{word[TARGET_INDEX]}</div>",
        unsafe_allow_html=True,
    )

    speak(word[TARGET_INDEX], S.tl)

    if st.toggle(
        tr("flip"),
        key=f"flip_{level}_{S.card_index}",
    ):
        st.markdown(
            f"<div class='big'>{word[NATIVE_INDEX]}</div>",
            unsafe_allow_html=True,
        )

    columns = st.columns(3)

    if columns[0].button("⬅️"):
        S.card_index = (S.card_index - 1) % len(pool)
        st.rerun()

    if columns[1].button("🔀"):
        S.card_index = random.randrange(len(pool))
        st.rerun()

    if columns[2].button("➡️"):
        S.card_index = (S.card_index + 1) % len(pool)
        st.rerun()


# ============================================================
# ИИ-тьютор Claude
# ============================================================

def claude(messages, api_key):
    system_prompt = (
        "You are a friendly, concise language tutor inside a learning game. "
        f"The learner speaks {NAME[S.ui]} and is learning {NAME[S.tl]}. "
        f"Reply primarily in {NAME[S.ui]}. Use {NAME[S.tl]} for examples "
        "and provide translations. Keep replies under approximately 150 words. "
        "Use clear explanations, practical examples, and occasional emojis. "
        "End with a short question or mini-exercise."
    )

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 600,
            "system": system_prompt,
            "messages": messages,
        },
        timeout=60,
    )

    if not response.ok:
        try:
            detail = response.json().get("error", {}).get(
                "message", response.text
            )
        except (ValueError, AttributeError):
            detail = response.text

        raise RuntimeError(
            f"Anthropic API error {response.status_code}: {detail}"
        )

    data = response.json()

    return "".join(
        item.get("text", "")
        for item in data.get("content", [])
        if item.get("type") == "text"
    ).strip()


def tutor():
    st.sidebar.subheader("🤖 AI Tutor")

    api_key = st.sidebar.text_input(
        "Anthropic API key",
        type="password",
        help="Ключ можно получить в консоли Anthropic.",
    )

    if not api_key:
        try:
            api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        except Exception:
            api_key = ""

    with st.chat_message("assistant"):
        st.write(tr("hello"))

    for message in S.chat:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    columns = st.columns(3)
    prompt = None

    for index, column in enumerate(columns):
        if column.button(
            CHIPS[S.ui][index],
            key=f"chip_{index}",
        ):
            prompt = CHIPS[S.ui][index]

    typed_prompt = st.chat_input(tr("ph"))

    if typed_prompt:
        prompt = typed_prompt

    if not prompt:
        return

    if not api_key:
        st.warning(tr("nokey"))
        return

    S.chat.append({
        "role": "user",
        "content": prompt,
    })

    try:
        with st.spinner("🤖 ..."):
            answer = claude(S.chat, api_key)

        if not answer:
            answer = "Не удалось получить текстовый ответ. Попробуйте ещё раз."

    except requests.Timeout:
        answer = "Сервер отвечает слишком долго. Попробуйте ещё раз."

    except requests.RequestException:
        answer = "Ошибка соединения. Проверьте интернет и попробуйте снова."

    except Exception as error:
        answer = f"Не удалось получить ответ: {error}"

    S.chat.append({
        "role": "assistant",
        "content": answer,
    })

    st.rerun()


# ============================================================
# Лига
# ============================================================

def league():
    bots = [
        ("Alisher", 380),
        ("Anna", 320),
        ("Li Wei", 270),
        ("Pierre", 220),
        ("Mia", 170),
        ("Timur", 130),
        ("Jack", 90),
        ("Sofia", 60),
        ("Dilnoza", 30),
    ]

    rows = bots + [(tr("you"), S.weekly_xp)]
    rows.sort(key=lambda row: -row[1])

    for index, (name, xp) in enumerate(rows):
        if index == 0:
            medal = "🥇"
        elif index == 1:
            medal = "🥈"
        elif index == 2:
            medal = "🥉"
        else:
            medal = f"{index + 1}."

        line = f"{medal} **{name}** — {xp} XP"

        if name == tr("you"):
            st.success(line)
        else:
            st.markdown(line)


# ============================================================
# Профиль
# ============================================================

def profile():
    st.progress(
        (S.xp % 100) / 100,
        text=f"{tr('lv')} {S.xp // 100 + 1} · {S.xp} XP",
    )

    badges = [
        (S.streak >= 3, "🔥 3 days"),
        (S.xp >= 100, "⭐ 100 XP"),
        (S.perfect_lessons > 0, "💯 Perfect"),
        (S.total_lessons >= 5, "📚 5 lessons"),
    ]

    st.write(
        " ".join(
            f"`{badge}`" if earned else f"~~{badge}~~"
            for earned, badge in badges
        )
    )

    ui = st.radio(
        tr("nat"),
        ["ru", "uz", "en"],
        index=["ru", "uz", "en"].index(S.ui),
        format_func=lambda lang: NAME[lang],
        horizontal=True,
    )

    available = [
        lang for lang in LANGUAGES
        if lang != ui
    ]

    tl = st.radio(
        tr("lrn"),
        available,
        index=available.index(S.tl) if S.tl in available else 0,
        format_func=lambda lang: NAME[lang],
        horizontal=True,
    )

    if (ui, tl) != (S.ui, S.tl):
        S.ui = ui
        S.tl = tl
        S.questions = None
        S.feedback = None
        S.result = None
        S.chat = []
        S.build = []
        st.rerun()

    if S.hearts < 5 and S.gems >= 20:
        if st.button(tr("refill") + " (20 💎)"):
            S.gems -= 20
            S.hearts = 5
            S.heart_time = 0.0
            st.rerun()

    if st.button(tr("reset")):
        for key in list(S.keys()):
            del S[key]
        st.rerun()


# ============================================================
# Главный экран
# ============================================================

header()

columns = st.columns(4)
columns[0].metric("🔥", S.streak)
columns[1].metric("💎", S.gems)
columns[2].metric("❤️", S.hearts)
columns[3].metric("⭐ XP", S.xp)

tabs = st.tabs([
    f"🎮 {tr('play')}",
    f"🃏 {tr('cards')}",
    f"🤖 {tr('tutor')}",
    f"🏆 {tr('league')}",
    f"👤 {tr('me')}",
])

functions = [
    lesson,
    cards,
    tutor,
    league,
    profile,
]

for tab, function in zip(tabs, functions):
    with tab:
        function()
