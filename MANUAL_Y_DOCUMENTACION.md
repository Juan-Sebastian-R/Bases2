# 📘 Documentación Técnica, Manual de Usuario y Matriz de Cumplimiento
## Plataforma de Gestión y Análisis de Red Profesional con Base de Datos de Grafos (Neo4j)

---

## 📋 1. Checklist de Cumplimiento de Requerimientos

| Requerimiento del Enunciado | Estado | Implementación en la Aplicación |
|---|:---:|---|
| **CRUD de Usuarios con información personal y profesional** | ✅ Cumple | Rutas `/usuarios`, API REST `/api/usuarios`, modal de creación y edición, eliminación con borrado en cascada en grafo (`DETACH DELETE`). |
| **Relación entre usuarios (CONECTA_CON)** | ✅ Cumple | En `/usuarios/<id>`, módulo interactivo de "Conexiones Profesionales" que permite enlazar y desenlazar usuarios. |
| **Vincular usuarios con habilidades (TIENE_HABILIDAD)** | ✅ Cumple | En `/usuarios/<id>`, sección para asignar y retirar competencias técnicas del catálogo. |
| **Vincular usuarios con empresas (TRABAJA_EN)** | ✅ Cumple | En `/usuarios/<id>`, registro de experiencia laboral con cargo, fecha de inicio, fecha de fin y estado actual vinculado a una empresa del grafo. |
| **Vincular usuarios con proyectos (PARTICIPA_EN)** | ✅ Cumple | En `/proyectos` y `/usuarios/<id>`, asignación de roles y participación activa en proyectos. |
| **Registrar empresas y ofertas publicadas (PUBLICA)** | ✅ Cumple | En `/empresas` y `/ofertas`, creación de empresas y publicación de vacantes asociadas mediante la relación `PUBLICA`. |
| **Relacionar ofertas con habilidades requeridas (REQUIERE)** | ✅ Cumple | En `/ofertas`, botón "Habilidades" que despliega y gestiona los requisitos técnicos de cada vacante. |
| **Postulación de usuarios a ofertas (POSTULA_A)** | ✅ Cumple | En `/ofertas` y `/usuarios/<id>`, postulación directa de candidatos a vacantes laborales registrando fecha de postulación. |
| **Consultar caminos y conexiones (Ruta más corta)** | ✅ Cumple | En `/usuarios/<id>`, selector interactivo para calcular la ruta más corta (`shortestPath`) entre el usuario y cualquier empresa del grafo. |
| **Recomendación de contactos** | ✅ Cumple | En `/usuarios/<id>`, algoritmo de cierre triádico (amigos de amigos no conectados) con conteo de intermediarios en común. |
| **Recomendación de empleos** | ✅ Cumple | En `/usuarios/<id>`, motor de matching que clasifica las ofertas según el número de habilidades coincidentes. |
| **Detección de usuarios con habilidades similares** | ✅ Cumple | En `/usuarios/<id>`, consulta de perfiles afines según intersección de competencias técnicas compartidas. |
| **Contactos en común entre dos profesionales** | ✅ Cumple | En `/usuarios/<id>`, herramienta interactiva que compara dos profesionales y lista los amigos mutuos. |
| **Proyectos que comparten miembros** | ✅ Cumple | En `/proyectos` y consulta Cypher dedicada para detectar proyectos interrelacionados. |
| **Panel de Analítica: Usuarios más influyentes** | ✅ Cumple | En `/analitica`, cálculo de centralidad de grado (suma ponderada de conexiones, empleos y proyectos) con gráfica en Chart.js. |
| **Panel de Analítica: Comunidades detectadas** | ✅ Cumple | En `/analitica`, algoritmo de componentes conexos que agrupa usuarios en subredes y clusters profesionales. |
| **Panel de Analítica: Habilidades más demandadas** | ✅ Cumple | En `/analitica`, gráfica de barras horizontales con las competencias con mayor frecuencia en las ofertas laborales. |
| **Visualización interactiva del grafo completo** | ✅ Cumple | En `/grafo`, renderizado 2D mediante `vis.js` con física de fuerzas, filtros dinámicos por tipo de nodo, buscador y panel inspector. |

---

## 🔐 2. Sistema de Autenticación y Roles de Usuario

La aplicación cuenta con un sistema de sesiones basado en dos roles claramente diferenciados:

### A. Rol Administrador (Admin)
- **Acceso:** Total e ilimitado a todas las herramientas ya existentes.
- **Capacidades exclusivas:**
  - Crear, editar y eliminar usuarios, empresas, habilidades, proyectos y ofertas laborales.
  - Ver todos los postulantes de cualquier oferta.
  - Asignar o remover integrantes en cualquier proyecto.
  - Visualizar el panel de analítica global.
- **Credenciales por defecto:**
  - **Correo:** `admin@pronet.com`
  - **Contraseña:** `admin123`
  - *(O mediante el botón de 1 clic "Entrar como Administrador" en la pantalla de login)*.

### B. Rol Usuario Profesional (Usuario Estándar)
- **Acceso:** Personalizado enfocado en su propia trayectoria y red.
- **Capacidades:**
  - **Mi Perfil (`/mi-perfil`):** Administra sus propias habilidades técnicas, su experiencia laboral en empresas, sus proyectos y sus postulaciones a vacantes.
  - **Explorar Red:** Puede explorar otros profesionales, ver sus perfiles y conectarse con ellos mediante el botón **"Conectar en mi Red"** (`CONECTA_CON`).
  - **Privacidad y Control:** No puede editar ni borrar la información de otros profesionales.
  - **Bolsa de Empleo:** Puede postularse directamente a cualquier vacante activa con el botón **"Postularme a esta Oferta"** (`POSTULA_A`).
- **Credenciales:**
  - Cada usuario tiene asignada una **contraseña aleatoria de 6 dígitos** (ej. `492018`, `839102`), visible y editable por el Administrador en la tabla de usuarios. En la pantalla de login, el selector rápido de usuarios autocompleta la contraseña correspondiente para facilitar pruebas. También se puede registrar una nueva cuenta desde `/register`.
- **Gestión de Contraseñas desde el Panel de Administrador:**
  - En la sección `/usuarios`, el Administrador puede ver la contraseña de cada usuario y modificarla en tiempo real mediante el botón con ícono de llave (<i class="fas fa-key"></i>), generando claves aleatorias de 6 dígitos o asignando una clave manual.

---

## 🎯 3. ¿Para qué sirve la Aplicación y qué Problema Resuelve?

Las redes profesionales modernas (como LinkedIn o redes de networking académico) poseen datos **altamente interconectados**. En una base de datos relacional tradicional (SQL):
- Consultar un camino entre un usuario y una empresa a través de 3 o 4 grados de separación requiere múltiples sentencias `JOIN` complejas, lentas y costosas a nivel de CPU y memoria.
- Identificar comunidades, contactos en común o recomendaciones de habilidades genera cuellos de botella notables a medida que crece el número de filas.

**Esta aplicación resuelve ese problema utilizando Neo4j**, una base de datos orientada a grafos en la que:
1. **Las relaciones son ciudadanos de primer orden** (punteros directos en disco), permitiendo recorridos (*index-free adjacency*) en milisegundos sin importar el tamaño total de la base de datos.
2. **Facilita recomendaciones en tiempo real** de empleos acordes al perfil técnico del usuario y de nuevos colegas según amigos en común.
3. **Ofrece analítica de redes complejas**, identificando líderes de opinión o perfiles clave (usuarios influyentes) y divisiones naturales de la red (comunidades).

---

## 🧭 3. Guía de Uso Paso a Paso por Módulo

### 🏠 A. Inicio (Dashboard Principal - `/`)
- **Qué es:** Pantalla de bienvenida y resumen global del estado de la red.
- **Funcionalidad:** Muestra 5 tarjetas estadísticas interactivas con los totales en tiempo real de Usuarios, Empresas, Habilidades, Proyectos y Ofertas laborales.
- **Cómo usarlo:** Pasa el cursor por cualquier tarjeta y haz clic en ella para navegar instantáneamente al módulo correspondiente. En la parte inferior cuentas con botones de acción rápida para ver el grafo o la analítica.

---

### 👤 B. Módulo de Usuarios (`/usuarios`)
- **Qué es:** Centro de administración y listado de profesionales registrados.
- **Funcionalidades:**
  - **Crear Usuario:** Haz clic en el botón superior **"+ Nuevo Usuario"**, llena los datos (Nombre, Email, Título profesional, Ubicación, Resumen) y presiona **"Guardar"**.
  - **Editar Usuario:** Haz clic en el ícono amarillo del lápiz en la fila del usuario, modifica sus datos y guarda.
  - **Eliminar Usuario:** Haz clic en el ícono rojo de la papelera para borrar el usuario y todas sus relaciones en el grafo.
  - **Ver Perfil Detallado:** Haz clic sobre el nombre del usuario o en el enlace **"Ver Perfil Completo"**.

---

### 🔍 C. Perfil Detallado y Motor de Recomendación (`/usuarios/<id>`)
Esta es una de las vistas más potentes de la aplicación:
1. **Pestaña Conexiones Profesionales:** Permite conectar al usuario actual con otro usuario del sistema (`CONECTA_CON`) mediante un menú desplegable y el botón **"Conectar"**. También permite romper conexiones existentes.
2. **Pestaña Habilidades:** Asigna competencias técnicas al usuario (`TIENE_HABILIDAD`) tomadas del catálogo general.
3. **Pestaña Experiencia Laboral:** Vincula al usuario con una empresa (`TRABAJA_EN`) especificando el cargo (ej. *Tech Lead*), fecha de inicio y fecha de fin (o marcando si trabaja allí actualmente).
4. **Pestaña Proyectos:** Agrega al usuario a proyectos colaborativos con su rol asignado (`PARTICIPA_EN`).
5. **Pestaña Postulaciones:** Muestra las vacantes a las que el usuario ha aplicado y permite postularlo a nuevas ofertas (`POSTULA_A`).
6. **Pestaña Recomendaciones (Inteligencia de Grafos):**
   - **Contactos Recomendados:** Sugiere personas que son contactos de sus contactos pero con quienes aún no está conectado.
   - **Empleos Recomendados:** Sugiere ofertas laborales ordenadas por mayor coincidencia con las habilidades que posee el usuario.
   - **Perfiles Similares:** Identifica qué otros usuarios comparten la mayor cantidad de habilidades técnicas.
7. **Herramienta "Contactos en Común":** Selecciona otro profesional de la lista y presiona **"Buscar Contactos en Común"** para ver los intermediarios mutuos.
8. **Herramienta "Ruta más Corta a Empresa":** Selecciona cualquier empresa y presiona **"Calcular Ruta"**; el sistema ejecutará el algoritmo `shortestPath` de Neo4j y mostrará la cadena exacta de nodos (Usuario → Conexión → Proyecto/Empresa) para llegar a ella.

---

### 🏢 D. Módulo de Empresas (`/empresas`)
- **Qué es:** Catálogo de organizaciones y compañías del ecosistema.
- **Funcionalidades:**
  - Registrar nuevas compañías con su industria, ubicación, sitio web y descripción.
  - Al hacer clic en **"Ver Ofertas"** en la tarjeta de cualquier empresa, el sistema consulta en tiempo real las vacantes publicadas por dicha empresa a través de la relación `PUBLICA`.

---

### ⚙️ E. Módulo de Habilidades (`/habilidades`)
- **Qué es:** Catálogo de competencias técnicas y blandas categorizadas (Frontend, Backend, DevOps, Datos, etc.).
- **Funcionalidades:**
  - Ver habilidades agrupadas en tarjetas por categoría con distintivos de color.
  - Crear nuevas habilidades mediante el botón **"+ Nueva Habilidad"**.
  - Eliminar habilidades que ya no se consideren relevantes.

---

### 📁 F. Módulo de Proyectos (`/proyectos`)
- **Qué es:** Gestión de iniciativas técnicas y productos donde colaboran los profesionales.
- **Funcionalidades:**
  - Registrar proyectos con su estado (*Activo*, *Finalizado*, *En Planificación*) y fecha de inicio.
  - Al presionar **"Ver Integrantes"**, se despliegan los usuarios que colaboran en el proyecto y su rol.
  - Permite vincular nuevos integrantes al proyecto con un rol específico (ej. *Product Owner*, *Backend Dev*).

---

### 💼 G. Módulo de Ofertas Laborales (`/ofertas`)
- **Qué es:** Bolsa de empleo vinculada directamente a las competencias del grafo.
- **Funcionalidades:**
  - Crear vacantes laborales asociadas a una empresa, con modalidad (*Remoto*, *Híbrido*, *Presencial*) y rango salarial.
  - **Gestionar Habilidades Requeridas:** En cada oferta, haz clic en **"Habilidades"** para añadir o quitar requisitos técnicos mediante la relación `REQUIERE`.
  - **Gestionar Postulantes:** Haz clic en **"Postulantes"** para ver los candidatos que han aplicado y postular a nuevos usuarios directamente.

---

### 📊 H. Panel de Analítica de Grafos (`/analitica`)
- **Qué es:** Panel con métricas de teoría de grafos y gráficos estadísticos interactivos generados con **Chart.js**:
  1. **Usuarios Más Influyentes:** Gráfico de barras que mide la centralidad de grado sumando conexiones de red, empresas y proyectos de cada persona.
  2. **Habilidades Más Demandadas:** Gráfico horizontal que revela cuáles son las tecnologías más solicitadas por las ofertas del mercado.
  3. **Detección de Comunidades:** Algoritmo que agrupa a los usuarios en subredes o clusters conexos coloreados por grupo, permitiendo detectar afinidades profesionales orgánicas.

---

### 🌐 I. Visualización del Grafo Completo (`/grafo`)
- **Qué es:** Lienzo interactivo en 2D impulsado por **vis.js Network**.
- **Funcionalidades:**
  - **Filtros por Tipo de Nodo:** Casillas de verificación para prender/apagar nodos de tipo Usuario, Empresa, Habilidad, Proyecto u Oferta.
  - **Buscador de Nodos:** Escribe el nombre de cualquier usuario, empresa o tecnología y presiona la flecha para enfocarlo automáticamente con animación y zoom.
  - **Física de Fuerzas:** Simulación física de resortes y gravedad (algoritmo Barnes-Hut). Puedes pausar o reanudar la física con el botón superior.
  - **Panel Inspector:** Al hacer clic en cualquier nodo del grafo, se abre un panel lateral derecho mostrando sus propiedades detalladas, el listado de conexiones directas y un enlace para ir al perfil.

---

## 🗄️ 4. Scripts y Consultas Cypher Utilizadas

Todas las consultas Cypher optimizadas que dan vida al backend se encuentran centralizadas y comentadas en el archivo:
📁 **[`scripts/consultas.cypher`](file:///c:/Users/Juanse/Desktop/Bases2/scripts/consultas.cypher)**

Entre ellas se destacan:
1. **Habilidades Similares:**
   ```cypher
   MATCH (u:Usuario {id: $user_id})-[:TIENE_HABILIDAD]->(h:Habilidad)<-[:TIENE_HABILIDAD]-(other:Usuario)
   WHERE u.id <> other.id
   RETURN other, count(h) AS habilidades_compartidas
   ORDER BY habilidades_compartidas DESC;
   ```
2. **Contactos en Común:**
   ```cypher
   MATCH (u1:Usuario {id: $u1})-[:CONECTA_CON]-(c:Usuario)-[:CONECTA_CON]-(u2:Usuario {id: $u2})
   RETURN DISTINCT c;
   ```
3. **Ruta más Corta:**
   ```cypher
   MATCH p = shortestPath((u:Usuario {id: $u})-[*]-(e:Empresa {id: $e}))
   RETURN p, length(p) AS distancia;
   ```
4. **Matching Candidato-Vacante:**
   ```cypher
   MATCH (u:Usuario {id: $u})-[:TIENE_HABILIDAD]->(h:Habilidad)<-[:REQUIERE]-(o:Oferta)
   WHERE NOT (u)-[:POSTULA_A]->(o)
   RETURN o, count(h) AS coincidencia
   ORDER BY coincidencia DESC;
   ```

