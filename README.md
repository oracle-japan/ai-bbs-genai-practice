# Oracle AI Brown Bag Seminar - OCI Generative AI Service 実践編

Oracle AI Brown Bag Seminar #7 OCI Generative AI Service 実践編で使用したサンプルコードです。

```sh
.
├── README.md
├── app
│   ├── ai_vector_search.py
│   ├── auth.py
│   ├── generative_ai_agents.py
│   ├── generative_ai.py
│   └── main.py
├── notebooks
│   ├── .env-template
│   ├── 01_getting_started_generative_ai_with_sdk.ipynb
│   ├── 02_getting_started_generative_ai_with_langchain.ipynb
│   ├── 03_getting_started_generative_ai_agents.ipynb
│   └── 04_getting_started_oracle_database_23c_ai_vector_search.ipynb
└── requirements.txt
```

## Prerequired

- OCI Search Service with OpenSearch, OCI Cache with Redis が作成可能なネットワークリソースが作成済みであること
- OCI Search Service with OpenSearch v2.3.0+ がプロビジョニング済みであること
- OCI Cache with Redis がプロビジョニング済みであること
- OCI Search Service with OpenSearch にアクセス可能な Compute インスタンスがプロビジョニング済みであること

### OpenSearch に対するセキュリティ設定

`settings/opensearch.http` に記載されている内容を順番に実行してください。`settings/parameters` は自身の環境に合わせて適宜修正してください。

## Notebooks

`.env-template` をコピーし、`.env` を作成してください。内容は、ご自身の環境に合わせて適宜修正してください。

## App

`.env-template` をコピーし、`.env` を作成してください。内容は、ご自身の環境に合わせて適宜修正してください。

アプリケーションを実行します。

```sh
streamlit run main.py
```

実行すると、以下のようにログが出力されます。

```sh
Collecting usage statistics. To deactivate, set browser.gatherUsageStats to False.


  You can now view your Streamlit app in your browser.

  Network URL: http://<private-ip>:8502
  External URL: http://<public-ip>:8502
```

ブラウザを参照すると、以下のようなアプリケーションが起動されます。

![application](./img/application.png)

OCI のサービスについて確認すると、以下のように表示されます。

![prompt-completion](./img/prompt-completion.png)
