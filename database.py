import os
import uuid
from neo4j import GraphDatabase


class Neo4jDB:
    """Comprehensive Neo4j database layer for the professional network app."""

    def __init__(self):
        uri = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7688")
        user = os.getenv("NEO4J_USER", "")
        password = os.getenv("NEO4J_PASSWORD", "")
        auth = (user, password) if user and password else None
        try:
            self.driver = GraphDatabase.driver(uri, auth=auth)
            self.driver.verify_connectivity()
        except Exception as e:
            print(f"[Neo4jDB] Warning: could not connect to Neo4j at {uri}: {e}")
            self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        self.driver.close()

    # ──────────────────────────── helpers ────────────────────────────

    @staticmethod
    def _node_to_dict(record, key="n"):
        node = record[key]
        return dict(node)

    # ──────────────────────────── USUARIO CRUD ────────────────────────────

    def create_usuario(self, data):
        import random
        with self.driver.session() as session:
            data["id"] = data.get("id", str(uuid.uuid4()))
            password = str(data.get("password") or random.randint(100000, 999999)).strip()
            result = session.run(
                """
                CREATE (n:Usuario {id: $id, nombre: $nombre, email: $email,
                        titulo: $titulo, ubicacion: $ubicacion, resumen: $resumen,
                        password: $password})
                RETURN n
                """,
                id=data["id"],
                nombre=data.get("nombre", ""),
                email=data.get("email", ""),
                titulo=data.get("titulo", ""),
                ubicacion=data.get("ubicacion", ""),
                resumen=data.get("resumen", ""),
                password=password,
            )
            return self._node_to_dict(result.single())

    def get_all_usuarios(self):
        with self.driver.session() as session:
            result = session.run("MATCH (n:Usuario) RETURN n ORDER BY n.nombre")
            return [self._node_to_dict(r) for r in result]

    def get_usuario(self, uid):
        with self.driver.session() as session:
            result = session.run("MATCH (n:Usuario {id: $id}) RETURN n", id=uid)
            record = result.single()
            return self._node_to_dict(record) if record else None

    def get_usuario_by_email(self, email):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (n:Usuario) WHERE toLower(n.email) = toLower($email) RETURN n",
                email=email.strip()
            )
            record = result.single()
            return self._node_to_dict(record) if record else None

    def update_usuario(self, uid, data):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (n:Usuario {id: $id})
                SET n.nombre = coalesce($nombre, n.nombre),
                    n.email = coalesce($email, n.email),
                    n.titulo = coalesce($titulo, n.titulo),
                    n.ubicacion = coalesce($ubicacion, n.ubicacion),
                    n.resumen = coalesce($resumen, n.resumen),
                    n.password = coalesce($password, n.password)
                RETURN n
                """,
                id=uid,
                nombre=data.get("nombre"),
                email=data.get("email"),
                titulo=data.get("titulo"),
                ubicacion=data.get("ubicacion"),
                resumen=data.get("resumen"),
                password=str(data["password"]).strip() if data.get("password") else None,
            )
            record = result.single()
            return self._node_to_dict(record) if record else None

    def update_user_password(self, uid, new_password):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (n:Usuario {id: $id}) SET n.password = $password RETURN n",
                id=uid, password=str(new_password).strip()
            )
            record = result.single()
            return self._node_to_dict(record) if record else None

    def ensure_user_passwords(self):
        import random
        with self.driver.session() as session:
            # Query all users that don't have a password or have empty password
            result = session.run("MATCH (n:Usuario) WHERE n.password IS NULL OR n.password = '' RETURN n.id AS id")
            for r in result:
                pwd = str(random.randint(100000, 999999))
                session.run("MATCH (n:Usuario {id: $id}) SET n.password = $pwd", id=r["id"], pwd=pwd)
            return self._node_to_dict(record) if record else None

    def delete_usuario(self, uid):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (n:Usuario {id: $id}) DETACH DELETE n RETURN count(n) AS c",
                id=uid,
            )
            return result.single()["c"] > 0

    # ──────────────────────────── EMPRESA CRUD ────────────────────────────

    def create_empresa(self, data):
        with self.driver.session() as session:
            data["id"] = data.get("id", str(uuid.uuid4()))
            result = session.run(
                """
                CREATE (n:Empresa {id: $id, nombre: $nombre, industria: $industria,
                        ubicacion: $ubicacion, descripcion: $descripcion, sitio_web: $sitio_web})
                RETURN n
                """,
                id=data["id"],
                nombre=data.get("nombre", ""),
                industria=data.get("industria", ""),
                ubicacion=data.get("ubicacion", ""),
                descripcion=data.get("descripcion", ""),
                sitio_web=data.get("sitio_web", ""),
            )
            return self._node_to_dict(result.single())

    def get_all_empresas(self):
        with self.driver.session() as session:
            result = session.run("MATCH (n:Empresa) RETURN n ORDER BY n.nombre")
            return [self._node_to_dict(r) for r in result]

    def get_empresa(self, uid):
        with self.driver.session() as session:
            result = session.run("MATCH (n:Empresa {id: $id}) RETURN n", id=uid)
            record = result.single()
            return self._node_to_dict(record) if record else None

    def update_empresa(self, uid, data):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (n:Empresa {id: $id})
                SET n.nombre = coalesce($nombre, n.nombre),
                    n.industria = coalesce($industria, n.industria),
                    n.ubicacion = coalesce($ubicacion, n.ubicacion),
                    n.descripcion = coalesce($descripcion, n.descripcion),
                    n.sitio_web = coalesce($sitio_web, n.sitio_web)
                RETURN n
                """,
                id=uid,
                nombre=data.get("nombre"),
                industria=data.get("industria"),
                ubicacion=data.get("ubicacion"),
                descripcion=data.get("descripcion"),
                sitio_web=data.get("sitio_web"),
            )
            record = result.single()
            return self._node_to_dict(record) if record else None

    def delete_empresa(self, uid):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (n:Empresa {id: $id}) DETACH DELETE n RETURN count(n) AS c",
                id=uid,
            )
            return result.single()["c"] > 0

    # ──────────────────────────── HABILIDAD CRUD ────────────────────────────

    def create_habilidad(self, data):
        with self.driver.session() as session:
            data["id"] = data.get("id", str(uuid.uuid4()))
            result = session.run(
                """
                CREATE (n:Habilidad {id: $id, nombre: $nombre, categoria: $categoria})
                RETURN n
                """,
                id=data["id"],
                nombre=data.get("nombre", ""),
                categoria=data.get("categoria", ""),
            )
            return self._node_to_dict(result.single())

    def get_all_habilidades(self):
        with self.driver.session() as session:
            result = session.run("MATCH (n:Habilidad) RETURN n ORDER BY n.nombre")
            return [self._node_to_dict(r) for r in result]

    def get_habilidad(self, uid):
        with self.driver.session() as session:
            result = session.run("MATCH (n:Habilidad {id: $id}) RETURN n", id=uid)
            record = result.single()
            return self._node_to_dict(record) if record else None

    def update_habilidad(self, uid, data):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (n:Habilidad {id: $id})
                SET n.nombre = coalesce($nombre, n.nombre),
                    n.categoria = coalesce($categoria, n.categoria)
                RETURN n
                """,
                id=uid,
                nombre=data.get("nombre"),
                categoria=data.get("categoria"),
            )
            record = result.single()
            return self._node_to_dict(record) if record else None

    def delete_habilidad(self, uid):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (n:Habilidad {id: $id}) DETACH DELETE n RETURN count(n) AS c",
                id=uid,
            )
            return result.single()["c"] > 0

    # ──────────────────────────── PROYECTO CRUD ────────────────────────────

    def create_proyecto(self, data):
        with self.driver.session() as session:
            data["id"] = data.get("id", str(uuid.uuid4()))
            result = session.run(
                """
                CREATE (n:Proyecto {id: $id, nombre: $nombre, descripcion: $descripcion,
                        estado: $estado, fecha_inicio: $fecha_inicio})
                RETURN n
                """,
                id=data["id"],
                nombre=data.get("nombre", ""),
                descripcion=data.get("descripcion", ""),
                estado=data.get("estado", "activo"),
                fecha_inicio=data.get("fecha_inicio", ""),
            )
            return self._node_to_dict(result.single())

    def get_all_proyectos(self):
        with self.driver.session() as session:
            result = session.run("MATCH (n:Proyecto) RETURN n ORDER BY n.nombre")
            return [self._node_to_dict(r) for r in result]

    def get_proyecto(self, uid):
        with self.driver.session() as session:
            result = session.run("MATCH (n:Proyecto {id: $id}) RETURN n", id=uid)
            record = result.single()
            return self._node_to_dict(record) if record else None

    def update_proyecto(self, uid, data):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (n:Proyecto {id: $id})
                SET n.nombre = coalesce($nombre, n.nombre),
                    n.descripcion = coalesce($descripcion, n.descripcion),
                    n.estado = coalesce($estado, n.estado),
                    n.fecha_inicio = coalesce($fecha_inicio, n.fecha_inicio)
                RETURN n
                """,
                id=uid,
                nombre=data.get("nombre"),
                descripcion=data.get("descripcion"),
                estado=data.get("estado"),
                fecha_inicio=data.get("fecha_inicio"),
            )
            record = result.single()
            return self._node_to_dict(record) if record else None

    def delete_proyecto(self, uid):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (n:Proyecto {id: $id}) DETACH DELETE n RETURN count(n) AS c",
                id=uid,
            )
            return result.single()["c"] > 0

    # ──────────────────────────── OFERTA CRUD ────────────────────────────

    def create_oferta(self, data):
        with self.driver.session() as session:
            data["id"] = data.get("id", str(uuid.uuid4()))
            result = session.run(
                """
                CREATE (n:Oferta {id: $id, titulo: $titulo, descripcion: $descripcion,
                        modalidad: $modalidad, salario: $salario, fecha_publicacion: $fecha_publicacion})
                RETURN n
                """,
                id=data["id"],
                titulo=data.get("titulo", ""),
                descripcion=data.get("descripcion", ""),
                modalidad=data.get("modalidad", "presencial"),
                salario=data.get("salario", ""),
                fecha_publicacion=data.get("fecha_publicacion", ""),
            )
            return self._node_to_dict(result.single())

    def get_all_ofertas(self):
        with self.driver.session() as session:
            result = session.run("MATCH (n:Oferta) RETURN n ORDER BY n.titulo")
            return [self._node_to_dict(r) for r in result]

    def get_oferta(self, uid):
        with self.driver.session() as session:
            result = session.run("MATCH (n:Oferta {id: $id}) RETURN n", id=uid)
            record = result.single()
            return self._node_to_dict(record) if record else None

    def update_oferta(self, uid, data):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (n:Oferta {id: $id})
                SET n.titulo = coalesce($titulo, n.titulo),
                    n.descripcion = coalesce($descripcion, n.descripcion),
                    n.modalidad = coalesce($modalidad, n.modalidad),
                    n.salario = coalesce($salario, n.salario),
                    n.fecha_publicacion = coalesce($fecha_publicacion, n.fecha_publicacion)
                RETURN n
                """,
                id=uid,
                titulo=data.get("titulo"),
                descripcion=data.get("descripcion"),
                modalidad=data.get("modalidad"),
                salario=data.get("salario"),
                fecha_publicacion=data.get("fecha_publicacion"),
            )
            record = result.single()
            return self._node_to_dict(record) if record else None

    def delete_oferta(self, uid):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (n:Oferta {id: $id}) DETACH DELETE n RETURN count(n) AS c",
                id=uid,
            )
            return result.single()["c"] > 0

    # ──────────────────────────── RELATIONSHIP METHODS ────────────────────────────

    def connect_users(self, user1_id, user2_id):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (a:Usuario {id: $id1}), (b:Usuario {id: $id2})
                MERGE (a)-[:CONECTA_CON]->(b)
                MERGE (b)-[:CONECTA_CON]->(a)
                """,
                id1=user1_id, id2=user2_id,
            )

    def disconnect_users(self, user1_id, user2_id):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (a:Usuario {id: $id1})-[r:CONECTA_CON]-(b:Usuario {id: $id2})
                DELETE r
                """,
                id1=user1_id, id2=user2_id,
            )

    def set_works_at(self, user_id, company_id, cargo, fecha_inicio):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (u:Usuario {id: $uid}), (e:Empresa {id: $cid})
                MERGE (u)-[r:TRABAJA_EN]->(e)
                SET r.cargo = $cargo, r.fecha_inicio = $fecha_inicio
                """,
                uid=user_id, cid=company_id, cargo=cargo, fecha_inicio=fecha_inicio,
            )

    def remove_works_at(self, user_id, company_id):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (u:Usuario {id: $uid})-[r:TRABAJA_EN]->(e:Empresa {id: $cid})
                DELETE r
                """,
                uid=user_id, cid=company_id,
            )

    def add_skill_to_user(self, user_id, skill_id):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (u:Usuario {id: $uid}), (h:Habilidad {id: $sid})
                MERGE (u)-[:TIENE_HABILIDAD]->(h)
                """,
                uid=user_id, sid=skill_id,
            )

    def remove_skill_from_user(self, user_id, skill_id):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (u:Usuario {id: $uid})-[r:TIENE_HABILIDAD]->(h:Habilidad {id: $sid})
                DELETE r
                """,
                uid=user_id, sid=skill_id,
            )

    def add_user_to_project(self, user_id, project_id, rol):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (u:Usuario {id: $uid}), (p:Proyecto {id: $pid})
                MERGE (u)-[r:PARTICIPA_EN]->(p)
                SET r.rol = $rol
                """,
                uid=user_id, pid=project_id, rol=rol,
            )

    def remove_user_from_project(self, user_id, project_id):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (u:Usuario {id: $uid})-[r:PARTICIPA_EN]->(p:Proyecto {id: $pid})
                DELETE r
                """,
                uid=user_id, pid=project_id,
            )

    def publish_offer(self, company_id, offer_id):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (e:Empresa {id: $cid}), (o:Oferta {id: $oid})
                MERGE (e)-[:PUBLICA]->(o)
                """,
                cid=company_id, oid=offer_id,
            )

    def add_skill_to_offer(self, offer_id, skill_id):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (o:Oferta {id: $oid}), (h:Habilidad {id: $sid})
                MERGE (o)-[:REQUIERE]->(h)
                """,
                oid=offer_id, sid=skill_id,
            )

    def remove_skill_from_offer(self, offer_id, skill_id):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (o:Oferta {id: $oid})-[r:REQUIERE]->(h:Habilidad {id: $sid})
                DELETE r
                """,
                oid=offer_id, sid=skill_id,
            )

    def apply_to_offer(self, user_id, offer_id, fecha):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (u:Usuario {id: $uid}), (o:Oferta {id: $oid})
                MERGE (u)-[r:POSTULA_A]->(o)
                SET r.fecha = $fecha
                """,
                uid=user_id, oid=offer_id, fecha=fecha,
            )

    def remove_application(self, user_id, offer_id):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (u:Usuario {id: $uid})-[r:POSTULA_A]->(o:Oferta {id: $oid})
                DELETE r
                """,
                uid=user_id, oid=offer_id,
            )

    # ──────────────────────────── QUERY / ANALYTICS ────────────────────────────

    def get_user_connections(self, user_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:Usuario {id: $uid})-[:CONECTA_CON]->(c:Usuario)
                RETURN c
                """,
                uid=user_id,
            )
            return [self._node_to_dict(r, "c") for r in result]

    def get_user_skills(self, user_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:Usuario {id: $uid})-[:TIENE_HABILIDAD]->(h:Habilidad)
                RETURN h
                """,
                uid=user_id,
            )
            return [self._node_to_dict(r, "h") for r in result]

    def get_user_companies(self, user_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:Usuario {id: $uid})-[r:TRABAJA_EN]->(e:Empresa)
                RETURN e, r.cargo AS cargo, r.fecha_inicio AS fecha_inicio
                """,
                uid=user_id,
            )
            return [
                {
                    "empresa": dict(r["e"]),
                    "cargo": r["cargo"],
                    "fecha_inicio": r["fecha_inicio"],
                }
                for r in result
            ]

    def get_user_projects(self, user_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:Usuario {id: $uid})-[r:PARTICIPA_EN]->(p:Proyecto)
                RETURN p, r.rol AS rol
                """,
                uid=user_id,
            )
            return [{"proyecto": dict(r["p"]), "rol": r["rol"]} for r in result]

    def get_user_applications(self, user_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:Usuario {id: $uid})-[r:POSTULA_A]->(o:Oferta)
                RETURN o, r.fecha AS fecha
                """,
                uid=user_id,
            )
            return [{"oferta": dict(r["o"]), "fecha": r["fecha"]} for r in result]

    def get_company_offers(self, company_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (e:Empresa {id: $cid})-[:PUBLICA]->(o:Oferta)
                RETURN o
                """,
                cid=company_id,
            )
            return [self._node_to_dict(r, "o") for r in result]

    def get_offer_skills(self, offer_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (o:Oferta {id: $oid})-[:REQUIERE]->(h:Habilidad)
                RETURN h
                """,
                oid=offer_id,
            )
            return [self._node_to_dict(r, "h") for r in result]

    def get_offer_applicants(self, offer_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:Usuario)-[:POSTULA_A]->(o:Oferta {id: $oid})
                RETURN u
                """,
                oid=offer_id,
            )
            return [self._node_to_dict(r, "u") for r in result]

    def get_project_members(self, project_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:Usuario)-[r:PARTICIPA_EN]->(p:Proyecto {id: $pid})
                RETURN u, r.rol AS rol
                """,
                pid=project_id,
            )
            return [{"usuario": dict(r["u"]), "rol": r["rol"]} for r in result]

    def users_with_similar_skills(self, user_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:Usuario {id: $uid})-[:TIENE_HABILIDAD]->(h:Habilidad)<-[:TIENE_HABILIDAD]-(other:Usuario)
                WHERE other.id <> $uid
                RETURN other, count(h) AS common_skills
                ORDER BY common_skills DESC
                """,
                uid=user_id,
            )
            return [
                {
                    **dict(r["other"]),
                    "habilidades_comunes": r["common_skills"],
                    "common_skills": r["common_skills"],
                    "shared_skills": r["common_skills"],
                    "common_count": r["common_skills"],
                }
                for r in result
            ]

    def common_contacts(self, user1_id, user2_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (a:Usuario {id: $id1})-[:CONECTA_CON]->(c:Usuario)<-[:CONECTA_CON]-(b:Usuario {id: $id2})
                RETURN c
                """,
                id1=user1_id, id2=user2_id,
            )
            return [self._node_to_dict(r, "c") for r in result]

    def shortest_path_user_company(self, user_id, company_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH p = shortestPath(
                    (u:Usuario {id: $uid})-[*]-(e:Empresa {id: $cid})
                )
                RETURN nodes(p) AS nodos
                """,
                uid=user_id, cid=company_id,
            )
            record = result.single()
            if not record:
                return []
            
            nodes_list = []
            for node in record["nodos"]:
                nd = dict(node)
                lbl = list(node.labels)[0] if node.labels else "Nodo"
                # Name can be 'nombre' (Usuario, Empresa, Habilidad, Proyecto) or 'titulo' (Oferta)
                name = nd.get("nombre") or nd.get("titulo") or nd.get("id", "Desconocido")
                nodes_list.append({
                    "id": nd.get("id"),
                    "nombre": name,
                    "label": name,
                    "type": lbl,
                    "tipo": lbl,
                })
            return nodes_list

    def recommend_contacts(self, user_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:Usuario {id: $uid})-[:CONECTA_CON]-(friend:Usuario)-[:CONECTA_CON]-(fof:Usuario)
                WHERE fof.id <> $uid
                  AND NOT (u)-[:CONECTA_CON]-(fof)
                RETURN fof, count(DISTINCT friend) AS mutual_count
                ORDER BY mutual_count DESC
                """,
                uid=user_id,
            )
            return [
                {
                    **dict(r["fof"]),
                    "contactos_mutuos": r["mutual_count"],
                    "mutual_count": r["mutual_count"],
                    "mutuos": r["mutual_count"],
                }
                for r in result
            ]

    def recommend_jobs(self, user_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:Usuario {id: $uid})-[:TIENE_HABILIDAD]->(h:Habilidad)<-[:REQUIERE]-(o:Oferta)
                WHERE NOT (u)-[:POSTULA_A]->(o)
                RETURN o, count(h) AS match_count
                ORDER BY match_count DESC
                """,
                uid=user_id,
            )
            return [
                {
                    **dict(r["o"]),
                    "habilidades_coincidentes": r["match_count"],
                    "match_count": r["match_count"],
                }
                for r in result
            ]

    def related_projects(self, project_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (p1:Proyecto {id: $pid})<-[:PARTICIPA_EN]-(u:Usuario)-[:PARTICIPA_EN]->(p2:Proyecto)
                WHERE p2.id <> $pid
                RETURN DISTINCT p2, count(u) AS shared_members
                ORDER BY shared_members DESC
                """,
                pid=project_id,
            )
            return [
                {**dict(r["p2"]), "miembros_compartidos": r["shared_members"]}
                for r in result
            ]

    def most_influential_users(self, limit=10):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:Usuario)
                OPTIONAL MATCH (u)-[:CONECTA_CON]->(c:Usuario)
                WITH u, count(DISTINCT c) AS conexiones
                OPTIONAL MATCH (u)-[:TRABAJA_EN]->(e:Empresa)
                WITH u, conexiones, count(DISTINCT e) AS empleos
                OPTIONAL MATCH (u)-[:PARTICIPA_EN]->(p:Proyecto)
                WITH u, conexiones, empleos, count(DISTINCT p) AS proyectos
                RETURN u, conexiones + empleos + proyectos AS total
                ORDER BY total DESC
                LIMIT $limit
                """,
                limit=limit,
            )
            return [
                {**dict(r["u"]), "total_conexiones": r["total"]}
                for r in result
            ]

    def detect_communities(self):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:Usuario)
                OPTIONAL MATCH path = (u)-[:CONECTA_CON*1..10]-(connected:Usuario)
                WITH u, collect(DISTINCT connected) AS members
                WITH u, [m IN members | m.id] + [u.id] AS community_ids
                WITH community_ids
                ORDER BY size(community_ids) DESC
                WITH collect(community_ids) AS all_communities
                WITH reduce(acc = [], c IN all_communities |
                    CASE WHEN any(existing IN acc WHERE all(id IN c WHERE id IN existing))
                    THEN acc
                    ELSE acc + [c]
                    END
                ) AS unique_communities
                UNWIND unique_communities AS community
                RETURN community
                """
            )
            communities = []
            for r in result:
                communities.append(r["community"])
            # Enrich communities with user data
            enriched = []
            for i, comm_ids in enumerate(communities):
                result2 = session.run(
                    """
                    MATCH (u:Usuario) WHERE u.id IN $ids
                    RETURN u
                    """,
                    ids=comm_ids,
                )
                members = [self._node_to_dict(r2, "u") for r2 in result2]
                enriched.append({"id": i, "miembros": members})
            return enriched

    def most_demanded_skills(self, limit=10):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (o:Oferta)-[:REQUIERE]->(h:Habilidad)
                RETURN h, count(o) AS demanda
                ORDER BY demanda DESC
                LIMIT $limit
                """,
                limit=limit,
            )
            return [
                {**dict(r["h"]), "demanda": r["demanda"]}
                for r in result
            ]

    def get_full_graph(self):
        nodes = []
        edges = []
        seen_nodes = set()

        with self.driver.session() as session:
            # Get all nodes
            for label in ["Usuario", "Empresa", "Habilidad", "Proyecto", "Oferta"]:
                result = session.run(f"MATCH (n:{label}) RETURN n, labels(n)[0] AS lbl")
                for r in result:
                    node = dict(r["n"])
                    nid = node.get("id")
                    if nid not in seen_nodes:
                        seen_nodes.add(nid)
                        nodes.append({
                            "id": nid,
                            "label": node.get("nombre", node.get("titulo", nid)),
                            "group": r["lbl"],
                        })

            # Get all relationships
            result = session.run(
                """
                MATCH (a)-[r]->(b)
                WHERE a.id IS NOT NULL AND b.id IS NOT NULL
                RETURN a.id AS from_id, b.id AS to_id, type(r) AS rel_type
                """
            )
            for r in result:
                edges.append({
                    "from": r["from_id"],
                    "to": r["to_id"],
                    "label": r["rel_type"],
                })

        return {"nodes": nodes, "edges": edges}
