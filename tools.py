"""
PASO 2: DEFINIR LAS HERRAMIENTAS
Herramientas del agente de incidencias
"""

tools = [
    {
        "name": "create_issue",
        "description": "Registra una nueva incidencia (bug) con título, descripción y prioridad",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Nombre del error o bug"
                },
                "description": {
                    "type": "string",
                    "description": "Descripción detallada del problema"
                },
                "priority": {
                    "type": "string",
                    "enum": ["Alta", "Media", "Baja"],
                    "description": "Nivel de urgencia"
                }
            },
            "required": ["title", "priority"]
        }
    },
    {
        "name": "list_issues",
        "description": "Lista incidencias o filtra por estado o prioridad",
        "input_schema": {
            "type": "object",
            "properties": {
                "filter": {
                    "type": "string",
                    "enum": ["todas", "alta", "media", "baja", "resueltas", "pendientes"],
                    "description": "Tipo de filtro"
                }
            },
            "required": ["filter"]
        }
    },
    {
        "name": "resolve_issue",
        "description": "Marca una incidencia como resuelta",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "ID de la incidencia"
                }
            },
            "required": ["task_id"]
        }
    },
    {
        "name": "get_statistics",
        "description": "Obtiene estadísticas de incidencias",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    }
]
