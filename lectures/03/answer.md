# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
``` bash
$ uv run python -m app.agent "AIE2026の講座の宿題にある「3レベル」とは何ですか？"
[model] gemini-3.5-flash-lite
AIE2026の宿題における「3レベル」とは、宿題の難易度や取り組み方の構成のことです。

具体的には以下の3つの段階に分かれており、受講生は自分のレベルや目的に合わせて**どれか1つに取り組めばその回の宿題が完了**となります。

1. **基礎**：講義内容の確認
2. **実装**：自分でコードを書く
3. **発展**：調査や試行

なお、宿題は原則として採点されません。

関係する回：第1回
```
- `--trace` で見えたツール呼び出し（ツール名と引数）：
``` bash
$ uv run python -m app.agent --trace "LoRAとQLoRAの違いは？"
[model] gemini-3.5-flash-lite
LoRAとQLoRAの違いは以下の通りです。

* **LoRA**: 事前学習済みの重みを固定したまま、重みの更新分を2つの小さな行列（低ランク行列）で表し、その部分だけを学習するPEFT手法です。学習するパラメータが少なく、メモリや保存容量を節約できます。
* **QLoRA**: LoRAの仕組みをベースにしつつ、**ベースモデルの重みを4ビットなどに量子化（圧縮）**して読み込むことで、さらに大幅なメモリ節約を行う手法です。これにより、より大きなモデルを小さなGPUでも学習・扱うことができるようになります。

関係する回：第2回

--- trace ---
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
[usage] RunUsage(cost=Decimal('0.0008088'), details={'text_prompt_tokens': 1196}, input_text_tokens=1196, input_tokens=1196, output_tokens=180, requests=2, tool_calls=2)
```
- 1つの質問での LLM 呼び出し回数（`requests`）： 2回
- 追加したツールと、docstring に書いた説明：
make_quiz<br>
指定した回の用語から 1つを選び、
    確認問題と答えを返す。

    「第2回の確認問題を出して」のように、
    復習用の問題を求められたときに使う。

## 宿題

- 取り組んだレベル：基礎 / 実装 / 発展
- やったこと：
- 結果：
- 気づき・疑問：
