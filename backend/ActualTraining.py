
import inspect
import sys
print(sys.executable)
from datasets import load_dataset
import transformers
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    DataCollatorForTokenClassification,
    Trainer,
    TrainingArguments
)
print(transformers.__version__)
print(transformers.__file__)
print(transformers.TrainingArguments)
print(transformers.TrainingArguments.__init__)
print(type(transformers.TrainingArguments.__init__))

print("TrainingArguments from:", inspect.getfile(TrainingArguments))
print("Init signature:", inspect.signature(TrainingArguments.__init__))

import numpy as np
import evaluate
import os

# Load dataset (assumes JSONL format)
dataset = load_dataset("json", data_files="vehicle_filters.jsonl")["train"]

# Split: 90% train, 10% eval
dataset = dataset.train_test_split(test_size=0.1)

# Extract label list
all_labels = set(label for ex in dataset["train"] for label in ex["tags"])
label_list = sorted(list(all_labels))
label2id = {label: idx for idx, label in enumerate(label_list)}
id2label = {idx: label for label, idx in label2id.items()}

# Tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

# Align tokens to labels
def tokenize_and_align_labels(example):
    tokenized_inputs = tokenizer(example["tokens"], truncation=True, is_split_into_words=True)
    word_ids = tokenized_inputs.word_ids()

    labels = []
    previous_word_idx = None
    for word_idx in word_ids:
        if word_idx is None:
            labels.append(-100)
        elif word_idx != previous_word_idx:
            labels.append(label2id[example["tags"][word_idx]])
        else:
            tag = example["tags"][word_idx]
            # Use the same tag as original for continuation tokens
            labels.append(label2id[tag])
        previous_word_idx = word_idx

    tokenized_inputs["labels"] = labels
    return tokenized_inputs


# Apply tokenization
tokenized_dataset = dataset.map(tokenize_and_align_labels)

# Load model
model = AutoModelForTokenClassification.from_pretrained(
    "bert-base-cased",
    num_labels=len(label_list),
    id2label=id2label,
    label2id=label2id
)

# Data collator
data_collator = DataCollatorForTokenClassification(tokenizer)

# Evaluation metric
metric = evaluate.load("seqeval")

def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    true_labels = [
        [id2label[l] for l in label if l != -100]
        for label in labels
    ]
    true_predictions = [
        [id2label[p] for (p, l) in zip(pred, label) if l != -100]
        for pred, label in zip(predictions, labels)
    ]

    results = metric.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }

# Training arguments
training_args = TrainingArguments(
    output_dir="./trained_model",
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=3e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=5,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    save_total_limit=1,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics
)

# Train
trainer.train()

# Save final model
trainer.save_model(r"backend/bert_model")  
