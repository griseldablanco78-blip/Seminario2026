# app.py
"""Gradio application for supermarket offers recommendation using HuggingFace e5 models.

Features:
1️⃣ Get top‑5 offers for a product.
2️⃣ Show products with missing expense (expensas) equal to 1.
3️⃣ Voice query → speech‑to‑text → same handling as #1.

The model is used only for inference (embedding + similarity search).
"""

import gradio as gr
import pandas as pd
import numpy as np
import time
from typing import List, Tuple

# ------------------------------------------------------------
# 1. Load data (mock dataset of offers). In a real scenario this
# would be loaded from a database or a CSV file stored alongside the
# app. For the demo we create a small in‑memory table.
# ------------------------------------------------------------
offers_data = pd.DataFrame(
    [
        {"supermarket": "Supermercado A", "product": "Leche", "price": 1.20, "offer": "2x1", "expensas": 0},
        {"supermarket": "Supermercado B", "product": "Leche", "price": 1.15, "offer": "Descuento 10%", "expensas": 1},
        {"supermarket": "Supermercado C", "product": "Arroz", "price": 0.90, "offer": "3x2", "expensas": 0},
        {"supermarket": "Supermercado A", "product": "Arroz", "price": 0.95, "offer": "Descuento 5%", "expensas": 1},
        {"supermarket": "Supermercado B", "product": "Huevos", "price": 2.10, "offer": "Pack 12", "expensas": 0},
        {"supermarket": "Supermercado C", "product": "Huevos", "price": 2.05, "offer": "Descuento 8%", "expensas": 1},
        # ... add more rows for a realistic demo
    ]
)

# ------------------------------------------------------------
# 2. Model loading – we use the small e5 model for embeddings.
# ------------------------------------------------------------
from transformers import AutoTokenizer, AutoModel
from huggingface_hub import InferenceClient

# Local inference (pipeline‑style) – runs on the host where the app lives.
TOKENIZER_SMALL = AutoTokenizer.from_pretrained("intfloat/e5-small-v2")
MODEL_SMALL = AutoModel.from_pretrained("intfloat/e5-small-v2")

# Remote inference – uses the HF Inference API (free tier). This is a
# fallback when the host does not have GPU/CPU capacity.
client_large = InferenceClient(model="intfloat/e5-large-v2")

def embed_text_local(text: str) -> np.ndarray:
    """Create an embedding using the locally loaded e5‑small model.
    The model returns a (1, 768) tensor – we flatten it to a 1‑D array.
    """
    inputs = TOKENIZER_SMALL(text, return_tensors="pt")
    with torch.no_grad():
        outputs = MODEL_SMALL(**inputs)
    # The e5 model puts the embedding in the last hidden state pooler output.
    embedding = outputs.last_hidden_state.mean(dim=1).cpu().numpy().flatten()
    return embedding

def embed_text_remote(text: str) -> np.ndarray:
    """Create an embedding using the remote e5‑large model via InferenceClient.
    The API returns a list of floats.
    """
    resp = client_large.post(json={"inputs": text})
    return np.array(resp)

def get_top_offers(product_name: str, use_remote: bool = False) -> List[Tuple[str, str, float, str]]:
    """Return the top‑5 offers for *product_name*.
    The function computes the cosine similarity between the query embedding
    and each row's *product* embedding (pre‑computed on app start).
    """
    # Pre‑compute embeddings for the catalogue once (simple memoisation).
    if not hasattr(get_top_offers, "catalog_embeddings"):
        # Compute embeddings for each distinct product in the dataset.
        products = offers_data["product"].unique()
        embed_fn = embed_text_remote if use_remote else embed_text_local
        get_top_offers.catalog_embeddings = {
            p: embed_fn(p) for p in products
        }
    embed_fn = embed_text_remote if use_remote else embed_text_local
    query_emb = embed_fn(product_name)

    # Cosine similarity helper
    def cosine(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)

    # Compute similarity for each row and sort.
    offers_data["sim"] = offers_data["product"].apply(lambda p: cosine(query_emb, get_top_offers.catalog_embeddings[p]))
    top5 = (
        offers_data.sort_values("sim", ascending=False)
        .head(5)
        .loc[:, ["supermarket", "product", "price", "offer"]]
        .itertuples(index=False, name=None)
    )
    # Clean up temporary column for subsequent calls.
    offers_data.drop(columns=["sim"], inplace=True)
    return list(top5)

def missing_expensas() -> pd.DataFrame:
    """Return rows where *expensas* == 1 (as requested by the assignment)."""
    return offers_data[offers_data["expensas"] == 1]

# ------------------------------------------------------------
# 3. Gradio UI definition.
# ------------------------------------------------------------
with gr.Blocks(theme=gr.themes.Default()) as demo:
    gr.Markdown("# 🛒 Supermarket Offers Assistant")
    with gr.Tab("🔎 Top 5 offers"):
        txt_query = gr.Textbox(label="Producto a buscar", placeholder="ej: leche, arroz, huevos")
        use_remote = gr.Checkbox(label="Usar modelo remoto (e5‑large) – más preciso, lento", value=False)
        btn_search = gr.Button("Buscar ofertas")
        out_table = gr.Dataframe(headers=["Supermercado", "Producto", "Precio", "Oferta"], label="Top 5 resultados")
        btn_search.click(fn=lambda q, r: get_top_offers(q, r), inputs=[txt_query, use_remote], outputs=out_table)
    with gr.Tab("📊 Productos con expensas = 1"):
        btn_missing = gr.Button("Mostrar productos")
        out_missing = gr.Dataframe(headers=["Supermercado", "Producto", "Precio", "Oferta", "Expensas"], label="Productos con expensas = 1")
        btn_missing.click(fn=lambda: missing_expensas().values.tolist(), inputs=None, outputs=out_missing)
    with gr.Tab("🎤 Consulta por voz"):
        voice_input = gr.Audio(source="microphone", type="filepath", label="Habla tu consulta")
        btn_voice = gr.Button("Procesar")
        out_voice = gr.Dataframe(headers=["Supermercado", "Producto", "Precio", "Oferta"], label="Resultado de voz")
        def voice_flow(audio_path, remote):
            # Simple speech‑to‑text using Whisper (via HF API)
            whisper_client = InferenceClient(model="openai/whisper-base")
            transcription = whisper_client.post(json={"inputs": open(audio_path, "rb")})
            text = transcription.get("text", "").strip()
            return get_top_offers(text, remote)
        btn_voice.click(fn=voice_flow, inputs=[voice_input, use_remote], outputs=out_voice)

if __name__ == "__main__":
    # Launch on a public URL (default gradio.share=True) – suitable for quick demo.
    demo.queue().launch(share=True)
