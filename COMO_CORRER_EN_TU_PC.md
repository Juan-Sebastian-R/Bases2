# 🚀 Guía Rápida: Cómo Ejecutar ProNet Graph en tu Computador Personal

Esta guía paso a paso te explica cómo levantar la base de datos Neo4j y la aplicación web Flask en tu máquina (Windows, Mac o Linux) para explorar y probar todas las funcionalidades del proyecto.

---

## 📋 Requisitos Previos

Asegúrate de tener instalados:
1. **Python 3.10 o superior** (al instalar en Windows, recuerda marcar la casilla *"Add python.exe to PATH"*).
2. **Git** (para clonar el repositorio) o haber descargado la carpeta del proyecto.
3. **Neo4j**, que puedes tener de dos formas:
   - **Opción Recomendada:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) (muy rápido y sin instalaciones pesadas).
   - **Opción Alternativa:** [Neo4j Desktop](https://neo4j.com/download/) instalado localmente.

---

## ⚡ Método 1: Usando Docker (Recomendado - En 3 Minutos)

Este proyecto ya incluye un archivo `docker-compose.yml` preconfigurado con Neo4j 5 y plugins listos.

### Paso 1: Abrir la terminal en la carpeta del proyecto
Abre tu terminal favorita (PowerShell, CMD o Terminal de VS Code) dentro de la carpeta del proyecto `Bases2`.

### Paso 2: Levantar el contenedor de Neo4j
Ejecuta:
```bash
docker compose up -d
```
*(Espera unos 15-20 segundos a que el contenedor inicie completamente).*

> **Nota de Puertos configurados en Docker:**
> - **Bolt (Conexión de la app):** Puerto `7688`
> - **Neo4j Browser (Visor web de Neo4j):** `http://localhost:7475` (sin contraseña).

### Paso 3: Verificar el archivo `.env`
Asegúrate de que en la raíz del proyecto exista el archivo `.env` con este contenido:
```ini
NEO4J_URI=bolt://127.0.0.1:7688
NEO4J_USER=
NEO4J_PASSWORD=
FLASK_APP=app.py
FLASK_ENV=development
```
*(Si no existe, créalo o renombra `.env.example` a `.env`).*

### Paso 4: Crear el entorno virtual de Python e instalar librerías
En tu terminal:
```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual
# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# (Si usas CMD en Windows):
.\venv\Scripts\activate.bat
# (En Mac o Linux):
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

### Paso 5: Inicializar la base de datos con datos de prueba
Ejecuta el script que crea los 15 usuarios, 6 empresas, 20 habilidades, ofertas y relaciones:
```bash
python init_db.py
```
*(Deberías ver una serie de checks verdes `✓` confirmando que se cargó toda la red).*

### Paso 6: Iniciar la aplicación web
Ejecuta:
```bash
python app.py
```

### Paso 7: ¡Listo! Abrir en tu navegador
Abre tu navegador web en:
👉 **[http://localhost:5000](http://localhost:5000)** o **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 💻 Método 2: Usando Neo4j Desktop (Sin Docker)

Si prefieres usar la aplicación gráfica oficial **Neo4j Desktop**:

### Paso 1: Crear una base de datos en Neo4j Desktop
1. Abre **Neo4j Desktop**.
2. Crea un nuevo proyecto y haz clic en **"Add" -> "Local DBMS"**.
3. Asígnale una contraseña que recuerdes (por ejemplo: `neo4j123` o `neo4j`).
4. Haz clic en **"Start"** para iniciar la base de datos.
5. Verifica el puerto Bolt (por defecto suele ser `bolt://localhost:7687`).

### Paso 2: Configurar tu archivo `.env`
Edita el archivo `.env` con las credenciales que creaste:
```ini
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=tu_contraseña_aqui
FLASK_APP=app.py
FLASK_ENV=development
```

### Paso 3: Instalar librerías y poblar datos
En tu terminal:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1   # En Windows
pip install -r requirements.txt

# Poblar el grafo con los datos de prueba
python init_db.py

# Iniciar la app
python app.py
```
Abre en tu navegador: **[http://localhost:5000](http://localhost:5000)**.

---

## 🔑 Credenciales para Probar la Plataforma

La aplicación cuenta con 3 roles con vistas y permisos distintos. En la pantalla de Login (**[http://localhost:5000/login](http://localhost:5000/login)**) hay selectores rápidos con 1 clic para entrar fácilmente:

### 1. Rol Administrador (Control Total)
- **Correo:** `admin@pronet.com`
- **Contraseña:** `admin123`
- *O usa el botón directo verde:* **"Entrar como Administrador"**.
- **Qué puedes ver:** Gestión completa de usuarios, empresas, habilidades, proyectos, ofertas laborales, asignación manual de conexiones y panel de analítica global.

### 2. Rol Empresa (Empleador / Reclutador)
- **Ejemplo:** `TechColombia SAS` o `DataSoft Solutions`.
- **Contraseña rápida:** `123456`
- **Qué puedes ver:** Publicación y edición de ofertas laborales propias, gestión de requisitos técnicos (`REQUIERE`) y visualización de candidatos que se han postulado a sus vacantes.

### 3. Rol Usuario (Profesional en la Red)
- **Ejemplo:** `Carlos Andrés Martínez`, `María Alejandra López`, `Gabriela Ríos`, etc.
- **Contraseña:** Puedes usar el selector interactivo en la pantalla de Login que autocompleta su clave.
- **Qué puedes ver:**
  - **Tu Perfil (`/mi-perfil`):** Gestionas tus habilidades, experiencia laboral en empresas, proyectos y tus postulaciones privadas.
  - **Perfil de otro usuario:** Si visitas a otro colega, verás directamente los **Contactos en común** que tienes con esa persona, y en recomendaciones solo verás **Usuarios similares** (respetando la privacidad de sus postulaciones y empleos recomendados).
  - **Bolsa de Empleo (`/ofertas`):** Botón de 1 clic para postularte a vacantes acordes a tu perfil.
  - **Visualizador de Grafo (`/grafo`):** Grafo 2D interactivo con física de fuerzas (`vis.js`).

---

## 🛠️ Preguntas Frecuentes y Solución de Errores

### ❓ Error en PowerShell: *"La ejecución de scripts está deshabilitada en este sistema"*
Si al intentar ejecutar `.\venv\Scripts\Activate.ps1` recibes un error de permisos en PowerShell:
1. Abre PowerShell como Administrador.
2. Ejecuta:
   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. Vuelve a tu terminal normal e intenta activar el entorno virtual de nuevo.

---

### ❓ Error: *"Unable to retrieve routing information" o "Failed to establish connection to bolt://..."*
Significa que Python no se está pudiendo comunicar con Neo4j:
1. Si usas Docker: revisa que el contenedor esté corriendo con `docker ps`. Si no está activo, ejecuta `docker compose up -d`.
2. Si usas Neo4j Desktop: asegúrate de haberle dado clic a **"Start"** y que el puerto en el `.env` coincida con el puerto Bolt (`7687` o `7688`).

---

### ❓ ¿Cómo detener la aplicación cuando termine de probarla?
1. En la consola donde corre Flask, presiona `Ctrl + C`.
2. Si usaste Docker y deseas apagar el contenedor de Neo4j:
   ```bash
   docker compose down
   ```
   *(Los datos quedan guardados en el volumen de Docker, así que no se perderán).*

---
¡Cualquier duda o inconveniente para levantarlo, nos escribimos por el grupo del proyecto! 🚀

