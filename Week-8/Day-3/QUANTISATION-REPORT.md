# Day 3 --- Model Quantization and Performance Evaluation

## Objective

The goal of this task is to understand how **model quantization affects
model size and inference performance**. Quantization reduces the
precision of model weights so that models become **smaller and easier to
run** on limited hardware.

In this experiment we tested:

-   FP16 (Half precision)
-   INT8 Quantization
-   INT4 Quantization
-   GGUF Quantization (Q8_0)

------------------------------------------------------------------------

## Workflow

Steps followed in this experiment:

1.  Load the base model.
2.  Convert the model to **FP16 format**.
3.  Apply **INT8 and INT4 quantization**.
4.  Convert the model to **GGUF format**.
5.  Quantize the GGUF model to **Q8_0 using llama.cpp**.
6.  Run inference and measure performance.

------------------------------------------------------------------------

## Workflow Diagram

    Base Model
       │
       ▼
    FP16 Model
       │
       ├── INT8 Model
       ├── INT4 Model
       │
       ▼
    Convert to GGUF
       │
       ▼
    GGUF Q8_0 Model
       │
       ▼
    Run Inference using llama.cpp

------------------------------------------------------------------------

## Test Setup

Prompt used:

    Explain machine learning in simple terms.

Generated tokens: **50**

Environment:

-   Python
-   Google Colab
-   llama.cpp

------------------------------------------------------------------------

## Results

  Format        Model Size   Time (s)   Tokens/sec
  ------------- ------------ ---------- ------------
  FP16          2.9 GB       2.49       23.25
  INT8          1.7 GB       8.99       6.45
  INT4          1.2 GB       3.52       16.47
  GGUF (Q8_0)   1.53 GB      10.64      4.7

------------------------------------------------------------------------

## GGUF Model Test

Command used:

    ./build/bin/llama-cli \
    -m model-q8_0.gguf \
    -p "Explain machine learning in simple terms." \
    -n 50

Example output:

Machine learning is a type of artificial intelligence that allows
computers to learn from data and improve their performance without being
explicitly programmed.

Performance:

-   Prompt speed: **14.1 tokens/sec**
-   Generation speed: **4.7 tokens/sec**

------------------------------------------------------------------------

## What I Learned

-   Quantization reduces the **size of large language models**.
-   Different formats (FP16, INT8, INT4) affect **speed and storage**.
-   GGUF format is optimized for **running models with llama.cpp**.
-   Quantized models allow **LLMs to run on CPUs with less memory**.

------------------------------------------------------------------------

## Conclusion

Model quantization helps reduce model size while maintaining useful
performance.

-   **FP16** gives the best accuracy but largest size.
-   **INT8 and INT4** reduce storage requirements.
-   **GGUF Q8_0** allows efficient CPU inference using llama.cpp.

Overall, quantization makes large language models **easier to deploy on
limited hardware**.

------------------------------------------------------------------------

## Tools Used

-   Python
-   llama.cpp
-   Google Colab