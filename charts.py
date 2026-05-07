"""
CHARTS.PY - Gráficos de Incidencias
Visualización con Matplotlib
"""

import matplotlib.pyplot as plt
import matplotlib
from database import get_all_tasks
import io
import base64

# Backend sin interfaz
matplotlib.use('Agg')

plt.style.use('seaborn-v0_8-darkgrid')


# ==========================================
# GRÁFICO 1: Estado de Incidencias
# ==========================================
def generate_pie_chart():

    issues = get_all_tasks()

    if not issues:
        return None

    resolved = sum(1 for i in issues if i["completed"])
    pending = len(issues) - resolved

    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor('#f8f9fa')

    labels = ['✅ Resueltas', '⏳ Pendientes']
    sizes = [resolved, pending]
    colors = ['#2ecc71', '#e74c3c']

    ax.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        shadow=True,
        textprops={'fontsize': 12, 'weight': 'bold'}
    )

    ax.set_title('Estado de Incidencias', fontsize=16, weight='bold')

    return convertir_img()


# ==========================================
# GRÁFICO 2: Prioridad
# ==========================================
def generate_priority_chart():

    issues = get_all_tasks()

    if not issues:
        return None

    alta = sum(1 for i in issues if i["priority"] == "Alta" and not i["completed"])
    media = sum(1 for i in issues if i["priority"] == "Media" and not i["completed"])
    baja = sum(1 for i in issues if i["priority"] == "Baja" and not i["completed"])

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#f8f9fa')

    labels = ['🔴 Alta', '🟡 Media', '🟢 Baja']
    values = [alta, media, baja]
    colors = ['#e74c3c', '#f39c12', '#2ecc71']

    bars = ax.bar(labels, values, color=colors)

    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height(),
                int(bar.get_height()),
                ha='center', va='bottom')

    ax.set_title('Incidencias Pendientes por Prioridad', fontsize=16)

    return convertir_img()


# ==========================================
# GRÁFICO 3: Progreso
# ==========================================
def generate_progress_chart():

    issues = get_all_tasks()

    if not issues:
        return None

    total = len(issues)
    resolved = sum(1 for i in issues if i["completed"])
    percentage = (resolved / total * 100) if total else 0

    fig, ax = plt.subplots(figsize=(10, 2))
    fig.patch.set_facecolor('#f8f9fa')

    ax.barh(['Progreso'], [percentage], color='#3498db')
    ax.barh(['Progreso'], [100 - percentage], left=[percentage], color='#ecf0f1')

    ax.text(50, 0,
            f'{percentage:.1f}% ({resolved}/{total})',
            ha='center', va='center',
            fontsize=12, weight='bold')

    ax.axis('off')
    ax.set_title('Progreso de Resolución', fontsize=14)

    return convertir_img()


# ==========================================
# CONVERTIR IMAGEN
# ==========================================
def convertir_img():
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    encoded = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return f"data:image/png;base64,{encoded}"


# ==========================================
# TODOS LOS GRÁFICOS
# ==========================================
def get_all_charts():
    return {
        "pie": generate_pie_chart(),
        "priority": generate_priority_chart(),
        "progress": generate_progress_chart()
    }
