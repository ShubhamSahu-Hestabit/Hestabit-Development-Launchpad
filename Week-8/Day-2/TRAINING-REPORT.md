# TRAINING-REPORT.md

## Week-8 --- Day-2 LoRA Fine-Tuning

------------------------------------------------------------------------

# Objective

Perform parameter-efficient fine-tuning of a Large Language Model using
LoRA adapters instead of full model training.\
This reduces GPU memory usage and trains only a small number of
parameters.

------------------------------------------------------------------------

# Base Model

Model used:

Qwen/Qwen2.5-1.5B-Instruct

-   \~1.5B parameters
-   Instruction tuned
-   Transformer decoder architecture

------------------------------------------------------------------------

# Dataset

Dataset prepared in Day-1.

Source: medalpaca/medical_meadow_medical_flashcards

Format used:

{ "instruction": "...", "input": "...", "output": "..." }

Training prompt format:

### Instruction:

{instruction}

### Input:

{input}

### Response:

{output}

------------------------------------------------------------------------

# Fine-Tuning Method

Technique used:

LoRA (Low Rank Adaptation)

Only attention layers were modified.

Configuration:

  Parameter        Value
  ---------------- ----------------
  Rank (r)         16
  Alpha            32
  Dropout          0.05
  Target Modules   q_proj, v_proj
  Task             CAUSAL_LM

This trains less than 1% of total model parameters.

------------------------------------------------------------------------

# Quantization

To reduce GPU memory usage, 4-bit quantization was used with
BitsAndBytes.

Configuration:

-   load_in_4bit = True
-   quant_type = nf4
-   compute_dtype = float16

This allowed training on Google Colab GPU.

------------------------------------------------------------------------

# Training Configuration

Training performed using TRL SFTTrainer.

  Parameter               Value
  ----------------------- -------
  Batch Size              2
  Gradient Accumulation   2
  Epochs                  3
  Learning Rate           2e-4
  Optimizer               AdamW
  Precision               FP16
  Logging Steps           10

------------------------------------------------------------------------

# Training Progress

Training ran for 3 epochs and 630 steps.

Sample logs:

  Step   Loss
  ------ --------
  10     1.6826
  100    0.9926
  200    0.9447
  300    0.9244
  400    0.9739
  500    0.8821
  630    0.9283

Final output:

TrainOutput( global_step=630, training_loss=0.9882, epoch=3.0 )

Loss decreased steadily showing successful learning.

------------------------------------------------------------------------

# Output Artifacts

After training, LoRA adapters were saved.

Modern PEFT versions save adapters as:

adapter_model.safetensors

instead of .bin.

Saved adapter folder:

adapters/

adapter_model.safetensors\
adapter_config.json\
tokenizer.json\
tokenizer_config.json\
vocab.json\
merges.txt

Important deliverables:

adapter_model.safetensors\
adapter_config.json

------------------------------------------------------------------------

# Deliverables

Week-8/

notebooks/ └── lora_train.ipynb

adapters/ ├── adapter_model.safetensors └── adapter_config.json

TRAINING-REPORT.md

------------------------------------------------------------------------

# Key Learning

This exercise demonstrated:

-   Parameter-efficient fine-tuning
-   LoRA adapter training
-   4-bit quantized training
-   Instruction tuning workflow
-   Adapter-based model deployment

------------------------------------------------------------------------

# Next Step

In Day-3 the trained LoRA adapter will be:

1.  Loaded with the base model
2.  Merged with model weights
3.  Quantized for efficient inference
