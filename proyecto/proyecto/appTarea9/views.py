"""
Vistas que demuestran los 5 atributos HTMX requeridos:
  1. hx-swap="none"    → registrar un "like" sin tocar el DOM
  2. hx-indicator      → spinner mientras se carga contenido lento
  3. hx-vals           → enviar datos extra sin campos de formulario
  4. hx-include        → incluir un input externo al disparador
  5. hx-swap-oob       → actualizar múltiples zonas del DOM a la vez
"""

import time
from django.shortcuts import render
from django.http import HttpResponse

# ── Estado en memoria (simula una BD) ────────────────────────────────────────
TAREAS = [
    {"id": 1, "texto": "Estudiar HTMX",       "hecha": False},
    {"id": 2, "texto": "Preparar el proyecto", "hecha": False},
    {"id": 3, "texto": "Subir a GitHub",       "hecha": False},
]
SIGUIENTE_ID = 4
LIKES = 0


# ── Página principal ──────────────────────────────────────────────────────────
def index(request):
    return render(request, "appTarea9/index.html", {
        "tareas": TAREAS,
        "likes":  LIKES,
    })


# ─────────────────────────────────────────────────────────────────────────────
# 1. hx-swap="none"
#    Registra un like en el servidor; HTMX descarta la respuesta por completo
#    y NO modifica el DOM. El efecto es puramente de lado servidor.
# ─────────────────────────────────────────────────────────────────────────────
def dar_like(request):
    global LIKES
    if request.method == "POST":
        LIKES += 1
    return HttpResponse("")   # respuesta vacía — hx-swap="none" la ignora


# ─────────────────────────────────────────────────────────────────────────────
# 2. hx-indicator
#    Simula trabajo pesado (2 s). Durante ese tiempo HTMX muestra
#    el elemento apuntado por hx-indicator (el spinner del template).
# ─────────────────────────────────────────────────────────────────────────────
def cargar_lento(request):
    time.sleep(2)
    html = """
    <ul class="lista-tareas">
      <li class="tarea-item">📦 Elemento cargado desde el servidor</li>
      <li class="tarea-item">📦 Segundo elemento cargado</li>
      <li class="tarea-item">📦 Tercer elemento cargado</li>
    </ul>
    """
    return HttpResponse(html)


# ─────────────────────────────────────────────────────────────────────────────
# 3. hx-vals
#    El botón envía {"prioridad": "alta"} o {"prioridad": "normal"}
#    sin que exista ningún <input> para ese campo en el HTML.
#    Django lo recibe igual, en request.POST.
# ─────────────────────────────────────────────────────────────────────────────
def agregar_con_prioridad(request):
    global SIGUIENTE_ID, TAREAS
    nueva = None
    if request.method == "POST":
        texto     = request.POST.get("texto_vals", "Nueva tarea")
        prioridad = request.POST.get("prioridad", "normal")
        etiqueta  = "🔴" if prioridad == "alta" else "🟡"
        nueva = {
            "id":    SIGUIENTE_ID,
            "texto": f"{etiqueta} [{prioridad.upper()}] {texto}",
            "hecha": False,
        }
        TAREAS.append(nueva)
        SIGUIENTE_ID += 1

    if nueva is None:
        return HttpResponse("")

    html = f'<li id="tarea-{nueva["id"]}" class="tarea-item">{nueva["texto"]}</li>'
    return HttpResponse(html)


# ─────────────────────────────────────────────────────────────────────────────
# 4. hx-include
#    El botón de búsqueda está FUERA del <input>. hx-include="#campo-busqueda"
#    le indica a HTMX que serialice ese input y lo adjunte al GET.
# ─────────────────────────────────────────────────────────────────────────────
def buscar(request):
    q = request.GET.get("q", "").strip().lower()
    resultados = [t for t in TAREAS if q in t["texto"].lower()] if q else TAREAS

    if not resultados:
        return HttpResponse('<p class="sin-resultados">Sin resultados.</p>')

    items = "".join(
        f'<li class="tarea-item {"hecha" if t["hecha"] else ""}">{t["texto"]}</li>'
        for t in resultados
    )
    return HttpResponse(f'<ul class="lista-tareas">{items}</ul>')


# ─────────────────────────────────────────────────────────────────────────────
# 5. hx-swap-oob
#    Al completar una tarea Django devuelve DOS fragmentos:
#      • El <li> actualizado  → target normal (outerHTML del <li>)
#      • El contador global   → hx-swap-oob="innerHTML" en el encabezado
# ─────────────────────────────────────────────────────────────────────────────
def completar_tarea(request, tarea_id):
    global TAREAS
    tarea = next((t for t in TAREAS if t["id"] == tarea_id), None)
    if tarea and request.method == "POST":
        tarea["hecha"] = True

    completadas = sum(1 for t in TAREAS if t["hecha"])

    html_principal = f"""
    <li id="tarea-{tarea_id}" class="tarea-item hecha">
      ✅ {tarea["texto"]} <em>(completada)</em>
    </li>
    """

    html_oob = f"""
    <span id="contador-oob" hx-swap-oob="innerHTML">
      {completadas} / {len(TAREAS)} completadas
    </span>
    """

    return HttpResponse(html_principal + html_oob)
