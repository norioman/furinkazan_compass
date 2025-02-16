import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import qrcode
import io
import urllib.parse
import random

# 共有モードかどうかを判定する
share_mode = False
params = st.query_params
if all(key in params for key in ["wind", "forest", "fire", "mountain"]):
    share_mode = True
    try:
        wind = int(float(params["wind"][0]))
        forest = int(float(params["forest"][0]))
        fire = int(float(params["fire"][0]))
        mountain = int(float(params["mountain"][0]))
        computed_scores = {"風": wind, "林": forest, "火": fire, "山": mountain}
        st.session_state.scores = computed_scores
    except Exception as e:
        st.error("クエリパラメータの読み込みエラー: " + str(e))

# 共有モードの場合はグラフのみ表示して終了
if share_mode:
    st.title("診断結果")
    mode_english = {"風": "Wind", "林": "Forest", "火": "Fire", "山": "Mountain"}
    fixed_order = ["風", "林", "火", "山"]
    computed_scores = st.session_state.scores
    categories = fixed_order
    N = len(categories)
    values = [computed_scores.get(mode, 3) for mode in categories]
    values += values[:1]  # チャートを閉じるために最初の値を追加
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2, linestyle='solid')
    ax.fill(angles, values, alpha=0.25)
    english_labels = [mode_english[mode] for mode in categories]
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(english_labels)
    ax.set_ylim(0, 5)
    ax.set_title("Diagnosis Result", y=1.1)
    st.pyplot(fig)

    # 共有用メッセージの追加
    st.write("### 風林火山モードの役割と特徴")
    st.write("- **風（Wind）**: 迅速で柔軟、アイディアをすぐに実行に移すタイプ。新しいプロジェクトや変化への対応、クリエイティブな発想に優れている人。")
    st.write("- **林（Forest）**: 計画的で組織的、基盤作りやプロセスの整備に長けたタイプ。プロジェクトのスケジュール管理や全体の構造を作る役割に適している人。")
    st.write("- **火（Fire）**: 情熱的でエネルギッシュ、チームに刺激を与え、士気を高めるリーダーシップを発揮するタイプ。変革を推進する原動力となる人。")
    st.write("- **山（Mountain）**: 安定感があり、信念が強い、どんな状況でもぶれずに判断できるタイプ。リスク管理や信頼の拠点となる役割に最適な人。")
    st.write("\nこの診断アプリを使って、メンバーの強みや特性を理解し、チームのバランスを考慮した役割分担をしてみてください。")
    st.stop()

# 以下は通常の診断アプリ（共有モードではない場合に表示）
st.title("風林火山モード診断アプリ")
st.write("この診断は、あなたの思考や行動パターンを「風」「林」「火」「山」の4つのモードに分類し、自己理解およびチーム内の役割理解を深めることを目的としています。")
st.write("各質問に1〜5のスライダーで回答し、あなたの強みや傾向を確認してみてください。")

# 内部的に保持するモードごとの質問リスト
questions_by_mode = {
    "風": [
        "新しいアイデアを思いついたら、すぐ試したくなる",
        "リスクを恐れずに挑戦することが好き",
        "柔軟に物事を進めるのが得意"
    ],
    "林": [
        "物事の進め方を整理して、手順や仕組みを整えるのが好き",
        "計画を立て、着実に実行するのが得意",
        "細かいところまで注意を払える"
    ],
    "火": [
        "自分の仕事に『なぜこれをやるのか』という情熱を持っている",
        "周囲にエネルギーや影響力を与えることができる",
        "積極的に自分の意見を発信する"
    ],
    "山": [
        "長期的な視点で『本当に大事なもの』を考えることが多い",
        "信念を持って行動する",
        "落ち着いて判断し、ぶれない意志がある"
    ]
}

# ランダムな順番の質問リストをセッション状態に保存
if "questions_list" not in st.session_state:
    questions_list = []
    for mode, qs in questions_by_mode.items():
        for i, question in enumerate(qs, start=1):
            questions_list.append({
                "mode": mode,
                "question": question,
                "key": f"{mode}_{i}"
            })
    random.shuffle(questions_list)
    st.session_state.questions_list = questions_list
else:
    questions_list = st.session_state.questions_list

# ランダム順に全ての質問をスライダーで表示（ラベルは質問文のみ）
for idx, item in enumerate(questions_list, start=1):
    st.slider(f"Question {idx}: {item['question']}",
              min_value=1, max_value=5,
              value=st.session_state.get(item["key"], 3),
              step=1, key=item["key"])

# 「診断結果を表示」ボタンで各モードの平均スコアを計算
if st.button("診断結果を表示"):
    scores = {}
    counts = {}
    for item in questions_list:
        mode = item["mode"]
        value = st.session_state.get(item["key"], 3)
        scores[mode] = scores.get(mode, 0) + value
        counts[mode] = counts.get(mode, 0) + 1
    computed_scores = {mode: int(round(scores[mode] / counts[mode])) for mode in scores}
    st.session_state.scores = computed_scores

# スコアがある場合、結果（グラフ、診断、共有ボタン）を表示
if st.session_state.get("scores") is not None:
    computed_scores = st.session_state.scores

    # 固定の順番でグラフを作成（「風」「林」「火」「山」）
    mode_english = {"風": "Wind", "林": "Forest", "火": "Fire", "山": "Mountain"}
    fixed_order = ["風", "林", "火", "山"]
    categories = fixed_order
    N = len(categories)
    values = [computed_scores.get(mode, 3) for mode in categories]
    values += values[:1]
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2, linestyle='solid')
    ax.fill(angles, values, alpha=0.25)
    english_labels = [mode_english[mode] for mode in categories]
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(english_labels)
    ax.set_ylim(0, 5)
    ax.set_title("Diagnosis Result", y=1.1)
    st.pyplot(fig)

    # 診断結果の表示（テキスト）
    max_score = max(computed_scores.values())
    dominant_modes = [mode for mode, score in computed_scores.items() if score == max_score]
    explanations = {
        "Wind": "あなたは風モードです。スピードと行動力があなたの強みです！",
        "Forest": "あなたは林モードです。計画性と基盤づくりに優れていますね！",
        "Fire": "あなたは火モードです。情熱と拡散力が際立っています！",
        "Mountain": "あなたは山モードです。信念と軸の強さが魅力です！"
    }
    st.write("診断結果:")
    if len(dominant_modes) > 1:
        st.write("複数のモードが同率です。")
        for mode in dominant_modes:
            st.write(explanations[mode_english[mode]])
    else:
        dominant_mode = dominant_modes[0]
        st.write(explanations[mode_english[dominant_mode]])
    

    # 結果共有機能（グラフも共有URLも通常のUI内に表示）
    if st.button("結果を共有する"):
        base_url = "https://furinkazancompass.streamlit.app/"  # デプロイ時は実際のURLに変更
        params = {
            "wind": computed_scores["風"],
            "forest": computed_scores["林"],
            "fire": computed_scores["火"],
            "mountain": computed_scores["山"]
        }
        query_string = urllib.parse.urlencode(params)
        share_url = f"{base_url}?{query_string}"
        st.write("下記のURLをコピーして結果を共有できます:")
        st.text_input("Share URL", share_url)
        


        # QRコード生成
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(share_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.image(buf, caption="QR Code for sharing")
