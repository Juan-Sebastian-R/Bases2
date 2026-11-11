# ProNet Graph - Aplicación de Red Profesional con Base de Datos de Grafos (Neo4j)

Aplicación web interactiva basada en **Neo4j** y **Flask** para la gestión, análisis de relaciones y recomendaciones en una red profesional.

---

## 🛠️ Tecnologías Utilizadas

- **Base de Datos de Grafos:** Neo4j (Cypher)
- **Backend:** Python 3 + Flask + neo4j driver
- **Frontend:** Bootstrap 5 (Dark theme), vis.js (Network Visualization), Chart.js
- **Iconografía:** Font Awesome 6

---

## 📐 Modelo del Grafo

### Nodos (Entidades)
| Nodo | Propiedades Principales |
|---|---|
| `Usuario` | `id`, `nombre`, `email`, `titulo`, `ubicacion`, `resumen` |
| `Empresa` | `id`, `nombre`, `industria`, `ubicacion`, `descripcion`, `sitio_web` |
| `Habilidad` | `id`, `nombre`, `categoria` |
| `Proyecto` | `id`, `nombre`, `descripcion`, `estado`, `fecha_inicio` |
| `Oferta` | `id`, `titulo`, `descripcion`, `modalidad`, `salario`, `fecha_publicacion` |

### Relaciones
| Relación | Nodos Involucrados | Propiedades |
|---|---|---|
| `CONECTA_CON` | `(Usuario)-[:CONECTA_CON]->(Usuario)` | Conexión profesional directa |
| `TRABAJA_EN` | `(Usuario)-[:TRABAJA_EN]->(Empresa)` | `cargo`, `fecha_inicio` |
| `TIENE_HABILIDAD`| `(Usuario)-[:TIENE_HABILIDAD]->(Habilidad)` | Competencia que posee el usuario |
| `PARTICIPA_EN` | `(Usuario)-[:PARTICIPA_EN]->(Proyecto)` | `rol` |
| `PUBLICA` | `(Empresa)-[:PUBLICA]->(Oferta)` | Vacante laboral publicada |
| `REQUIERE` | `(Oferta)-[:REQUIERE]->(Habilidad)` | Requisito técnico de la vacante |
| `POSTULA_A` | `(Usuario)-[:POSTULA_A]->(Oferta)` | `fecha` |

---

## 🚀 Instalación y Puesta en Marcha

### 1. Requisitos Previos
- Python 3.10+
- Instancia activa de **Neo4j** (Neo4j Desktop, Docker o Neo4j AuraDB).
  - Por defecto: `bolt://localhost:7687`, usuario: `neo4j`, contraseña: `neo4j`.

### 2. Configurar Entorno
```bash
# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
venv\Scripts\activate   # en Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar Credenciales
Editar el archivo `.env` según tus credenciales de Neo4j:
```ini
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j
```

### 4. Inicializar la Base de Datos con Datos de Prueba
Ejecutar el script de inicialización con 15 usuarios, 6 empresas, 20 habilidades, 5 proyectos, 8 ofertas y múltiples relaciones:
```bash
python init_db.py
```

### 5. Iniciar la Aplicación
```bash
python app.py
```
Abrir en el navegador: [http://localhost:5000](http://localhost:5000)

---

## 🌟 Funcionalidades Implementadas

1. **Gestión CRUD Completa:**
   - Usuarios, Empresas, Habilidades, Proyectos y Ofertas laborales.
2. **Gestión de Relaciones:**
   - Conectar usuarios, registrar experiencia en empresas, asignar habilidades, vincular proyectos y postulación a vacantes.
3. **Motor de Recomendación Basado en Grafos:**
   - Recomendación de contactos profesionales (amigos de amigos).
   - Usuarios con habilidades similares.
   - Contactos en común entre dos profesionales.
   - Empleos recomendados según las habilidades del usuario.
   - Ruta más corta (`shortestPath`) entre un usuario y una empresa.
4. **Panel de Analítica:**
   - Usuarios más influyentes (centralidad de grado ponderada).
   - Detección de comunidades / clusters de usuarios conectados.
   - Habilidades más demandadas por el mercado laboral.
5. **Visualización Interactiva del Grafo (`vis.js`):**
   - Explorador visual en tiempo real.
   - Filtros por tipo de nodo, búsqueda, simulación de física y panel de inspección.

---

## 📁 Estructura del Proyecto

```
Bases2/
├── app.py                   # Servidor Flask y endpoints REST
├── database.py              # Capa de datos con Neo4j Driver y consultas Cypher
├── init_db.py               # Script de carga inicial con datos de prueba
├── requirements.txt         # Dependencias de Python
├── .env                     # Variables de entorno
├── scripts/
│   └── consultas.cypher     # Colección de queries Cypher para el reporte
├── static/
│   ├── css/
│   │   └── style.css        # Estilos personalizados (Dark Theme)
│   └── js/
│       └── app.js           # Utilidades frontend, toasts y vis.js
└── templates/
    ├── base.html            # Layout maestro con navbar y scripts CDN
    ├── index.html           # Dashboard principal
    ├── usuarios.html        # Gestión y listado de usuarios
    ├── usuario_detalle.html # Perfil, ego-graph y recomendaciones
    ├── empresas.html        # Gestión de empresas y vacantes asociadas
    ├── habilidades.html     # Catálogo de competencias por categoría
    ├── proyectos.html       # Proyectos e integrantes
    ├── ofertas.html         # Ofertas laborales, postulaciones y requisitos
    ├── analitica.html       # Métricas, Chart.js y comunidades
    └── grafo.html           # Visualizador de grafos interactivo
```

