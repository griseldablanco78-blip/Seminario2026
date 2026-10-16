"""
Persistencia unificada de datos para Expensa House.
Sincroniza el inventario, compras, ofertas y presupuesto entre la Web y la App Android.
Exporta automáticamente a data/stock.json para retrocompatibilidad con dashboards existentes.
"""
import json
import os
import uuid
import time
import pandas as pd
from typing import List, Dict, Any, Optional

DB_FILE = os.path.join(os.path.dirname(__file__), "app_state.json")
STOCK_JSON = os.path.join(os.path.dirname(__file__), "stock.json")
STOCK_CSV = os.path.join(os.path.dirname(__file__), "stock.csv")
CSV_CLEAN = os.path.join(os.path.dirname(__file__), "inventario_movimientos_limpio.csv")

INITIAL_DATA = {
    "stock": [],
    "shopping": [],
    "user_prefs": {
        "id": 0,
        "monthlyBudget": 0.0,
        "totalSpent": 0.0
    },
    "expenses": [],
    "offers": [],
    "last_sync": int(time.time() * 1000)
}

def load_db() -> Dict[str, Any]:
    if not os.path.exists(DB_FILE):
        save_db(INITIAL_DATA)
        return INITIAL_DATA
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure keys exist
            for key in ["stock", "shopping", "user_prefs", "expenses", "offers"]:
                if key not in data:
                    data[key] = INITIAL_DATA.get(key, [])
            return data
    except Exception as e:
        print(f"Error cargando DB, reestableciendo estado: {e}")
        save_db(INITIAL_DATA)
        return INITIAL_DATA

def save_db(data: Dict[str, Any]):
    data["last_sync"] = int(time.time() * 1000)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    export_to_legacy_formats(data)

def export_to_legacy_formats(data: Dict[str, Any]):
    """Exporta a data/stock.json y data/stock.csv para compatibilidad total con dashboard.py."""
    try:
        stock_items = data.get("stock", [])
        legacy_list = []
        for item in stock_items:
            legacy_list.append({
                "name": item.get("name", "Producto"),
                "brand": item.get("brand", "Genérica"),
                "category": item.get("category", "Comestibles"),
                "stockQuantity": int(item.get("stockQuantity", 0)),
                "inUseCount": int(item.get("inUseCount", 0)),
                "price": float(item.get("price", 0.0)),
                "unit": item.get("unit", "unidad")
            })
        with open(STOCK_JSON, "w", encoding="utf-8") as f:
            json.dump(legacy_list, f, ensure_ascii=False, indent=2)
            
        df = pd.DataFrame(legacy_list)
        df.to_csv(STOCK_CSV, index=False)
    except Exception as e:
        print(f"Error exportando formatos legacy: {e}")

# Funciones de acceso rápido
def get_stock() -> List[Dict[str, Any]]:
    db = load_db()
    return db.get("stock", [])

def add_or_update_stock_item(item: Dict[str, Any]) -> Dict[str, Any]:
    db = load_db()
    if not item.get("id"):
        item["id"] = str(uuid.uuid4())
    
    # Check if exists
    existing_idx = next((i for i, x in enumerate(db["stock"]) if x["id"] == item["id"]), None)
    if existing_idx is not None:
        db["stock"][existing_idx].update(item)
        saved_item = db["stock"][existing_idx]
    else:
        db["stock"].append(item)
        saved_item = item
        
    # Auto-sync with shopping list if critical
    check_and_sync_shopping_for_stock(db, saved_item)
    save_db(db)
    return saved_item

def check_and_sync_shopping_for_stock(db: Dict[str, Any], stock_item: Dict[str, Any]):
    stock_qty = stock_item.get("stockQuantity", 0)
    name = stock_item.get("name", "").strip().lower()
    
    if stock_qty <= 1:
        # Check if already in shopping
        exists = any(s.get("name", "").strip().lower() == name for s in db["shopping"])
        if not exists:
            db["shopping"].append({
                "id": str(uuid.uuid4()),
                "name": stock_item.get("name"),
                "brand": stock_item.get("brand", "Genérica"),
                "category": stock_item.get("category", "Comestibles"),
                "detail": "Reposición automática (stock crítico)",
                "quantity": 1,
                "suggestedStore": None,
                "checked": False
            })

def delete_stock_item(item_id: str) -> bool:
    db = load_db()
    original_len = len(db["stock"])
    db["stock"] = [x for x in db["stock"] if x["id"] != item_id]
    if len(db["stock"]) < original_len:
        save_db(db)
        return True
    return False

def open_stock_unit(item_id: str) -> Optional[Dict[str, Any]]:
    db = load_db()
    for item in db["stock"]:
        if item["id"] == item_id:
            if item.get("stockQuantity", 0) > 0:
                item["stockQuantity"] = item["stockQuantity"] - 1
                item["inUseCount"] = item.get("inUseCount", 0) + 1
                check_and_sync_shopping_for_stock(db, item)
                save_db(db)
                return item
    return None

def consume_stock_unit(item_id: str) -> Optional[Dict[str, Any]]:
    db = load_db()
    for item in db["stock"]:
        if item["id"] == item_id:
            if item.get("inUseCount", 0) > 0:
                item["inUseCount"] = item["inUseCount"] - 1
                save_db(db)
                return item
    return None

def get_shopping() -> List[Dict[str, Any]]:
    db = load_db()
    return db.get("shopping", [])

def add_shopping_item(item: Dict[str, Any]) -> Dict[str, Any]:
    db = load_db()
    if not item.get("id"):
        item["id"] = str(uuid.uuid4())
    db["shopping"].append(item)
    save_db(db)
    return item

def update_shopping_item(item_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    db = load_db()
    for item in db["shopping"]:
        if item["id"] == item_id:
            item.update(updates)
            save_db(db)
            return item
    return None

def delete_shopping_item(item_id: str) -> bool:
    db = load_db()
    original_len = len(db["shopping"])
    db["shopping"] = [x for x in db["shopping"] if x["id"] != item_id]
    if len(db["shopping"]) < original_len:
        save_db(db)
        return True
    return False

def move_shopping_to_stock(item_id: str) -> Optional[Dict[str, Any]]:
    db = load_db()
    shop_item = next((x for x in db["shopping"] if x["id"] == item_id), None)
    if not shop_item:
        return None
    
    # Check if item exists in stock
    name = shop_item.get("name", "").strip().lower()
    brand = shop_item.get("brand", "").strip().lower()
    qty = shop_item.get("quantity", 1)
    
    existing = next((s for s in db["stock"] if s.get("name", "").strip().lower() == name and s.get("brand", "").strip().lower() == brand), None)
    if existing:
        existing["stockQuantity"] = existing.get("stockQuantity", 0) + qty
        result_stock = existing
    else:
        new_item = {
            "id": str(uuid.uuid4()),
            "name": shop_item.get("name"),
            "brand": shop_item.get("brand", "Genérica"),
            "category": shop_item.get("category", "Comestibles"),
            "stockQuantity": qty,
            "inUseCount": 0,
            "unit": "unidad",
            "price": 0.0
        }
        db["stock"].append(new_item)
        result_stock = new_item
        
    db["shopping"] = [x for x in db["shopping"] if x["id"] != item_id]
    save_db(db)
    return result_stock

def get_user_prefs() -> Dict[str, Any]:
    db = load_db()
    return db.get("user_prefs", {"monthlyBudget": 0.0, "totalSpent": 0.0})

def update_user_prefs(prefs: Dict[str, Any]) -> Dict[str, Any]:
    db = load_db()
    db["user_prefs"].update(prefs)
    save_db(db)
    return db["user_prefs"]

def get_expenses() -> List[Dict[str, Any]]:
    db = load_db()
    return db.get("expenses", [])

def add_expense(expense: Dict[str, Any]) -> Dict[str, Any]:
    db = load_db()
    if not expense.get("id"):
        expense["id"] = str(uuid.uuid4())
    if not expense.get("timestamp"):
        expense["timestamp"] = int(time.time() * 1000)
    db["expenses"].insert(0, expense)
    
    # Actualizar totalSpent en user_prefs
    db["user_prefs"]["totalSpent"] = db["user_prefs"].get("totalSpent", 0.0) + expense.get("amount", 0.0)
    save_db(db)
    return expense

def get_offers() -> List[Dict[str, Any]]:
    db = load_db()
    return db.get("offers", [])

def add_offer(offer: Dict[str, Any]) -> Dict[str, Any]:
    db = load_db()
    if not offer.get("id"):
        offer["id"] = str(uuid.uuid4())
    db["offers"].insert(0, offer)
    save_db(db)
    return offer

# Inicializar exportación al importar
load_db()
