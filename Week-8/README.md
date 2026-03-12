# Week-8 — LLM Fine-Tuning, Quantisation & Optimised Inference

> **Model training was done on Google Colab.**
> Adapter weights and quantized models are large files — they are **not pushed to Git**.
> They are saved to and loaded from **Google Drive**, mounted in Colab at runtime.

---

## Repository Structure

```
WEEK-8/
│
├── Day-1/
│   ├── data/
│   │   ├── train.jsonl
│   │   ├── val.jsonl
│   │   └── test.jsonl
│   ├── utils/
│   ├── images/
│   └── DATASET-ANALYSIS.md
│
├── Day-2/
│   ├── adapters/           ← saved to Google Drive (not in git)
│   ├── lora_train.ipynb    ← training run on Colab
│   └── TRAINING-REPORT.md
│
├── Day-3/
│   ├── quantized/          ← saved to Google Drive (not in git)
│   ├── quantization.ipynb
│   ├── quantized_models.txt
│   └── QUANTISATION-REPORT.md
│
├── Day-4/
│   ├── benchmarks/
│   ├── inference/
│   └── BENCHMARK-REPORT.md
│
└── Day-5/
    ├── deploy/
    │   ├── app.py
    │   ├── config.py
    │   └── model_loader.py
    ├── models/             ← GGUF model mounted from Google Drive
    ├── images/
    ├── streamlit_app.py
    ├── Dockerfile
    ├── README.md
    └── FINAL-REPORT.md
```

---

## Why Adapters & Models Are Not in Git

| Artifact | Location |
|---|---|
| `adapter_model.safetensors` | Google Drive |
| `model-int8`, `model-int4` | Google Drive |
| `model-q8_0.gguf` | Google Drive |

These files exceed Git/GitHub limits. All notebooks mount Google Drive and load models directly from there.

---

## Stack

`transformers` · `peft` · `trl` · `bitsandbytes` · `accelerate` · `llama.cpp` · `fastapi` · `streamlit`