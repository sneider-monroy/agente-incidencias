"""
PASO 2: DEFINIR LAS HERRAMIENTAS
Herramientas del agente de incidencias (Compatible con OpenAI)
"""

tools = [
    {
        "type": "function",
        "function": {
            "name": "create_issue",
            "description": "Registra una nueva incidencia (bug) con título, descripción y prioridad",
            "parameters": {
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
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_issues",
            "description": "Lista incidencias o filtra por estado o prioridad",
            "parameters": {
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
        }
    },
    {
        "type": "function",
        "function": {
            "name": "resolve_issue",
            "description": "Marca una incidencia como resuelta",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID de la incidencia"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_statistics",
            "description": "Obtiene estadísticas de incidencias",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]