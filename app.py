import datetime
import random

import pandas as pd
import streamlit as st

# ==========================
# CONFIG GENERAL
# ==========================

st.set_page_config(
    page_title="Plataforma de Analíticas del Municipio",
    page_icon="📊",
    layout="wide"
)

# CSS para look más claro / institucional
st.markdown(
    """
    <style>
    /* Fondo general claro */
    .stApp {
        background-color: #f5f5f5 !important;
    }

    /* Contenedor central tipo tarjeta grande */
    .main-block {
        background-color: #ffffff;
        padding: 20px 30px 30px 30px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 18px;
    }

    .big-title {
        font-size: 28px !important;
        font-weight: 800 !important;
        margin-bottom: 0px;
        color: #1b3b5a !important;
    }
    .sub-title {
        font-size: 14px !important;
        color: #555555 !important;
        margin-top: 4px;
        margin-bottom: 0px;
    }

    .gov-bar {
        height: 6px;
        background: linear-gradient(90deg, #006847 0%, #ffffff 50%, #ce1126 100%);
        border-radius: 6px;
        margin-bottom: 14px;
    }

    .metric-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 12px 14px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    .metric-label {
        font-size: 12px;
        color: #666666;
    }
    .metric-value {
        font-size: 22px;
        font-weight: 700;
        color: #1b3b5a;
    }
    .metric-sub {
        font-size: 11px;
        color: #888888;
    }

    .section-title {
        font-size: 18px;
        font-weight: 700;
        color: #1b3b5a;
        margin-top: 10px;
        margin-bottom: 4px;
    }

    .module-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 12px 14px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
        font-size: 13px;
        color: #444444;
        height: 100%;
    }

    .module-title {
        font-weight: 700;
        margin-bottom: 6px;
        color: #1b3b5a;
    }

    /* Sidebar más claro */
    section[data-testid="stSidebar"] {
        background-color: #f0f2f6 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="gov-bar"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="big-title">Plataforma de Analíticas del Municipio</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">Visualización centralizada de reportes ciudadanos, encuestas y desempeño de atención.</div>',
    unsafe_allow_html=True,
)
st.write("")


# ==========================
# GENERAR DATOS FAKE
# ==========================

def generar_datos_fake(num_reportes=150, num_encuestas=80, dias_atras=90):
    hoy = datetime.date.today()
    categorias = ["Seguridad", "Bacheo", "Alumbrado", "Limpieza"]
    colonias = ["Colonia Centro", "Colonia Norte", "Colonia Sur", "Colonia Oriente", "Colonia Poniente"]
    estatus_list = ["abierto", "en_proceso", "resuelto"]
    prioridad_list = ["baja", "media", "alta"]
    canales = ["whatsapp", "web", "facebook", "telegram"]
    fuentes = ["chatbot", "manual"]

    # --- Reportes ---
    reportes = []
    for i in range(num_reportes):
        dias = random.randint(0, dias_atras)
        fecha = hoy - datetime.timedelta(days=dias)
        estatus = random.choices(estatus_list, weights=[0.4, 0.3, 0.3])[0]

        # simulamos que resueltos tardan 1–10 días
        if estatus == "resuelto":
            tiempo_respuesta = random.randint(1, 10)
        else:
            tiempo_respuesta = None

        reportes.append({
            "id": i + 1,
            "folio": f"MUN-{fecha.strftime('%Y%m%d')}-{i:04d}",
            "categoria": random.choice(categorias),
            "colonia": random.choice(colonias),
            "estatus": estatus,
            "prioridad": random.choices(prioridad_list, weights=[0.3, 0.5, 0.2])[0],
            "canal": random.choice(canales),
            "fuente": random.choice(fuentes),
            "descripcion": "Descripción del reporte ciudadano número " + str(i + 1),
            "created_at": datetime.datetime.combine(fecha, datetime.time(hour=random.randint(8, 22))),
            "tiempo_respuesta_dias": tiempo_respuesta,
        })

    reportes_df = pd.DataFrame(reportes)

    # --- Encuestas ---
    temas = [
        "Percepción de seguridad",
        "Limpieza de calles",
        "Alumbrado público",
        "Estado de las vialidades",
    ]
    encuestas = []
    for i in range(num_encuestas):
        dias = random.randint(0, dias_atras)
        fecha = hoy - datetime.timedelta(days=dias)
        encuestas.append({
            "id": i + 1,
            "tema": random.choice(temas),
            "categoria": "Percepción de servicios",
            "colonia": random.choice(colonias),
            "score": round(random.uniform(1.8, 4.8), 2),
            "canal": random.choice(canales),
            "created_at": datetime.datetime.combine(fecha, datetime.time(hour=random.randint(8, 22))),
        })

    encuestas_df = pd.DataFrame(encuestas)

    return reportes_df, encuestas_df


@st.cache_data
def get_fake_data():
    return generar_datos_fake()


reportes_df, encuestas_df = get_fake_data()


# ==========================
# SIDEBAR – FILTROS
# ==========================

st.sidebar.title("🎛 Filtros")

today = datetime.date.today()
default_start = today - datetime.timedelta(days=60)

start_date = st.sidebar.date_input("Fecha inicial", value=default_start)
end_date = st.sidebar.date_input("Fecha final", value=today)

if start_date > end_date:
    st.sidebar.error("La fecha inicial no puede ser mayor a la fecha final.")

estatus_options = ["abierto", "en_proceso", "resuelto"]
selected_status = st.sidebar.multiselect(
    "Estatus",
    options=estatus_options,
    default=estatus_options,
)

st.sidebar.markdown("---")
st.sidebar.caption("Datos simulados con fines de demostración institucional.")


# ==========================
# APLICAR FILTROS
# ==========================

rep = reportes_df.copy()
enc = encuestas_df.copy()

rep = rep[(rep["created_at"].dt.date >= start_date) & (rep["created_at"].dt.date <= end_date)]
enc = enc[(enc["created_at"].dt.date >= start_date) & (enc["created_at"].dt.date <= end_date)]

if selected_status:
    rep = rep[rep["estatus"].isin(selected_status)]


# ==========================
# BLOQUE PRINCIPAL
# ==========================

with st.container():
    st.markdown('<div class="main-block">', unsafe_allow_html=True)

    # ======== KPIs PRINCIPALES (tarjetas) ========
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)

    if rep.empty:
        total_rep = 0
        abiertos = en_proceso = resueltos = 0
        tasa_resolucion = 0
        tiempo_promedio = 0
    else:
        total_rep = len(rep)
        abiertos = (rep["estatus"] == "abierto").sum()
        en_proceso = (rep["estatus"] == "en_proceso").sum()
        resueltos = (rep["estatus"] == "resuelto").sum()
        tasa_resolucion = round((resueltos / total_rep) * 100, 1) if total_rep > 0 else 0
        tiempos = rep["tiempo_respuesta_dias"].dropna()
        tiempo_promedio = round(tiempos.mean(), 1) if len(tiempos) > 0 else 0

    with col_k1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Reportes registrados</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{total_rep}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-sub">En el periodo seleccionado</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_k2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Tasa de resolución</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{tasa_resolucion}%</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-sub">Reportes marcados como resueltos</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_k3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Tiempo promedio de atención</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{tiempo_promedio} días</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-sub">Solo reportes resueltos</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # KPI fijo “índice de satisfacción” basado en encuestas fake
    if enc.empty:
        indice_satisfaccion = 0
    else:
        indice_satisfaccion = round((enc["score"].mean() / 5) * 100, 1)

    with col_k4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Índice de satisfacción ciudadana</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{indice_satisfaccion}%</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-sub">Promedio de encuestas del periodo</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("")

    # ======== MÓDULOS DE LA PLATAFORMA (texto fijo chulo) ========
    st.markdown('<div class="section-title">Módulos de la plataforma</div>', unsafe_allow_html=True)
    mod1, mod2, mod3 = st.columns(3)

    with mod1:
        st.markdown(
            """
            <div class="module-card">
              <div class="module-title">📲 Atención ciudadana omnicanal</div>
              Registro unificado de reportes provenientes de WhatsApp, chat web y otros canales digitales,
              con clasificación automática por categoría y colonia.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with mod2:
        st.markdown(
            """
            <div class="module-card">
              <div class="module-title">📌 Gestión y seguimiento de reportes</div>
              Visualización de estatus (abierto, en proceso, resuelto), prioridades y tiempos de atención
              para cada reporte, facilitando la coordinación entre áreas operativas.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with mod3:
        st.markdown(
            """
            <div class="module-card">
              <div class="module-title">📈 Analítica para toma de decisiones</div>
              Indicadores clave por categoría y colonia, análisis de tendencias y nivel
              de satisfacción ciudadana para respaldar decisiones de política pública.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")

    # ==========================
    # TABS PRINCIPALES
    # ==========================
    tab_overview, tab_reportes, tab_encuestas = st.tabs(
        ["🌎 Visión general", "📍 Detalle de reportes", "📝 Encuestas ciudadanas"]
    )

    # ---------- TAB 1 – VISIÓN GENERAL ----------
    with tab_overview:
        st.markdown('<div class="section-title">Visión general del municipio</div>', unsafe_allow_html=True)

        if rep.empty:
            st.info("No hay reportes para los filtros seleccionados (en estos datos simulados).")
        else:
            col_a, col_b = st.columns(2)

            # Reportes por categoría
            rep_cat = rep.groupby("categoria")["id"].count().reset_index()
            rep_cat = rep_cat.rename(columns={"id": "total_reportes"})
            rep_cat = rep_cat.sort_values("total_reportes", ascending=False)

            with col_a:
                st.markdown("**Reportes por categoría**")
                st.bar_chart(
                    rep_cat.set_index("categoria")["total_reportes"]
                )

            # Top colonias
            rep_colonia = rep.groupby("colonia")["id"].count().reset_index()
            rep_colonia = rep_colonia.rename(columns={"id": "total_reportes"})
            rep_colonia = rep_colonia.sort_values("total_reportes", ascending=False).head(10)

            with col_b:
                st.markdown("**Colonias con mayor número de reportes**")
                st.bar_chart(
                    rep_colonia.set_index("colonia")["total_reportes"]
                )

            # Serie de tiempo
            st.markdown("### Evolución de reportes en el tiempo")
            tmp = rep.copy()
            tmp["fecha"] = tmp["created_at"].dt.date
            rep_dia = tmp.groupby("fecha")["id"].count().reset_index()
            rep_dia = rep_dia.rename(columns={"id": "total_reportes"})
            rep_dia = rep_dia.sort_values("fecha")

            st.line_chart(rep_dia.set_index("fecha")["total_reportes"])

    # ---------- TAB 2 – DETALLE REPORTES ----------
    with tab_reportes:
        st.markdown('<div class="section-title">Detalle de reportes ciudadanos</div>', unsafe_allow_html=True)

        if rep.empty:
            st.info("No hay reportes para los filtros seleccionados.")
        else:
            # Quick stats por canal
            st.markdown("**Distribución por canal de contacto**")
            rep_canal = rep.groupby("canal")["id"].count().reset_index()
            rep_canal = rep_canal.rename(columns={"id": "total_reportes"})
            rep_canal = rep_canal.sort_values("total_reportes", ascending=False)

            col_c, col_d = st.columns([1, 2])

            with col_c:
                st.bar_chart(rep_canal.set_index("canal")["total_reportes"])

            with col_d:
                st.markdown(
                    f"- Canales con más reportes: **{', '.join(rep_canal['canal'].tolist())}**  \n"
                    f"- Total de reportes en el periodo: **{len(rep)}**"
                )

            st.markdown("### Tabla de reportes")
            st.dataframe(
                rep[
                    [
                        "folio",
                        "categoria",
                        "colonia",
                        "estatus",
                        "prioridad",
                        "canal",
                        "fuente",
                        "descripcion",
                        "created_at",
                    ]
                ],
                use_container_width=True,
                hide_index=True,
            )

    # ---------- TAB 3 – ENCUESTAS ----------
    with tab_encuestas:
        st.markdown('<div class="section-title">Resultados de encuestas ciudadanas</div>', unsafe_allow_html=True)

        if enc.empty:
            st.info("No hay encuestas para los filtros seleccionados.")
        else:
            enc["score"] = pd.to_numeric(enc["score"], errors="coerce")
            enc = enc.dropna(subset=["score"])

            col_e, col_f = st.columns(2)

            avg_global = enc["score"].mean()
            total_encuestas = len(enc)

            with col_e:
                st.metric("Promedio global de satisfacción", f"{avg_global:.2f} / 5")
            with col_f:
                st.metric("Total de encuestas levantadas", total_encuestas)

            st.markdown("")

            # Promedio por colonia
            avg_col = (
                enc.groupby("colonia")["score"]
                .mean()
                .reset_index()
                .sort_values("score", ascending=False)
            )

            st.markdown("**Satisfacción promedio por colonia**")
            st.bar_chart(avg_col.set_index("colonia")["score"])

            st.markdown("### Detalle de encuestas")
            st.dataframe(
                enc[
                    [
                        "tema",
                        "colonia",
                        "score",
                        "canal",
                        "created_at",
                    ]
                ],
                use_container_width=True,
                hide_index=True,
            )

    st.markdown('</div>', unsafe_allow_html=True)  # cierre main-block

st.markdown("---")
st.caption("Plataforma de Analíticas del Municipio · Ejemplo demostrativo con datos simulados.")
