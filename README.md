# 風林火山コンパス (Furinkazan Compass)

## 🧭 プロジェクト概要
風林火山コンパスは、ユーザーの思考や行動パターンを「風・林・火・山」の4つのモードに分類し、自己理解とチーム内の役割理解を深めるための診断アプリです。

## 🌐 アプリURL
[風林火山コンパス](https://furinkazancompass.streamlit.app/)

## 🎯 診断モードと役割
- **風（Wind）**: 迅速で柔軟。アイディアを即座に実行するタイプ。新規プロジェクトやクリエイティブ業務に適任。
- **林（Forest）**: 計画的で組織的。基盤づくりやプロセス整備に長けるタイプ。プロジェクト管理が得意。
- **火（Fire）**: 情熱的でエネルギッシュ。周囲を鼓舞するリーダーシップを発揮するタイプ。推進力が必要な業務に最適。
- **山（Mountain）**: 安定感と信念があるタイプ。リスク管理や方針決定の軸となる存在。

## 🚀 使い方
1. [アプリURL](https://furinkazancompass.streamlit.app/) にアクセス。
2. 質問に対してスライダーで回答。
3. 「診断結果を表示」ボタンをクリック。
4. 診断結果とともに、あなたのモードが表示されます。
5. 「結果を共有する」ボタンで共有用URLとQRコードを取得可能。

## 🛠️ 技術スタック
- 言語: Python
- フレームワーク: Streamlit
- グラフ描画: Matplotlib
- QRコード生成: qrcode

## 🧑‍💻 ローカル開発手順
```bash
# リポジトリをクローン
git clone https://github.com/norioman/furinkazan_compass.git
cd furinkazan_compass

# 仮想環境の作成と有効化
python3 -m venv venv
source venv/bin/activate

# 必要なパッケージをインストール
pip install -r requirements.txt

# アプリの起動
streamlit run app.py
```

## 🧾 必要なファイル
- `app.py`: アプリケーションのメインコード
- `requirements.txt`: 依存ライブラリのリスト

## 📜 ライセンス
MIT License

---

**このアプリは、風林火山の知恵を活かして、チームの可能性を最大化するために作成されました。**

