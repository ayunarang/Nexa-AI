from typing import List
import os, psutil
import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer

MODEL_ID = "sentence-transformers/paraphrase-albert-small-v2"
ONNX_MODEL_DIR = "onnx_quant"
ONNX_MODEL_FILE = "model_quantized.onnx"
BATCH_SIZE = 4 

tokenizer = None
session = None

def print_memory_usage(stage):
    mem = psutil.Process(os.getpid()).memory_info().rss / 1024**2
    print(f"[Memory] {stage} - {mem:.2f} MB")

def embed_texts(texts: List[str], batch_size: int = BATCH_SIZE) -> List[List[float]]:
    global tokenizer, session

    if session is None:
        print_memory_usage("Before model load")

        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        model_path = os.path.join(ONNX_MODEL_DIR, ONNX_MODEL_FILE)

        try:
            session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
        except Exception as e:
            raise RuntimeError(f"Failed to load ONNX model: {e}")

        print_memory_usage("After model load")

    embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        inputs = tokenizer(batch, padding=True, truncation=True, return_tensors="np")

        expected_inputs = set(i.name for i in session.get_inputs())
        ort_inputs = {k: v for k, v in inputs.items() if k in expected_inputs}

        ort_outputs = session.run(None, ort_inputs)
        last_hidden_state = ort_outputs[0]

        # Mean pooling
        attention_mask = np.expand_dims(inputs["attention_mask"], -1)
        summed = (last_hidden_state * attention_mask).sum(axis=1)
        counts = attention_mask.sum(axis=1)
        mean_pooled = summed / counts

        embeddings.extend(mean_pooled.tolist())

    return embeddings
