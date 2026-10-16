"""Compara las ofertas sincronizadas de Expensa House con similitud semántica E5."""
import re
import unicodedata
from functools import lru_cache
from typing import Dict, Any, Optional, Tuple
import os
import sys

# Añadir raíz al sys.path para importar data.db
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from data.db import get_offers, get_stock

E5_MODEL_ID = "intfloat/multilingual-e5-small"
KEYWORD_MATCH_THRESHOLD = 0.5


class OfferModelUnavailableError(RuntimeError):
    """The semantic offer-search model could not be loaded."""


@lru_cache(maxsize=1)
def _load_e5_components() -> Tuple[Any, Any, Any]:
    try:
        import torch
        from transformers import AutoModel, AutoTokenizer
    except ImportError as exc:
        raise OfferModelUnavailableError(
            "Faltan dependencias para la búsqueda semántica. "
            "Instalá las dependencias de Clase 7 con pip."
        ) from exc

    try:
        tokenizer = AutoTokenizer.from_pretrained(E5_MODEL_ID)
        model = AutoModel.from_pretrained(E5_MODEL_ID)
    except (OSError, RuntimeError, ValueError) as exc:
        raise OfferModelUnavailableError(
            "No se pudo cargar multilingual-e5-small. Verificá la conexión a "
            "Internet y que haya espacio y memoria disponibles; la primera carga "
            "descarga el modelo desde Hugging Face."
        ) from exc

    model.eval()
    return tokenizer, model, torch


@lru_cache(maxsize=512)
def _embed_e5_text(prefix: str, text: str) -> Any:
    tokenizer, model, torch = _load_e5_components()
    import torch.nn.functional as functional

    tokens = tokenizer(
        f"{prefix}: {text}",
        return_tensors="pt",
        truncation=True,
        max_length=512,
    )
    with torch.inference_mode():
        output = model(**tokens)
        attention_mask = tokens["attention_mask"].unsqueeze(-1)
        pooled = (output.last_hidden_state * attention_mask).sum(dim=1)
        pooled = pooled / attention_mask.sum(dim=1).clamp(min=1)
        return functional.normalize(pooled, p=2, dim=1)[0].cpu()


def _e5_similarity(query: str, passage: str) -> float:
    query_embedding = _embed_e5_text("query", query)
    passage_embedding = _embed_e5_text("passage", passage)
    return float(query_embedding @ passage_embedding)


def clean_query(q: str) -> str:
    """Limpia el texto de búsqueda proveniente de voz o teclado."""
    q = q.lower().strip()
    # Eliminar frases comunes de entrada de voz
    phrases_to_remove = [
        "quiero comparar", "comparar ofertas de", "buscar ofertas de", "cuanto sale", "cuánto cuesta",
        "donde esta mas barato", "dónde está más barato", "buscar", "comparar", "ofertas de", "precio de"
    ]
    for p in phrases_to_remove:
        q = q.replace(p, "")
    q = re.sub(r'[^\w\s]', '', q)
    return q.strip()

def compare_supermarket_offers(raw_query: str) -> Dict[str, Any]:
    """
    Ordena por similitud E5 las ofertas guardadas que también pasan el filtro
    conservador de palabras clave. No inventa precios ni promociones.
    """
    cleaned = clean_query(raw_query)
    query_tokens = _comparison_tokens(cleaned)
    if not query_tokens:
        return _empty_comparison(cleaned, "Escribí el nombre del producto que querés comparar.")

    keyword_candidates = []
    incomplete_offer_count = 0
    for saved_offer in get_offers():
        product = str(saved_offer.get("product", "")).strip()
        if not product:
            continue
        brand = str(saved_offer.get("brand", ""))
        product_tokens = _comparison_tokens(
            f"{product} {brand}"
        )
        overlap = query_tokens & product_tokens
        keyword_score = len(overlap) / len(query_tokens)
        if not overlap or keyword_score <= KEYWORD_MATCH_THRESHOLD:
            continue

        price = _parse_saved_price(saved_offer.get("price", ""))
        if price is None:
            incomplete_offer_count += 1
            continue

        keyword_candidates.append((saved_offer, product, brand, price, keyword_score))

    if not keyword_candidates:
        message = (
            "No hay ofertas manuales con suficientes palabras clave compartidas. "
            "La similitud semántica por sí sola no confirma que sea el mismo producto."
        )
        if incomplete_offer_count:
            message += (
                f" Hay {incomplete_offer_count} oferta(s) coincidente(s) sin precio; "
                "completá el precio en la app y sincronizá nuevamente."
            )
        return _empty_comparison(cleaned, message)

    matched_offers = []
    query_text = " ".join(str(raw_query or "").split())
    for saved_offer, product, brand, price, keyword_score in keyword_candidates:
        passage = " ".join(part for part in (product, brand) if part).strip()
        semantic_score = _e5_similarity(query_text, passage)
        saving = str(saved_offer.get("saving", "")).strip()
        saving_match = re.search(r"(\d+(?:[.,]\d+)?)\s*%", saving)
        saving_percent = (
            float(saving_match.group(1).replace(",", ".")) if saving_match else 0.0
        )
        matched_offers.append({
            "store": str(saved_offer.get("store", "Supermercado")),
            "store_badge": re.sub(
                r"[^a-z0-9-]+",
                "-",
                _normalize_comparison_text(saved_offer.get("store", "")),
            ).strip("-"),
            "brand": str(saved_offer.get("brand", "Genérica")),
            "regular_price": price,
            "promo_price": price,
            "promo_text": saving or "Precio cargado manualmente",
            "unit_effective_price": price,
            "saving_percent": saving_percent,
            "promo_type": "direct",
            "direct_link": "",
            "in_stock": True,
            "delivery_time": "",
            "product": product,
            "match_score": semantic_score,
            "keyword_match_score": keyword_score,
        })

    offers = sorted(
        matched_offers,
        key=lambda offer: (-offer["match_score"], offer["promo_price"]),
    )
    product_name = offers[0]["product"]
    category = "General"
    best_single = min(offers, key=lambda offer: offer["promo_price"])
    best_bulk = min(offers, key=lambda offer: offer["unit_effective_price"])
    max_saving = max(offer["saving_percent"] for offer in offers)
    current_stock_list = get_stock()
    stock_match = None
    for item in current_stock_list:
        item_tokens = _comparison_tokens(
            f"{item.get('name', '')} {item.get('brand', '')}"
        )
        if query_tokens & item_tokens:
            stock_match = item
            category = item.get("category", category)
            break
            
    stock_status_alert = None
    stock_advice = ""
    if stock_match:
        qty = stock_match.get("stockQuantity", 0)
        in_use = stock_match.get("inUseCount", 0)
        if qty <= 1:
            stock_status_alert = f"⚠️ Stock Crítico: Te quedan solo {qty} unidad(es) cerrada(s) y {in_use} abierta(s) en casa."
            stock_advice = f"Como tu stock está bajo, revisá el precio cargado en **{best_single['store']}** antes de reponer."
        else:
            stock_status_alert = f"✅ Stock Saludable: Tienes {qty} unidades cerradas y {in_use} en uso."
            stock_advice = "Tu stock actual es suficiente; compará los precios guardados antes de hacer otra compra."
    else:
        stock_status_alert = "ℹ️ Este producto no está en tu inventario habitual."
        stock_advice = "Revisá la oferta y agregá el producto a tu lista si lo necesitás."

    verdict_text = (
        f"Se encontraron {len(offers)} oferta(s) manual(es) para {product_name}. "
        f"El menor precio cargado es {best_single['store']} "
        f"(${best_single['promo_price']:,.2f}). "
        "La app no registra cantidad/unidad ni fecha de actualización de la oferta, "
        "por lo que todavía no se puede validar el precio por kilo/litro ni su vigencia. "
        f"{stock_advice}"
    )

    return {
        "query": raw_query,
        "cleaned_query": cleaned,
        "product_name": product_name,
        "category": category,
        "offers": offers,
        "ai_analysis": {
            "best_single": {
                "store": best_single["store"],
                "price": best_single["promo_price"],
                "promo_text": best_single["promo_text"]
            },
            "best_bulk": {
                "store": best_bulk["store"],
                "effective_price": best_bulk["unit_effective_price"],
                "promo_text": best_bulk["promo_text"],
                "saving_percent": best_bulk["saving_percent"]
            },
            "max_saving_percent": max_saving,
            "verdict": verdict_text,
            "stock_alert": stock_status_alert,
            "suggested_store": best_bulk["store"] if (stock_match and stock_match.get("stockQuantity", 0) <= 1) else best_single["store"]
        }
    }


def _normalize_comparison_text(value: Any) -> str:
    normalized = unicodedata.normalize("NFKD", str(value or ""))
    return "".join(char for char in normalized if not unicodedata.combining(char)).lower()


def _comparison_tokens(value: Any) -> set[str]:
    stop_words = {"a", "al", "de", "del", "el", "la", "las", "los", "para", "por", "un", "una"}
    tokens = set(re.findall(r"[a-z0-9]+", _normalize_comparison_text(value)))
    return tokens - stop_words


def _parse_saved_price(value: Any) -> Optional[float]:
    text = re.sub(r"[^\d,.-]", "", str(value or "")).strip()
    if not text:
        return None
    if "," in text:
        text = text.replace(".", "").replace(",", ".")
    elif "." in text:
        whole, separator, decimal = text.rpartition(".")
        if separator and len(decimal) == 3:
            text = whole + decimal
    try:
        price = float(text)
    except ValueError:
        return None
    return price if price > 0 else None


def _empty_comparison(query: str, message: str) -> Dict[str, Any]:
    return {
        "query": query,
        "cleaned_query": query,
        "product_name": query,
        "category": "General",
        "offers": [],
        "ai_analysis": {
            "best_single": {"store": "", "price": 0, "promo_text": ""},
            "best_bulk": {"store": "", "effective_price": 0, "promo_text": "", "saving_percent": 0},
            "max_saving_percent": 0,
            "verdict": message,
            "stock_alert": None,
            "suggested_store": "",
        },
    }


def answer_ai_chat_query(user_msg: str) -> str:
    """Responde consultas del menú del asistente usando los datos guardados."""
    msg = re.sub(r"\s+", " ", _normalize_comparison_text(user_msg)).strip()
    menu_selections = {
        "1": "reposicion",
        "opcion 1": "reposicion",
        "1 reposicion": "reposicion",
        "2": "ofertas",
        "opcion 2": "ofertas",
        "2 ofertas": "ofertas",
        "3": "presupuesto",
        "opcion 3": "presupuesto",
        "3 presupuesto": "presupuesto",
    }
    msg = menu_selections.get(msg, msg)
    stock = get_stock()
    
    if any(w in msg for w in ["falta", "comprar", "critico", "agotado", "terminando", "reposicion", "reponer", "stock"]):
        criticos = [p for p in stock if p.get("stockQuantity", 0) <= 1]
        if not criticos:
            return "¡Buenas noticias! Tu despensa está bien abastecida y no tienes productos en nivel crítico en este momento."
        nombres = [f"• {p['name']} ({p.get('brand', 'Genérica')}): {p.get('stockQuantity', 0)} cerradas" for p in criticos]
        return f"Detecté {len(criticos)} producto(s) en estado crítico que necesitan reposición pronto:\n" + "\n".join(nombres) + "\n\n¿Quieres que comparemos ofertas en los supermercados de alguno de ellos?"
        
    if any(w in msg for w in ["presupuesto", "plata", "gasto", "gastos", "dinero", "ticket"]):
        from data.db import get_user_prefs
        prefs = get_user_prefs()
        budget = prefs.get("monthlyBudget", 0.0)
        spent = prefs.get("totalSpent", 0.0)
        remaining = budget - spent
        return (
            f"📊 **Estado Financiero del Mes:**\n"
            f"• Presupuesto mensual asignado: ${budget:,.2f}\n"
            f"• Gastos totales registrados: ${spent:,.2f}\n"
            f"• Saldo disponible: ${remaining:,.2f}\n"
            f"{'⚠️ ¡Cuidado! Estás cerca de superar tu presupuesto mensual.' if remaining < budget * 0.15 else '✅ Tu ritmo de gasto está controlado.'}"
        )
        
    if any(w in msg for w in ["oferta", "ofertas", "barato", "precio", "descuento", "supermercado"]):
        offers = get_offers()
        if not offers:
            return "Todavía no hay ofertas guardadas. Cargá una oferta en la app y sincronizá para consultarla acá."
        lines = [
            f"• {offer.get('product', 'Producto')} — {offer.get('store', 'Supermercado')}: "
            f"{offer.get('price') or 'falta cargar el precio'}"
            for offer in offers[:10]
        ]
        return "Estas son las ofertas guardadas y sincronizadas:\n" + "\n".join(lines)
        
    return (
        "¡Hola! Soy Boti House. Elegí una opción escribiendo el número o tocando un botón:\n"
        "1. Ver qué productos necesitan reposición.\n"
        "2. Consultar las ofertas guardadas.\n"
        "3. Ver el estado de tu presupuesto."
    )
