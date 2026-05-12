"""
DATABASE - Sistema de Incidencias
Guarda incidencias en archivo JSON
"""

import json
import os
from datetime import datetime

# Archivo de base de datos
DB_FILE = "incidencias.json"


# ==========================================
# CARGAR DATOS
# ==========================================
def load_data():
    """Carga incidencias desde JSON"""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data["issues"], data["next_id"]
        except:
            return [], 1
    return [], 1


# Cargar al iniciar
issues_db, next_id = load_data()


# ==========================================
# GUARDAR DATOS
# ==========================================
def save_data():
    global next_id

    data = {
        "issues": issues_db,
        "next_id": next_id,
        "last_save": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ==========================================
# CRUD
# ==========================================
def add_task(issue):
    """Agregar incidencia"""
    issues_db.append(issue)
    save_data()


def update_task(issue_id, updates):
    """Actualizar incidencia"""
    for issue in issues_db:
        if issue["id"] == issue_id:
            issue.update(updates)
            save_data()
            return True
    return False


def get_all_tasks():
    """Obtener todas las incidencias"""
    return issues_db


def increment_next_id():
    """Incrementar ID"""
    global next_id
    next_id += 1
    save_data()
    return next_id - 1


def delete_task(issue_id):
    """Eliminar incidencia"""
    global issues_db
    for i, issue in enumerate(issues_db):
        if issue["id"] == issue_id:
            issues_db.pop(i)
            save_data()
            return True
    return False