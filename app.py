import os
from functools import wraps
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from dotenv import load_dotenv
from database import Neo4jDB

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "pronet-graph-secret-key-2024")
db = Neo4jDB()


# ──────────────────────────── AUTH HELPERS & CONTEXT ────────────────────────────


def get_current_user():
    if "user_id" not in session:
        return None
    if session.get("role") == "admin":
        return {
            "id": "admin",
            "nombre": "Administrador",
            "email": "admin@pronet.com",
            "role": "admin",
        }
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
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()
        next_url = request.form.get("next") or "/"

        # Admin check
        if email == "admin@pronet.com" and (password == "admin123" or password == "admin"):
            session["user_id"] = "admin"
            session["role"] = "admin"
            session["user_name"] = "Administrador"
            flash("Bienvenido, Administrador. Acceso total concedido.", "success")
            return redirect(next_url)

        # Normal User check in Neo4j
        usuario = db.get_usuario_by_email(email)
        if usuario:
            session["user_id"] = usuario["id"]
            session["role"] = "usuario"
            session["user_name"] = usuario.get("nombre", "Usuario")
            flash(f"¡Bienvenido de nuevo, {usuario.get('nombre')}!", "success")
            return redirect(f"/usuarios/{usuario['id']}")
        else:
            flash("Usuario no encontrado con ese correo electrónico.", "danger")

    usuarios = db.get_all_usuarios()
    return render_template("login.html", usuarios=usuarios)


@app.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión exitosamente.", "info")
    return redirect(url_for("login_page"))


@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        data = {
            "nombre": request.form.get("nombre", "").strip(),
            "email": request.form.get("email", "").strip().lower(),
            "titulo": request.form.get("titulo", "").strip(),
            "ubicacion": request.form.get("ubicacion", "").strip(),
            "resumen": request.form.get("resumen", "").strip(),
        }
        if not data["nombre"] or not data["email"]:
            flash("El nombre y correo son obligatorios.", "warning")
            return render_template("register.html")

        # Verify if email already exists
        existente = db.get_usuario_by_email(data["email"])
        if existente:
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
    if session.get("role") == "admin":
        return redirect("/usuarios")
    return redirect(f"/usuarios/{session['user_id']}")


# ──────────────────────────── PAGE ROUTES ────────────────────────────


@app.route("/")
def index():
    stats = {
        "usuarios": len(db.get_all_usuarios()),
        "empresas": len(db.get_all_empresas()),
        "habilidades": len(db.get_all_habilidades()),
        "proyectos": len(db.get_all_proyectos()),
        "ofertas": len(db.get_all_ofertas()),
    }
    return render_template("index.html", stats=stats)


@app.route("/usuarios")
def usuarios_page():
    usuarios = db.get_all_usuarios()
    return render_template("usuarios.html", usuarios=usuarios)


@app.route("/usuarios/<id>")
def usuario_detalle_page(id):
    usuario = db.get_usuario(id)
    if not usuario:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for("usuarios_page"))

    can_edit = session.get("role") == "admin" or session.get("user_id") == id
    conexiones = db.get_user_connections(id)
    habilidades = db.get_user_skills(id)
    empresas = db.get_user_companies(id)
    proyectos = db.get_user_projects(id)
    postulaciones = db.get_user_applications(id)
    recomendaciones_contactos = db.recommend_contacts(id)
    recomendaciones_empleos = db.recommend_jobs(id)
    similares = db.users_with_similar_skills(id)
    return render_template(
        "usuario_detalle.html",
        usuario=usuario,
        can_edit=can_edit,
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
def empresas_page():
    empresas = db.get_all_empresas()
    return render_template("empresas.html", empresas=empresas)


@app.route("/habilidades")
def habilidades_page():
    habilidades = db.get_all_habilidades()
    return render_template("habilidades.html", habilidades=habilidades)


@app.route("/proyectos")
def proyectos_page():
    proyectos = db.get_all_proyectos()
    return render_template("proyectos.html", proyectos=proyectos)


@app.route("/ofertas")
def ofertas_page():
    ofertas = db.get_all_ofertas()
    return render_template("ofertas.html", ofertas=ofertas)


@app.route("/analitica")
def analitica_page():
    return render_template("analitica.html")


@app.route("/grafo")
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
        data = request.get_json()
        usuario = db.update_usuario(id, data)
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify(usuario)
    else:
        ok = db.delete_usuario(id)
        if not ok:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify({"message": "Usuario eliminado"})


# ──────────────────────────── CRUD API: EMPRESAS ────────────────────────────


@app.route("/api/empresas", methods=["GET", "POST"])
def api_empresas():
    if request.method == "POST":
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
        data = request.get_json()
        empresa = db.update_empresa(id, data)
        if not empresa:
            return jsonify({"error": "Empresa no encontrada"}), 404
        return jsonify(empresa)
    else:
        ok = db.delete_empresa(id)
        if not ok:
            return jsonify({"error": "Empresa no encontrada"}), 404
        return jsonify({"message": "Empresa eliminada"})


# ──────────────────────────── CRUD API: HABILIDADES ────────────────────────────


@app.route("/api/habilidades", methods=["GET", "POST"])
def api_habilidades():
    if request.method == "POST":
        data = request.get_json()
        habilidad = db.create_habilidad(data)
        return jsonify(habilidad), 201
    return jsonify(db.get_all_habilidades())


@app.route("/api/habilidades/<id>", methods=["DELETE"])
def api_habilidad_delete(id):
    ok = db.delete_habilidad(id)
    if not ok:
        return jsonify({"error": "Habilidad no encontrada"}), 404
    return jsonify({"message": "Habilidad eliminada"})


# ──────────────────────────── CRUD API: PROYECTOS ────────────────────────────


@app.route("/api/proyectos", methods=["GET", "POST"])
def api_proyectos():
    if request.method == "POST":
        data = request.get_json()
        proyecto = db.create_proyecto(data)
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
        data = request.get_json()
        proyecto = db.update_proyecto(id, data)
        if not proyecto:
            return jsonify({"error": "Proyecto no encontrado"}), 404
        return jsonify(proyecto)
    else:
        ok = db.delete_proyecto(id)
        if not ok:
            return jsonify({"error": "Proyecto no encontrado"}), 404
        return jsonify({"message": "Proyecto eliminado"})


# ──────────────────────────── CRUD API: OFERTAS ────────────────────────────


@app.route("/api/ofertas", methods=["GET", "POST"])
def api_ofertas():
    if request.method == "POST":
        data = request.get_json()
        oferta = db.create_oferta(data)
        return jsonify(oferta), 201
    return jsonify(db.get_all_ofertas())


@app.route("/api/ofertas/<id>", methods=["GET", "PUT", "DELETE"])
def api_oferta(id):
    if request.method == "GET":
        oferta = db.get_oferta(id)
        if not oferta:
            return jsonify({"error": "Oferta no encontrada"}), 404
        return jsonify(oferta)
    elif request.method == "PUT":
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
        db.set_works_at(data["user_id"], data["company_id"], data.get("cargo", ""), data.get("fecha_inicio", ""))
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
    data = request.get_json()
    if request.method == "POST":
        db.add_user_to_project(data["user_id"], data["project_id"], data.get("rol", ""))
        return jsonify({"message": "Usuario agregado al proyecto"})
    else:
        db.remove_user_from_project(data["user_id"], data["project_id"])
        return jsonify({"message": "Usuario removido del proyecto"})


@app.route("/api/relaciones/publica", methods=["POST"])
def api_rel_publica():
    data = request.get_json()
    db.publish_offer(data["company_id"], data["offer_id"])
    return jsonify({"message": "Oferta publicada"})


@app.route("/api/relaciones/requiere", methods=["POST", "DELETE"])
def api_rel_requiere():
    data = request.get_json()
    if request.method == "POST":
        db.add_skill_to_offer(data["offer_id"], data["skill_id"])
        return jsonify({"message": "Habilidad requerida agregada"})
    else:
        db.remove_skill_from_offer(data["offer_id"], data["skill_id"])
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


@app.route("/api/usuarios/<id>/conexiones")
def api_user_conexiones(id):
    return jsonify(db.get_user_connections(id))


@app.route("/api/usuarios/<id>/habilidades")
def api_user_habilidades(id):
    return jsonify(db.get_user_skills(id))


@app.route("/api/usuarios/<id>/empresas")
def api_user_empresas(id):
    return jsonify(db.get_user_companies(id))


@app.route("/api/usuarios/<id>/proyectos")
def api_user_proyectos(id):
    return jsonify(db.get_user_projects(id))


@app.route("/api/usuarios/<id>/postulaciones")
def api_user_postulaciones(id):
    return jsonify(db.get_user_applications(id))


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
