# Model Benchmark (Day-1 Multi-Agent System)

## Setup

* Pipeline: `Research → Summarizer → Answer`
* Execution: Sequential
* Runtime: Local (Ollama, CPU)
* Context: `buffer_size = 10`
* Benchmark Query:
  **What are the ways to deploy AI models on edge devices?**

---

# Qwen 2.5 7B (q4) — Selected Model

**Model:** `qwen2.5:7b-instruct-q4_0`

## Output

**Short Explanation**
Edge deployment involves adapting AI models to run efficiently on devices with limited compute and memory.

**Key Points**

* Quantization (INT8/INT4) reduces memory usage
* Pruning removes redundant parameters
* Model distillation creates lightweight models
* Conversion to ONNX, TensorRT, TensorFlow Lite
* Hardware-aware optimization (CPU, GPU, NPU)
* Edge runtimes like ONNX Runtime and TFLite
* Container-based deployment on edge systems
* Offline inference for low-latency execution

**Conclusion**
Efficient edge deployment focuses on reducing model size while maintaining acceptable performance.

## Latency

| Stage      |         Time |
| ---------- | -----------: |
| Research   |      49.60 s |
| Summarizer |      34.37 s |
| Answer     |      41.84 s |
| **Total**  | **125.81 s** |

## Observed Issues

* Slightly generic conclusion
* Minor drop in depth for follow-up queries

---

# Mistral 7B (Instruct)

## Output

**Short Explanation**
Deploying AI models on edge devices requires optimizing them for performance and compatibility with constrained hardware.

**Key Points**

* Quantization and pruning for model compression
* Conversion to ONNX and TensorRT
* TensorFlow Lite for lightweight deployment
* Hardware-specific inference optimization
* Use of edge inference engines

**Conclusion**
Edge deployment enhances performance by reducing model complexity and adapting to device limitations.

## Latency

| Stage      |         Time |
| ---------- | -----------: |
| Research   |      55.42 s |
| Summarizer |      40.18 s |
| Answer     |      50.36 s |
| **Total**  | **145.96 s** |

## Observed Issues

* Misses some important techniques (distillation, containers)
* Less structured output compared to Qwen
* Slight inconsistency in detail level

---

# Phi-3 (~3.8B)

## Output

**Short Explanation**
AI models can be adapted for edge devices by simplifying them and using efficient deployment formats.

**Key Points**

* Quantization reduces model size
* Pruning removes unnecessary weights
* Conversion to TensorFlow Lite or ONNX
* Lightweight runtimes for execution

**Conclusion**
Edge deployment mainly focuses on simplifying models to fit hardware constraints.

## Latency

| Stage      |        Time |
| ---------- | ----------: |
| Research   |     24.28 s |
| Summarizer |     20.14 s |
| Answer     |     26.32 s |
| **Total**  | **70.74 s** |

## Observed Issues

* Missing key methods (distillation, hardware tuning)
* Limited technical depth
* Outputs are more generic

---

# TinyLlama (~1.1B)

## Output

**Short Explanation**
Edge devices can run AI models if the models are small and efficient.

**Key Points**

* Smaller models improve speed
* Basic optimization techniques
* Lightweight execution
* Cloud deployment can support edge devices  

**Conclusion**
Simple optimizations allow AI models to run on edge devices, but capabilities remain limited.

## Latency

| Stage      |        Time |
| ---------- | ----------: |
| Research   |     10.12 s |
| Summarizer |      8.06 s |
| Answer     |     10.21 s |
| **Total**  | **28.39 s** |

## Observed Issues

* Hallucinated concept (cloud ≠ edge deployment method)
* Poor coverage of real techniques
* Weak structure and reasoning

---

# Qwen 7B (Full FP16)

## Output

**Short Explanation**
Edge deployment of AI models is achieved through advanced optimization techniques and hardware-aware execution strategies.

**Key Points**

* Quantization (INT8/INT4) and pruning
* Knowledge distillation for compact models
* Conversion to ONNX, TensorRT, TensorFlow Lite
* Hardware-specific optimization (CPU, GPU, NPU)
* Edge runtimes and inference frameworks
* Containerized and offline deployment pipelines

**Conclusion**
Edge deployment combines model optimization and system-level design to enable efficient local inference.

## Latency

| Stage      |         Time |
| ---------- | -----------: |
| Research   |      62.75 s |
| Summarizer |      48.63 s |
| Answer     |      58.92 s |
| **Total**  | **170.30 s** |

## Observed Issues

* More verbose outputs
* High latency reduces usability in iterative workflows

---

# Final Comparison

| Model       | Strength       | Weakness                     | Latency  |
| ----------- | -------------- | ---------------------------- | -------- |
| TinyLlama   | Fast           | Hallucination, poor coverage | 28.39 s  |
| Phi-3       | Efficient      | Missing depth                | 70.74 s  |
| Mistral 7B  | Good reasoning | Misses key techniques        | 145.96 s |
| Qwen Full   | Best quality   | Very slow                    | 170.30 s |
| **Qwen q4** | Best balance   | Slight generalization        | 125.81 s |

---

# Final Decision

**Selected Model:** `qwen2.5:7b-instruct-q4_0`

## Why


* Lower latency than Mistral and full Qwen
* Works efficiently in local setup

## Trade-off

* High latency due to sequential execution
* Slight reduction in depth compared to full model

---

## Final Statement

> Qwen q4 provides the best balance between structured output, reasoning capability, and local execution efficiency while minimizing hallucination compared to smaller models, making it the most suitable choice for Day-1 multi-agent implementation.
