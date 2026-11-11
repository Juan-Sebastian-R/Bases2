import os
from functools import wraps
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from dotenv import load_dotenv
from database import Neo4jDB

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "pronet-graph-secret-key-2024")
db = Neo4jDB()

# Ensure all users and companies have passwords
try:
    db.ensure_user_passwords()
    db.ensure_empresa_passwords()
except Exception:
    pass


# ──────────────────────────── AUTH HELPERS & CONTEXT ────────────────────────────


def get_current_user():
    if "user_id" not in session:
        return None
    role = session.get("role")
    if role == "admin":
        return {
            "id": "admin",
            "nombre": "Administrador",
            "email": "admin@pronet.com",
            "role": "admin",
        }
    if role == "empresa":
        emp = db.get_empresa(session["user_id"])
        if emp:
            emp["role"] = "empresa"
        return emp
    user = db.get_usuario(session["user_id"])
    if user:
        user["role"] = "usuario"
    return user


@app.context_processor
def inject_auth():
    user = get_current_user()
    return {
        "current_user": user,
        "is_admin": session.get("role") == "admin",
        "is_empresa": session.get("role") == "empresa",
        "is_logged_in": "user_id" in session,
    }


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión para acceder a esta sección.", "warning")
            return redirect(url_for("login_page", next=request.path))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Acceso restringido: requiere permisos de Administrador.", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function


# ──────────────────────────── AUTH ROUTES ────────────────────────────


@app.route("/login", methods=["GET", "POST"])
def login_page():
    # If already logged in, redirect accordingly
    if "user_id" in session:
        role = session.get("role")
        if role == "admin":
            return redirect(url_for("dashboard_page"))
        elif role == "empresa":
            return redirect(url_for("ofertas_page"))
        return redirect(url_for("mi_perfil"))

    try:
        db.ensure_user_passwords()
        db.ensure_empresa_passwords()
    except Exception:
        pass

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()
        next_url = request.form.get("next") or ""

        # Validate that both fields are filled
        if not email or not password:
            flash("Debes ingresar tu correo y tu contraseña. Ningún campo puede quedar vacío.", "warning")
            usuarios = db.get_all_usuarios()
            empresas = db.get_all_empresas()
            return render_template("login.html", usuarios=usuarios, empresas=empresas)

        # 1. Admin check
        if email == "admin@pronet.com":
            if password in ("admin123", "admin"):
                session["user_id"] = "admin"
                session["role"] = "admin"
                session["user_name"] = "Administrador"
                flash("Bienvenido, Administrador. Acceso total concedido.", "success")
                return redirect(next_url if next_url and next_url != "/" else url_for("dashboard_page"))
            else:
                flash("Contraseña incorrecta para la cuenta de Administrador.", "danger")
                usuarios = db.get_all_usuarios()
                empresas = db.get_all_empresas()
                return render_template("login.html", usuarios=usuarios, empresas=empresas)

        # 2. Empresa check in Neo4j
        empresa = db.get_empresa_by_email(email)
        if empresa:
            emp_pwd = str(empresa.get("password") or "123456").strip()
            if not emp_pwd or password != emp_pwd:
                flash("Contraseña incorrecta para la cuenta de Empresa.", "danger")
                usuarios = db.get_all_usuarios()
                empresas = db.get_all_empresas()
                return render_template("login.html", usuarios=usuarios, empresas=empresas)

            if not empresa.get("password"):
                db.update_empresa(empresa["id"], {"password": emp_pwd})

            session["user_id"] = empresa["id"]
            session["role"] = "empresa"
            session["user_name"] = empresa.get("nombre", "Empresa")
            flash(f"¡Bienvenido, {empresa.get('nombre')}! Sesión iniciada como Empresa.", "success")
            return redirect(next_url if next_url and next_url != "/" else url_for("ofertas_page"))

        # 3. Normal User check in Neo4j
        usuario = db.get_usuario_by_email(email)
        if usuario:
            user_pwd = str(usuario.get("password") or "").strip()
            if not user_pwd or password != user_pwd:
                flash("Contraseña incorrecta. Por favor verifica tu clave de acceso.", "danger")
                usuarios = db.get_all_usuarios()
                empresas = db.get_all_empresas()
                return render_template("login.html", usuarios=usuarios, empresas=empresas)

            session["user_id"] = usuario["id"]
            session["role"] = "usuario"
            session["user_name"] = usuario.get("nombre", "Usuario")
            flash(f"¡Bienvenido de nuevo, {usuario.get('nombre')}!", "success")
            return redirect(next_url if next_url and next_url != "/" else f"/usuarios/{usuario['id']}")
        else:
            flash("No existe ninguna cuenta registrada con ese correo electrónico.", "danger")

    usuarios = db.get_all_usuarios()
    empresas = db.get_all_empresas()
    return render_template("login.html", usuarios=usuarios, empresas=empresas)


@app.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión exitosamente.", "info")
    return redirect(url_for("login_page"))


@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        tipo = request.form.get("tipo", "usuario").strip().lower()

        if tipo == "empresa":
            data = {
                "nombre": request.form.get("nombre", "").strip(),
                "email": request.form.get("email", "").strip().lower(),
                "industria": request.form.get("industria", "").strip(),
                "ubicacion": request.form.get("ubicacion", "").strip(),
                "sitio_web": request.form.get("sitio_web", "").strip(),
                "descripcion": request.form.get("descripcion", "").strip(),
                "password": request.form.get("password", "").strip(),
            }
            if not data["nombre"] or not data["email"]:
                flash("El nombre de la empresa y correo son obligatorios.", "warning")
                return render_template("register.html")

            existente_emp = db.get_empresa_by_email(data["email"])
            existente_usr = db.get_usuario_by_email(data["email"])
            if existente_emp or existente_usr:
                flash("Ese correo ya está registrado en la red. Inicia sesión directamente.", "warning")
                return redirect(url_for("login_page"))

            nueva_emp = db.create_empresa(data)
            session["user_id"] = nueva_emp["id"]
            session["role"] = "empresa"
            session["user_name"] = nueva_emp["nombre"]
            flash(f"¡Cuenta de Empresa creada exitosamente! Bienvenido {nueva_emp['nombre']}.", "success")
            return redirect(url_for("ofertas_page"))

        else:
            data = {
                "nombre": request.form.get("nombre", "").strip(),
                "email": request.form.get("email", "").strip().lower(),
                "titulo": request.form.get("titulo", "").strip(),
                "ubicacion": request.form.get("ubicacion", "").strip(),
                "resumen": request.form.get("resumen", "").strip(),
                "password": request.form.get("password", "").strip(),
            }
            if not data["nombre"] or not data["email"]:
                flash("El nombre y correo son obligatorios.", "warning")
                return render_template("register.html")

            existente_emp = db.get_empresa_by_email(data["email"])
            existente_usr = db.get_usuario_by_email(data["email"])
            if existente_emp or existente_usr:
                flash("Ese correo ya está registrado en la red. Inicia sesión directamente.", "warning")
                return redirect(url_for("login_page"))

            nuevo = db.create_usuario(data)
            session["user_id"] = nuevo["id"]
            session["role"] = "usuario"
            session["user_name"] = nuevo["nombre"]
            flash("¡Cuenta creada exitosamente! Bienvenido a tu perfil.", "success")
            return redirect(f"/usuarios/{nuevo['id']}")

    return render_template("register.html")


@app.route("/mi-perfil")
@login_required
def mi_perfil():
    role = session.get("role")
    if role == "admin":
        return redirect(url_for("dashboard_page"))
    elif role == "empresa":
        return redirect(url_for("ofertas_page"))
    return redirect(f"/usuarios/{session['user_id']}")


# ──────────────────────────── PAGE ROUTES ────────────────────────────


@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    if session.get("role") == "admin":
        return redirect(url_for("dashboard_page"))
    return redirect(url_for("mi_perfil"))


@app.route("/dashboard")
@login_required
def dashboard_page():
    stats = {
        "usuarios": len(db.get_all_usuarios()),
        "empresas": len(db.get_all_empresas()),
        "habilidades": len(db.get_all_habilidades()),
        "proyectos": len(db.get_all_proyectos()),
        "ofertas": len(db.get_all_ofertas()),
    }
    return render_template("index.html", stats=stats)


@app.route("/usuarios")
@login_required
def usuarios_page():
    try:
        db.ensure_user_passwords()
    except Exception:
        pass
    usuarios = db.get_all_usuarios()
    return render_template("usuarios.html", usuarios=usuarios)


@app.route("/usuarios/<id>")
@login_required
def usuario_detalle_page(id):
    usuario = db.get_usuario(id)
    if not usuario:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for("usuarios_page"))

    current_role = session.get("role")
    current_user_id = session.get("user_id")
    is_admin = current_role == "admin"
    is_other_user = not is_admin and current_user_id and current_user_id != id

    contactos_en_comun = []
    if is_other_user:
        try:
            contactos_en_comun = db.common_contacts(current_user_id, id)
        except Exception:
            contactos_en_comun = []

    can_edit = is_admin or current_user_id == id
    conexiones = db.get_user_connections(id)
    habilidades = db.get_user_skills(id)
    empresas = db.get_user_companies(id)
    proyectos = db.get_user_projects(id)
    postulaciones = db.get_user_applications(id) if not is_other_user else []
    recomendaciones_contactos = db.recommend_contacts(id)
    recomendaciones_empleos = db.recommend_jobs(id)
    similares = db.users_with_similar_skills(id)
    return render_template(
        "usuario_detalle.html",
        usuario=usuario,
        can_edit=can_edit,
        is_other_user=is_other_user,
        contactos_en_comun=contactos_en_comun,
        conexiones=conexiones,
        habilidades=habilidades,
        empresas=empresas,
        proyectos=proyectos,
        postulaciones=postulaciones,
        recomendaciones_contactos=recomendaciones_contactos,
        recomendaciones_empleos=recomendaciones_empleos,
        similares=similares,
    )


@app.route("/empresas")
@login_required
def empresas_page():
    empresas = db.get_all_empresas()
    return render_template("empresas.html", empresas=empresas)


@app.route("/habilidades")
@login_required
def habilidades_page():
    habilidades = db.get_all_habilidades()
    return render_template("habilidades.html", habilidades=habilidades)


@app.route("/proyectos")
@login_required
def proyectos_page():
    proyectos = db.get_all_proyectos()
    return render_template("proyectos.html", proyectos=proyectos)


@app.route("/ofertas")
@login_required
def ofertas_page():
    ofertas = db.get_all_ofertas()
    mis_postulaciones = set()
    if session.get("role") == "usuario" and "user_id" in session:
        user_apps = db.get_user_applications(session["user_id"])
        mis_postulaciones = {a["id"] for a in user_apps if a.get("id")}
    return render_template("ofertas.html", ofertas=ofertas, mis_postulaciones=mis_postulaciones)


@app.route("/analitica")
@login_required
def analitica_page():
    return render_template("analitica.html")


@app.route("/grafo")
@login_required
def grafo_page():
    return render_template("grafo.html")


# ──────────────────────────── CRUD API: USUARIOS ────────────────────────────


@app.route("/api/usuarios", methods=["GET", "POST"])
def api_usuarios():
    if request.method == "POST":
        data = request.get_json()
        usuario = db.create_usuario(data)
        return jsonify(usuario), 201
    return jsonify(db.get_all_usuarios())


@app.route("/api/usuarios/<id>", methods=["GET", "PUT", "DELETE"])
def api_usuario(id):
    if request.method == "GET":
        usuario = db.get_usuario(id)
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify(usuario)
    elif request.method == "PUT":
        if session.get("role") != "admin" and session.get("user_id") != id:
            return jsonify({"error": "No tienes permisos para modificar este perfil."}), 403
        data = request.get_json()
        usuario = db.update_usuario(id, data)
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify(usuario)
    else:
        if session.get("role") != "admin":
            return jsonify({"error": "Solo un Administrador puede eliminar usuarios."}), 403
        ok = db.delete_usuario(id)
        if not ok:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify({"message": "Usuario eliminado"})


@app.route("/api/usuarios/<id>/password", methods=["POST", "PUT"])
def api_usuario_password(id):
    if session.get("role") != "admin" and session.get("user_id") != id:
        return jsonify({"error": "No tienes permisos para cambiar la contraseña de otro usuario."}), 403
    data = request.get_json() or {}
    new_password = str(data.get("password", "")).strip()
    if not new_password or len(new_password) < 4:
        return jsonify({"error": "La contraseña debe tener al menos 4 dígitos o caracteres"}), 400
    res = db.update_user_password(id, new_password)
    if not res:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify({"message": "Contraseña actualizada exitosamente", "password": new_password})


# ──────────────────────────── CRUD API: EMPRESAS ────────────────────────────


@app.route("/api/empresas", methods=["GET", "POST"])
def api_empresas():
    if request.method == "POST":
        if session.get("role") != "admin":
            return jsonify({"error": "Solo un Administrador puede registrar empresas directamente."}), 403
        data = request.get_json()
        empresa = db.create_empresa(data)
        return jsonify(empresa), 201
    return jsonify(db.get_all_empresas())


@app.route("/api/empresas/<id>", methods=["GET", "PUT", "DELETE"])
def api_empresa(id):
    if request.method == "GET":
        empresa = db.get_empresa(id)
        if not empresa:
            return jsonify({"error": "Empresa no encontrada"}), 404
        return jsonify(empresa)
    elif request.method == "PUT":
        if session.get("role") != "admin" and session.get("user_id") != id:
            return jsonify({"error": "No tienes permisos para modificar los datos de esta empresa."}), 403
        data = request.get_json()
        empresa = db.update_empresa(id, data)
        if not empresa:
            return jsonify({"error": "Empresa no encontrada"}), 404
        return jsonify(empresa)
    else:
        if session.get("role") != "admin":
            return jsonify({"error": "Solo un Administrador puede eliminar empresas."}), 403
        ok = db.delete_empresa(id)
        if not ok:
            return jsonify({"error": "Empresa no encontrada"}), 404
        return jsonify({"message": "Empresa eliminada"})


# ──────────────────────────── CRUD API: HABILIDADES ────────────────────────────


@app.route("/api/habilidades", methods=["GET", "POST"])
def api_habilidades():
    if request.method == "POST":
        if session.get("role") != "admin":
            return jsonify({"error": "Solo un Administrador puede crear habilidades globales."}), 403
        data = request.get_json()
        habilidad = db.create_habilidad(data)
        return jsonify(habilidad), 201
    return jsonify(db.get_all_habilidades())


@app.route("/api/habilidades/<id>", methods=["DELETE"])
def api_habilidad_delete(id):
    if session.get("role") != "admin":
        return jsonify({"error": "Solo un Administrador puede eliminar habilidades del catálogo general."}), 403
    ok = db.delete_habilidad(id)
    if not ok:
        return jsonify({"error": "Habilidad no encontrada"}), 404
    return jsonify({"message": "Habilidad eliminada"})


# ──────────────────────────── CRUD API: PROYECTOS ────────────────────────────


@app.route("/api/proyectos", methods=["GET", "POST"])
def api_proyectos():
    if request.method == "POST":
        if "user_id" not in session:
            return jsonify({"error": "Debes iniciar sesión para crear proyectos."}), 401
        data = request.get_json()
        proyecto = db.create_proyecto(data)
        # If created by a regular user, automatically join them to the project
        if session.get("role") == "usuario" and proyecto and proyecto.get("id"):
            db.add_user_to_project(session["user_id"], proyecto["id"], "Creador")
        return jsonify(proyecto), 201
    return jsonify(db.get_all_proyectos())


@app.route("/api/proyectos/<id>", methods=["GET", "PUT", "DELETE"])
def api_proyecto(id):
    if request.method == "GET":
        proyecto = db.get_proyecto(id)
        if not proyecto:
            return jsonify({"error": "Proyecto no encontrado"}), 404
        return jsonify(proyecto)
    elif request.method == "PUT":
        if session.get("role") != "admin":
            return jsonify({"error": "Solo un Administrador puede editar los datos del proyecto."}), 403
        data = request.get_json()
        proyecto = db.update_proyecto(id, data)
        if not proyecto:
            return jsonify({"error": "Proyecto no encontrado"}), 404
        return jsonify(proyecto)
    else:
        if session.get("role") != "admin":
            return jsonify({"error": "Solo un Administrador puede eliminar proyectos."}), 403
        ok = db.delete_proyecto(id)
        if not ok:
            return jsonify({"error": "Proyecto no encontrado"}), 404
        return jsonify({"message": "Proyecto eliminado"})


# ──────────────────────────── CRUD API: OFERTAS ────────────────────────────


@app.route("/api/ofertas", methods=["GET", "POST"])
def api_ofertas():
    if request.method == "POST":
        role = session.get("role")
        if role not in ("admin", "empresa"):
            return jsonify({"error": "Solo administradores o empresas pueden publicar ofertas laborales."}), 403
        data = request.get_json() or {}
        oferta = db.create_oferta(data)
        # If published by Empresa, automatically bind via PUBLICA
        company_id = session.get("user_id") if role == "empresa" else data.get("company_id")
        if company_id and oferta and oferta.get("id"):
            db.publish_offer(company_id, oferta["id"])
        return jsonify(oferta), 201
    return jsonify(db.get_all_ofertas())


@app.route("/api/ofertas/<id>", methods=["GET", "PUT", "DELETE"])
def api_oferta(id):
    if request.method == "GET":
        oferta = db.get_oferta(id)
        if not oferta:
            return jsonify({"error": "Oferta no encontrada"}), 404
        return jsonify(oferta)

    role = session.get("role")
    if role != "admin":
        if role == "empresa":
            offer_emp = db.get_offer_company(id)
            if not offer_emp or offer_emp.get("id") != session.get("user_id"):
                return jsonify({"error": "No tienes permisos para modificar ofertas de otra empresa."}), 403
        else:
            return jsonify({"error": "Solo administradores o empresas pueden modificar o eliminar ofertas."}), 403

    if request.method == "PUT":
        data = request.get_json()
        oferta = db.update_oferta(id, data)
        if not oferta:
            return jsonify({"error": "Oferta no encontrada"}), 404
        return jsonify(oferta)
    else:
        ok = db.delete_oferta(id)
        if not ok:
            return jsonify({"error": "Oferta no encontrada"}), 404
        return jsonify({"message": "Oferta eliminada"})


# ──────────────────────────── RELATIONSHIP APIs ────────────────────────────


@app.route("/api/relaciones/conectar", methods=["POST", "DELETE"])
def api_rel_conectar():
    data = request.get_json()
    if request.method == "POST":
        db.connect_users(data["user1_id"], data["user2_id"])
        return jsonify({"message": "Usuarios conectados"})
    else:
        db.disconnect_users(data["user1_id"], data["user2_id"])
        return jsonify({"message": "Conexión eliminada"})


@app.route("/api/relaciones/trabaja_en", methods=["POST", "DELETE"])
def api_rel_trabaja_en():
    data = request.get_json()
    if request.method == "POST":
        db.set_works_at(
            data["user_id"],
            data["company_id"],
            data.get("cargo", ""),
            data.get("fecha_inicio", ""),
            data.get("fecha_fin"),
            data.get("actual", False),
        )
        return jsonify({"message": "Relación laboral creada"})
    else:
        db.remove_works_at(data["user_id"], data["company_id"])
        return jsonify({"message": "Relación laboral eliminada"})


@app.route("/api/relaciones/tiene_habilidad", methods=["POST", "DELETE"])
def api_rel_tiene_habilidad():
    data = request.get_json()
    if request.method == "POST":
        db.add_skill_to_user(data["user_id"], data["skill_id"])
        return jsonify({"message": "Habilidad asignada"})
    else:
        db.remove_skill_from_user(data["user_id"], data["skill_id"])
        return jsonify({"message": "Habilidad removida"})


@app.route("/api/relaciones/participa_en", methods=["POST", "DELETE"])
def api_rel_participa_en():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    project_id = data.get("project_id")
    if not user_id or not project_id:
        return jsonify({"error": "Faltan parámetros user_id o project_id"}), 400

    # Non-admin users can ONLY add or remove THEMSELVES
    if session.get("role") != "admin":
        curr_id = session.get("user_id")
        if not curr_id or curr_id != user_id:
            return jsonify({"error": "No puedes agregar ni remover a otros usuarios de un proyecto. Solo puedes agregarte o retirarte a ti mismo."}), 403

    if request.method == "POST":
        db.add_user_to_project(user_id, project_id, data.get("rol", ""))
        return jsonify({"message": "Usuario agregado al proyecto"})
    else:
        db.remove_user_from_project(user_id, project_id)
        return jsonify({"message": "Usuario removido del proyecto"})


@app.route("/api/relaciones/publica", methods=["POST"])
def api_rel_publica():
    data = request.get_json()
    if session.get("role") != "admin" and session.get("user_id") != data.get("company_id"):
        return jsonify({"error": "No tienes permisos para vincular ofertas a esta empresa."}), 403
    db.publish_offer(data["company_id"], data["offer_id"])
    return jsonify({"message": "Oferta publicada"})


@app.route("/api/relaciones/requiere", methods=["POST", "DELETE"])
def api_rel_requiere():
    data = request.get_json() or {}
    offer_id = data.get("offer_id")
    skill_id = data.get("skill_id")
    if not offer_id or not skill_id:
        return jsonify({"error": "Faltan parámetros offer_id o skill_id"}), 400

    role = session.get("role")
    if role != "admin":
        if role == "empresa":
            offer_emp = db.get_offer_company(offer_id)
            if not offer_emp or offer_emp.get("id") != session.get("user_id"):
                return jsonify({"error": "Solo la empresa que publicó esta oferta o un Administrador pueden modificar sus requisitos."}), 403
        else:
            return jsonify({"error": "Los usuarios regulares no tienen permisos para añadir o modificar habilidades requeridas a una oferta."}), 403

    if request.method == "POST":
        db.add_skill_to_offer(offer_id, skill_id)
        return jsonify({"message": "Habilidad requerida agregada"})
    else:
        db.remove_skill_from_offer(offer_id, skill_id)
        return jsonify({"message": "Habilidad requerida removida"})


@app.route("/api/relaciones/postula", methods=["POST", "DELETE"])
def api_rel_postula():
    data = request.get_json()
    if request.method == "POST":
        db.apply_to_offer(data["user_id"], data["offer_id"], data.get("fecha", ""))
        return jsonify({"message": "Postulación creada"})
    else:
        db.remove_application(data["user_id"], data["offer_id"])
        return jsonify({"message": "Postulación eliminada"})


# ──────────────────────────── ANALYTICS APIs ────────────────────────────


@app.route("/api/analitica/influyentes")
def api_influyentes():
    return jsonify(db.most_influential_users())


@app.route("/api/analitica/comunidades")
def api_comunidades():
    return jsonify(db.detect_communities())


@app.route("/api/analitica/habilidades_demandadas")
def api_habilidades_demandadas():
    return jsonify(db.most_demanded_skills())


# ──────────────────────────── RECOMMENDATION APIs ────────────────────────────


@app.route("/api/recomendaciones/contactos/<user_id>")
def api_rec_contactos(user_id):
    return jsonify(db.recommend_contacts(user_id))


@app.route("/api/recomendaciones/empleos/<user_id>")
def api_rec_empleos(user_id):
    return jsonify(db.recommend_jobs(user_id))


@app.route("/api/recomendaciones/similares/<user_id>")
def api_rec_similares(user_id):
    return jsonify(db.users_with_similar_skills(user_id))


@app.route("/api/recomendaciones/comunes/<user1_id>/<user2_id>")
def api_rec_comunes(user1_id, user2_id):
    return jsonify(db.common_contacts(user1_id, user2_id))


@app.route("/api/recomendaciones/ruta/<user_id>/<company_id>")
def api_rec_ruta(user_id, company_id):
    return jsonify(db.shortest_path_user_company(user_id, company_id))


# ──────────────────────────── GRAPH API ────────────────────────────


@app.route("/api/grafo")
def api_grafo():
    return jsonify(db.get_full_graph())


# ──────────────────────────── USER DETAIL APIs ────────────────────────────


def user_can_edit(uid):
    return session.get("role") == "admin" or session.get("user_id") == uid


@app.route("/api/usuarios/<id>/conexiones", methods=["GET", "POST"])
def api_user_conexiones(id):
    if request.method == "POST":
        if not user_can_edit(id):
            return jsonify({"error": "No tienes permisos para modificar este perfil."}), 403
        data = request.get_json() or {}
        other_id = data.get("otro_id") or data.get("user2_id")
        if not other_id:
            return jsonify({"error": "Falta id del usuario a conectar"}), 400
        db.connect_users(id, other_id)
        return jsonify({"message": "Conectado"})
    return jsonify(db.get_user_connections(id))


@app.route("/api/usuarios/<id>/conexiones/<other_id>", methods=["DELETE"])
def api_user_del_conexion(id, other_id):
    if not user_can_edit(id):
        return jsonify({"error": "No tienes permisos para modificar este perfil."}), 403
    db.disconnect_users(id, other_id)
    return jsonify({"message": "Conexión eliminada"})


@app.route("/api/usuarios/<id>/habilidades", methods=["GET", "POST"])
def api_user_habilidades(id):
    if request.method == "POST":
        if not user_can_edit(id):
            return jsonify({"error": "No tienes permisos para modificar este perfil."}), 403
        data = request.get_json() or {}
        skill_id = data.get("habilidad_id") or data.get("skill_id")
        if not skill_id:
            return jsonify({"error": "Falta habilidad_id"}), 400
        db.add_skill_to_user(id, skill_id)
        return jsonify({"message": "Habilidad agregada"})
    return jsonify(db.get_user_skills(id))


@app.route("/api/usuarios/<id>/habilidades/<skill_id>", methods=["DELETE"])
def api_user_del_habilidad(id, skill_id):
    if not user_can_edit(id):
        return jsonify({"error": "No tienes permisos para modificar este perfil."}), 403
    db.remove_skill_from_user(id, skill_id)
    return jsonify({"message": "Habilidad removida"})


@app.route("/api/usuarios/<id>/empresas", methods=["GET", "POST"])
def api_user_empresas(id):
    if request.method == "POST":
        if not user_can_edit(id):
            return jsonify({"error": "No tienes permisos para modificar este perfil."}), 403
        data = request.get_json() or {}
        company_id = data.get("empresa_id") or data.get("company_id")
        cargo = data.get("cargo", "")
        fecha_inicio = data.get("fecha_inicio", "")
        fecha_fin = data.get("fecha_fin")
        actual = data.get("actual", False)
        if not company_id:
            return jsonify({"error": "Falta empresa_id"}), 400
        db.set_works_at(id, company_id, cargo, fecha_inicio, fecha_fin, actual)
        return jsonify({"message": "Experiencia agregada"})
    return jsonify(db.get_user_companies(id))


@app.route("/api/usuarios/<id>/empresas/<company_id>", methods=["DELETE"])
def api_user_del_empresa(id, company_id):
    if not user_can_edit(id):
        return jsonify({"error": "No tienes permisos para modificar este perfil."}), 403
    db.remove_works_at(id, company_id)
    return jsonify({"message": "Experiencia eliminada"})


@app.route("/api/usuarios/<id>/proyectos", methods=["GET", "POST"])
def api_user_proyectos(id):
    if request.method == "POST":
        if not user_can_edit(id):
            return jsonify({"error": "No tienes permisos para modificar este perfil."}), 403
        data = request.get_json() or {}
        project_id = data.get("proyecto_id") or data.get("project_id")
        rol = data.get("rol", "")
        if not project_id:
            return jsonify({"error": "Falta proyecto_id"}), 400
        db.add_user_to_project(id, project_id, rol)
        return jsonify({"message": "Proyecto agregado"})
    return jsonify(db.get_user_projects(id))


@app.route("/api/usuarios/<id>/proyectos/<project_id>", methods=["DELETE"])
def api_user_del_proyecto(id, project_id):
    if not user_can_edit(id):
        return jsonify({"error": "No tienes permisos para modificar este perfil."}), 403
    db.remove_user_from_project(id, project_id)
    return jsonify({"message": "Proyecto eliminado"})


@app.route("/api/usuarios/<id>/postulaciones", methods=["GET", "POST"])
def api_user_postulaciones(id):
    if request.method == "POST":
        if not user_can_edit(id):
            return jsonify({"error": "No tienes permisos para postular a este usuario."}), 403
        data = request.get_json() or {}
        offer_id = data.get("oferta_id") or data.get("offer_id")
        fecha = data.get("fecha", "")
        if not offer_id:
            return jsonify({"error": "Falta oferta_id"}), 400
        db.apply_to_offer(id, offer_id, fecha)
        return jsonify({"message": "Postulación agregada"})

    if session.get("role") == "usuario" and session.get("user_id") != id:
        return jsonify([])

    return jsonify(db.get_user_applications(id))


@app.route("/api/usuarios/<id>/postulaciones/<offer_id>", methods=["DELETE"])
def api_user_del_postulacion(id, offer_id):
    if not user_can_edit(id):
        return jsonify({"error": "No tienes permisos para retirar esta postulación."}), 403
    db.remove_application(id, offer_id)
    return jsonify({"message": "Postulación eliminada"})


# ──────────────────────────── COMPANY / OFFER DETAIL APIs ────────────────────────────


@app.route("/api/empresas/<id>/ofertas")
def api_empresa_ofertas(id):
    return jsonify(db.get_company_offers(id))


@app.route("/api/ofertas/<id>/habilidades")
def api_oferta_habilidades(id):
    return jsonify(db.get_offer_skills(id))


@app.route("/api/ofertas/<id>/postulantes")
def api_oferta_postulantes(id):
    return jsonify(db.get_offer_applicants(id))


@app.route("/api/proyectos/<id>/miembros")
def api_proyecto_miembros(id):
    return jsonify(db.get_project_members(id))


# ──────────────────────────── MAIN ────────────────────────────


if __name__ == "__main__":
    app.run(debug=True, port=5000)
