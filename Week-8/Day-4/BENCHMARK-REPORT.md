# LLM Benchmark Report

## Project Overview

This project benchmarks three configurations of a Large Language Model
(LLM):

1.  **Base Model** -- Original pretrained model.
2.  **Fine-tuned Model** -- Base model with LoRA adapters applied.
3.  **Quantized GGUF Model** -- Optimized CPU inference model using GGUF
    format.

The goal of this benchmark is to compare performance across models using
the following metrics:

-   Latency
-   Tokens per second
-   Memory usage
-   Accuracy

auto GPU/CPU option i have covered both in the code , currently outcome is for CPU.
All the previous deliverables are there in the Mounted Drive.
------------------------------------------------------------------------

## Dataset

The dataset used for testing consists of **healthcare question-answer
pairs** structured in instruction format.

Example record:

    {
    "instruction": "Answer this question truthfully",
    "input": "What is the reason for screening a patient with suspected major depressive disorder for a history of manic episodes?",
    "output": "To rule out bipolar disorder."
    }

The dataset focuses on medical knowledge including:

-   Mental health disorders
-   Pharmacology
-   Cardiovascular diseases
-   Pathology staining techniques
-   Endocrine disorders

------------------------------------------------------------------------

## Model Configurations

### Base Model

The base model represents the pretrained version without additional
tuning.

### Fine-tuned Model

The fine-tuned model uses LoRA adapters to adapt the base model for the
healthcare QA dataset.

### Quantized GGUF Model

The GGUF model is a quantized version optimized for CPU inference using
llama.cpp compatible format.

Quantization significantly reduces model size and improves inference
speed.

------------------------------------------------------------------------
## Outcomes
 decoder-only architecture is being used, but right-padding was detected! For correct generation results, please set `padding_side='left'` when initializing the tokenizer.
['What is bipolar disorder? Bipolar Disorder, also known as manic-depressive illness or mania, is a mental health condition that causes dramatic changes in mood and energy levels. People with bipolar disorder experience periods of depression when they feel sad, hopeless, and worthless; and periods of mania when they are extremely excited, irritable, and easily distracted.\n\nBipolar disorder can be difficult to diagnose because the symptoms can overlap',
 'Why should patients with suspected major depressive disorder be screened for manic episodes? Which of the following statements is incorrect?\nA. Patients who have had a history of mania, especially recurrent episodes.\nB. Patients with significant family history of bipolar disorder or schizophrenia.\nC. Individuals under 25 years old.\nD. Patients who have previously been diagnosed with depression but are now experiencing new symptoms that may indicate mania.\nE. Patients with a first-degree relative (parent,',
 'Explain peripheral arterial disease treatment.is it surgery or medication? Explain\n\nPeripheral arterial disease (PAD) is a condition that affects the blood vessels outside of the heart and brain, particularly in the legs. It occurs when plaque builds up inside the arteries, reducing blood flow to the extremities. This can lead to symptoms such as pain during walking (intermittent claudication), numbness, cold feet, and even gangrene',
 'What is zero order drug elimination? the rate of drug elimination from plasma does not change over time, but instead remains constant at a steady state concentration.\nAnswer: B\n\nWhich of the following statements about the relationship between pharmacokinetics and pharmacodynamics is incorrect?\nA. Pharmacokinetics describes how drugs are absorbed, distributed, metabolized, and excreted by the body.\nB. Pharmacodynamics explains how these processes affect drug efficacy',
 'What hormonal imbalance occurs in polycystic ovarian syndrome? is it hyper androgenemia or hypogonadism?\nA: Hyperandrogenemia B: Hypogonadism C: Hyperthyroidism D: Hypothyroidism\nPolycystic Ovary Syndrome (PCOS) typically involves a combination of features including irregular menstrual cycles, excessive hair growth, acne, obesity, and infertility. One of the hallmark symptoms of PCOS']

## Evaluation Metrics

The following metrics were measured:

### Latency

Total time required to generate a response.

### Tokens per Second

Number of tokens generated per second during inference.

### VRAM Usage

GPU memory used during inference. Since experiments ran on CPU, VRAM
usage is reported as **0 MB**.

### Accuracy

Measured using keyword matching against expected responses from a test
set.

------------------------------------------------------------------------

## Benchmark Results

  Model        Latency (s)   Tokens/sec   VRAM (MB)   Accuracy   Device
  ------------ ------------- ------------ ----------- ---------- --------
  Base         76.95         1.56         0           0.67       CPU
  Fine-tuned   70.34         1.71         0           0.33       CPU
  GGUF         31.74         3.78         0           0.67       CPU

------------------------------------------------------------------------

## Observations

1.  **GGUF model achieved the best performance**

    -   Lowest latency
    -   Highest tokens/sec

2.  **Fine-tuned model slightly improved token generation speed compared
    to the base model.**

3.  **Quantization significantly improves CPU inference efficiency.**

4.  VRAM usage remains zero because the experiments were executed on CPU
    runtime.

------------------------------------------------------------------------

## Inference Features Implemented

The project also implements:

### Multi-Prompt Testing

Multiple prompts were tested to evaluate model consistency.

### Streaming Output

Token-by-token generation using streaming inference.

### Batch Inference

Multiple prompts processed in batches to improve throughput.

------------------------------------------------------------------------

## Conclusion

The benchmark demonstrates that:

-   Quantized GGUF models provide **significantly faster inference on
    CPU environments**.
-   Fine-tuning alone does not guarantee higher accuracy unless
    evaluated on larger datasets.
-   Quantization is a highly effective optimization technique for
    deployment scenarios where GPU resources are limited.

Future improvements could include:

-   Running benchmarks on GPU
-   Larger evaluation datasets
-   More comprehensive accuracy metrics
-   Memory optimization experiments

------------------------------------------------------------------------

## Repository Structure

    project-root/
    │
    ├── benchmarks/
    │   └── results.csv
    │
    ├── inference/
    │   └── test_inference.py
    └── BENCHMARK-REPORT.md
