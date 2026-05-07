"""
PASO 4: FUNCIONES DEL AGENTE
Sistema de incidencias de software
"""

from datetime import datetime
from database import get_all_tasks, add_task, update_task, increment_next_id

# ==========================================
# FUNCIÓN 1: Crear incidencia
# ==========================================
def create_issue(title, description, priority):
    """
    Crear una incidencia (bug)
    """

    issue_id = increment_next_id()

    new_issue = {
        "id": issue_id,
        "title": f"🐛 {title}",
        "description": description if description else "(sin descripción)",
        "priority": priority,
        "completed": False,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    add_task(new_issue)

    return {
        "status": "✅ Incidencia creada",
        "issue_id": issue_id,
        "title": title,
        "priority": priority
    }


# ==========================================
# FUNCIÓN 2: Listar incidencias
# ==========================================
def list_issues(filter_type="todas"):

    issues = get_all_tasks()

    if filter_type == "todas":
        result = issues
    elif filter_type == "alta":
        result = [i for i in issues if i["priority"] == "Alta"]
    elif filter_type == "media":
        result = [i for i in issues if i["priority"] == "Media"]
    elif filter_type == "baja":
        result = [i for i in issues if i["priority"] == "Baja"]
    elif filter_type == "resueltas":
        result = [i for i in issues if i["completed"]]
    elif filter_type == "pendientes":
        result = [i for i in issues if not i["completed"]]
    else:
        result = []

    formatted = []

    for i in result:
        estado = "✅ Resuelta" if i["completed"] else "⏳ Pendiente"

        formatted.append({
            "id": i["id"],
            "titulo": i["title"],
            "prioridad": i["priority"],
            "estado": estado,
            "descripcion": i["description"]
        })

    return {
        "filtro": filter_type,
        "cantidad": len(formatted),
        "incidencias": formatted
    }


# ==========================================
# FUNCIÓN 3: Resolver incidencia
# ==========================================
def resolve_issue(issue_id):

    issues = get_all_tasks()

    issue = next((i for i in issues if i["id"] == issue_id), None)

    if issue:
        update_task(issue_id, {"completed": True})
        return {
            "status": f"✅ Incidencia {issue_id} resuelta",
            "title": issue["title"]
        }
    else:
        return {
            "error": f"❌ No encontré la incidencia {issue_id}"
        }


# ==========================================
# FUNCIÓN 4: Estadísticas
# ==========================================
def get_statistics():

    issues = get_all_tasks()

    total = len(issues)
    resolved = sum(1 for i in issues if i["completed"])
    pending = total - resolved

    by_priority = {
        "Alta": sum(1 for i in issues if i["priority"] == "Alta" and not i["completed"]),
        "Media": sum(1 for i in issues if i["priority"] == "Media" and not i["completed"]),
        "Baja": sum(1 for i in issues if i["priority"] == "Baja" and not i["completed"])
    }

    return {
        "total_tareas": total,
        "tareas_completadas": resolved,
        "tareas_pendientes": pending,
        "pendientes_por_prioridad": by_priority,
        "porcentaje_completado": f"{(resolved/total*100):.1f}%" if total > 0 else "0%"
    }
