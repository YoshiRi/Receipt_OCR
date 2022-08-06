# Receipt OCR

Google Vision APIを用いたレシートのOCRとその結果をCSVに変換することを目的としています。


## How to Use


### OCR

下記の設定を済ませる必要があります
https://cloud.google.com/docs/authentication/getting-started#create-service-account-gcloud

```
$ export GOOGLE_APPLICATION_CREDENTIALS=<your json file>
```


```
python main_scan.py <image folder>
```

jsonファイル達が`<image folder>/output/`に出来上がります。

### csv 作成

jsonファイルからcsv形式で必要な情報を抜き出します。

```
python main.py <image folder>/output
```
