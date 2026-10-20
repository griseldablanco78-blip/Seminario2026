"""
Backend FastAPI para Expensa House.
Sincroniza instantáneas de la App Android (Room DB) con la Aplicación Web.
Provee motor de IA para comparar ofertas de supermercados, búsqueda por voz y asistente Boti House.
"""
import os
import sys
import logging
import subprocess
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

# Añadir raíz al sys.path para importar data y web
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from data.db import (
    load_db, save_db, get_stock, add_or_update_stock_item, delete_stock_item,
    open_stock_unit, consume_stock_unit, get_shopping, add_shopping_item,
    update_shopping_item, delete_shopping_item, move_shopping_to_stock,
    get_user_prefs, update_user_prefs, get_expenses, add_expense,
    get_offers, add_offer
)
from web.ai_comparator import (
    OfferModelUnavailableError,
    compare_supermarket_offers,
    answer_ai_chat_query,
)

logger = logging.getLogger(__name__)
USE_WHISPER = os.getenv("USE_WHISPER", "0") == "1"

app = FastAPI(
    title="Expensa House API & Web",
    description="Ecosistema inteligente para la gestión de despensa familiar, ofertas de supermercados y sincronización Android/Web",
    version="2.0.0"
)

# Habilitar CORS para permitir llamadas desde cualquier origen (móvil, web local, emulador)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELOS PYDANTIC ---
class StockItemModel(BaseModel):
    id: Optional[str] = None
    name: str
    brand: Optional[str] = "Genérica"
    category: str
    stockQuantity: int = 1
    inUseCount: int = 0
    unit: Optional[str] = "unidad"
    price: Optional[float] = 0.0

class ShoppingItemModel(BaseModel):
    id: Optional[str] = None
    name: str
    brand: Optional[str] = "Genérica"
    category: str
    detail: Optional[str] = "Agregado manual"
    quantity: int = 1
    suggestedStore: Optional[str] = None
    checked: bool = False

class BudgetModel(BaseModel):
    monthlyBudget: float

class ExpenseModel(BaseModel):
    id: Optional[str] = None
    category: str
    amount: float
    timestamp: Optional[int] = None
    note: Optional[str] = ""

class ChatRequest(BaseModel):
    message: str

class AndroidSyncPayload(BaseModel):
    stock: Optional[List[Dict[str, Any]]] = None
    shopping: Optional[List[Dict[str, Any]]] = None
    expenses: Optional[List[Dict[str, Any]]] = None
    user_prefs: Optional[Dict[str, Any]] = None
    offers: Optional[List[Dict[str, Any]]] = None

# --- RUTAS DE STOCK ---
@app.get("/api/stock")
def api_get_stock():
    """Retorna todo el inventario con cantidades cerradas y en uso."""
    return get_stock()

@app.post("/api/stock")
def api_add_stock(item: StockItemModel):
    """Crea o actualiza un producto en el inventario."""
    saved = add_or_update_stock_item(item.dict())
    return {"status": "success", "item": saved}

@app.put("/api/stock/{item_id}")
def api_update_stock(item_id: str, item: StockItemModel):
    """Modifica un producto existente."""
    data = item.dict()
    data["id"] = item_id
    saved = add_or_update_stock_item(data)
    return {"status": "success", "item": saved}

@app.delete("/api/stock/{item_id}")
def api_delete_stock(item_id: str):
    """Elimina un producto del inventario."""
    ok = delete_stock_item(item_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"status": "success", "message": "Producto eliminado"}

@app.post("/api/stock/{item_id}/open")
def api_open_stock_unit(item_id: str):
    """Pasa una unidad de cerrada (stock) a abierta (en uso)."""
    res = open_stock_unit(item_id)
    if not res:
        raise HTTPException(status_code=400, detail="No hay unidades cerradas para abrir")
    return {"status": "success", "item": res}

@app.post("/api/stock/{item_id}/consume")
def api_consume_stock_unit(item_id: str):
    """Termina o consume una unidad que estaba abierta."""
    res = consume_stock_unit(item_id)
    if not res:
        raise HTTPException(status_code=400, detail="No hay unidades abiertas para terminar")
    return {"status": "success", "item": res}

# --- RUTAS DE LISTA DEL SÚPER (SHOPPING) ---
@app.get("/api/shopping")
def api_get_shopping():
    """Retorna la lista de compras."""
    return get_shopping()

@app.post("/api/shopping")
def api_add_shopping(item: ShoppingItemModel):
    """Agrega un producto a la lista de compras."""
    saved = add_shopping_item(item.dict())
    return {"status": "success", "item": saved}

@app.put("/api/shopping/{item_id}")
def api_update_shopping(item_id: str, updates: Dict[str, Any]):
    """Actualiza cantidad o datos de un ítem de la lista."""
    res = update_shopping_item(item_id, updates)
    if not res:
        raise HTTPException(status_code=404, detail="Ítem no encontrado")
    return {"status": "success", "item": res}

@app.post("/api/shopping/{item_id}/toggle")
def api_toggle_shopping(item_id: str):
    """Marca o desmarca un producto como comprado."""
    items = get_shopping()
    item = next((x for x in items if x["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Ítem no encontrado")
    new_checked = not item.get("checked", False)
    res = update_shopping_item(item_id, {"checked": new_checked})
    return {"status": "success", "item": res}

@app.post("/api/shopping/{item_id}/move-to-stock")
def api_move_to_stock(item_id: str):
    """Mueve un ítem de la lista de compras al inventario de la casa."""
    res = move_shopping_to_stock(item_id)
    if not res:
        raise HTTPException(status_code=404, detail="Ítem no encontrado en lista de compras")
    return {"status": "success", "stock_item": res}

@app.delete("/api/shopping/{item_id}")
def api_delete_shopping(item_id: str):
    """Elimina un ítem de la lista de compras."""
    ok = delete_shopping_item(item_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Ítem no encontrado")
    return {"status": "success", "message": "Ítem eliminado"}

# --- RUTAS DE PRESUPUESTO Y GASTOS ---
@app.get("/api/budget")
def api_get_budget():
    """Retorna el presupuesto mensual y el total gastado."""
    return get_user_prefs()

@app.post("/api/budget")
def api_set_budget(budget: BudgetModel):
    """Establece el monto de presupuesto mensual."""
    res = update_user_prefs({"monthlyBudget": budget.monthlyBudget})
    return {"status": "success", "user_prefs": res}

@app.get("/api/expenses")
def api_get_expenses():
    """Retorna el historial de gastos registrados."""
    return get_expenses()

@app.post("/api/expenses")
def api_add_expense(expense: ExpenseModel):
    """Registra un nuevo gasto / ticket de compra."""
    saved = add_expense(expense.dict())
    return {"status": "success", "expense": saved}

# --- COMPARADOR DE OFERTAS CON IA Y VOZ ---
@app.get("/api/offers/compare")
def api_compare_offers(q: str = "leche"):
    """
    Endpoint principal del Comparador IA:
    Compara ofertas de Coto, Carrefour, Día, Jumbo y ChangoMás,
    cruza con el stock local del usuario y emite un veredicto de compra inteligente.
    """
    try:
        return compare_supermarket_offers(q)
    except OfferModelUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

@app.get("/offers")
def api_android_remote_offers(q: str = ""):
    """
    Endpoint compatible directo con la interfaz Android Retrofit:
    SupermarketApi.kt -> @GET("offers") suspend fun getOffers(@Query("q") query: String): List<RemoteOffer>
    """
    try:
        comparison = compare_supermarket_offers(q or "leche")
    except OfferModelUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    remote_offers = []
    for off in comparison.get("offers", []):
        remote_offers.append({
            "store": off.get("store", "Supermercado"),
            "name": comparison.get("product_name", q),
            "brand": off.get("brand", "Genérica"),
            "price": f"${off.get('promo_price', 0):,.2f}",
            "discount": off.get("promo_text", "Oferta")
        })
    return remote_offers

@app.post("/api/ai/chat")
def api_ai_chat(req: ChatRequest):
    """Chatbot inteligente Boti House."""
    answer = answer_ai_chat_query(req.message)
    return {"answer": answer}

def _transcribe_with_google(audio_path: str) -> str:
    import speech_recognition as sr

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
    return recognizer.recognize_google(audio_data, language="es-AR")


def _convert_audio_to_wav(source_path: str, wav_path: str) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-i", source_path, "-ac", "1", "-ar", "16000", wav_path],
        check=True,
        capture_output=True,
        text=True,
    )


@app.post("/api/voice/transcribe")
async def api_voice_transcribe(audio: UploadFile = File(...)):
    """Transcribe audio con Whisper opcional y Google como alternativa."""
    audio_bytes = await audio.read()
    if not audio_bytes:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "El archivo de audio está vacío."},
        )

    suffix = Path(audio.filename or "").suffix.lower()
    if not suffix or not suffix[1:].isalnum():
        suffix = ".webm"

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            audio_path = os.path.join(temp_dir, f"recording{suffix}")
            wav_path = os.path.join(temp_dir, "recording.wav")
            with open(audio_path, "wb") as audio_file:
                audio_file.write(audio_bytes)

            if USE_WHISPER:
                try:
                    from web.voice_model import transcribe_audio

                    return {
                        "status": "success",
                        "text": transcribe_audio(audio_path),
                        "engine": "whisper",
                    }
                except Exception:
                    logger.warning(
                        "Whisper falló; se intentará la transcripción alternativa de Google.",
                        exc_info=True,
                    )

            google_audio_path = audio_path
            if suffix not in {".wav", ".wave"}:
                _convert_audio_to_wav(audio_path, wav_path)
                google_audio_path = wav_path
            return {
                "status": "success",
                "text": _transcribe_with_google(google_audio_path),
                "engine": "google",
            }
    except Exception as e:
        logger.exception("No se pudo transcribir el audio.")
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": f"No se pudo transcribir el audio: {str(e)}"}
        )

# --- SINCRONIZACIÓN ANDROID / WEB ---
@app.get("/api/sync")
def api_get_sync_state():
    """Devuelve el estado compartido para inicializar una instalación Android vacía."""
    return {"status": "success", "data": load_db()}


@app.post("/api/sync")
def api_full_sync(payload: AndroidSyncPayload):
    """
    Recibe una instantánea completa de Android y la publica para la Web.
    """
    db = load_db()

    if payload.stock is not None:
        db["stock"] = payload.stock
    if payload.shopping is not None:
        db["shopping"] = payload.shopping
    if payload.expenses is not None:
        db["expenses"] = payload.expenses
    if payload.user_prefs is not None:
        db["user_prefs"] = payload.user_prefs
    if payload.offers is not None:
        db["offers"] = payload.offers

    save_db(db)
    return {
        "status": "success",
        "message": "Sincronización completada con éxito",
        "data": load_db()
    }

# --- RUTAS RETROCOMPATIBLES ---
@app.get("/stock")
def get_legacy_stock():
    """Retrocompatibilidad con endpoints anteriores de api.py."""
    return get_stock()

@app.get("/productos_criticos")
def get_legacy_productos_criticos():
    """Retrocompatibilidad con endpoints anteriores de api.py."""
    stock = get_stock()
    return [p for p in stock if p.get("stockQuantity", 0) <= 1]

# --- SERVIR LA APLICACIÓN WEB (SPA) ---
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "css"), exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "js"), exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_home():
    """Sirve la página web principal de Expensa House."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Expensa House API está activa. Frontend en construcción."}
