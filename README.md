# bocchi-the-radio-reminder

ぼっち・ざ・らじお！のリマインダー

## 開発環境構築

## デプロイ方法

1. 利用する外部ライブラリの圧縮ファイルを作成する

   > :warning: `requirements.txt`の変更がなければスキップ

   ```bash
   sh ./create_zip4layer.sh
   ```

2. Lambda にアップするための圧縮ファイルを作成する

   `{:VERSION}`にバージョン番号を入れる

   ```bash
   sh ./create_zip4function.sh {:VERSION}
   ```

3. AWS コンソールの Lambda からレイヤーを更新する

   > :warning: `requirements.txt`の変更がなければスキップ

4. AWS コンソールの Lambda から関数を更新する

> 参考記事:
>
> https://www.distant-view.co.jp/column/6513/
