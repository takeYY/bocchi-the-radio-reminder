# ==================================================
# AWS Lambda Layer用にzipファイルを作成するコマンド
# ==================================================

# 利用するライブラリを python ディレクトリに追加
mkdir python
pip3 install -r requirements.txt -t ./python

# 追加したライブラリを zip で圧縮
zip -r layer.zip ./python
