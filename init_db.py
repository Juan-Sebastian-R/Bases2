"""
init_db.py - Initialize the Neo4j database with rich sample data
for the professional network application.
"""

from database import Neo4jDB


def main():
    db = Neo4jDB()
    print("=" * 60)
    print("  Inicializando base de datos de Red Profesional")
    print("=" * 60)

    # ──────────────────────────── USUARIOS ────────────────────────────
    print("\n📌 Creando usuarios...")
    usuarios_data = [
        {"nombre": "Carlos Andrés Martínez", "email": "carlos.martinez@email.com", "titulo": "Ingeniero de Software Senior", "ubicacion": "Bogotá", "resumen": "Desarrollador full-stack con 8 años de experiencia en aplicaciones web y móviles."},
        {"nombre": "María Alejandra López", "email": "maria.lopez@email.com", "titulo": "Data Scientist", "ubicacion": "Medellín", "resumen": "Científica de datos especializada en machine learning y análisis predictivo."},
        {"nombre": "Juan Sebastián Rodríguez", "email": "juan.rodriguez@email.com", "titulo": "DevOps Engineer", "ubicacion": "Bogotá", "resumen": "Ingeniero DevOps con experiencia en AWS, Docker y CI/CD pipelines."},
        {"nombre": "Laura Valentina García", "email": "laura.garcia@email.com", "titulo": "Frontend Developer", "ubicacion": "Cali", "resumen": "Desarrolladora frontend especializada en React y UX/UI design."},
        {"nombre": "Andrés Felipe Hernández", "email": "andres.hernandez@email.com", "titulo": "Backend Developer", "ubicacion": "Barranquilla", "resumen": "Desarrollador backend con experiencia en Python, Django y microservicios."},
        {"nombre": "Sofía Catalina Ramírez", "email": "sofia.ramirez@email.com", "titulo": "Project Manager", "ubicacion": "Medellín", "resumen": "Gerente de proyectos certificada en Scrum y metodologías ágiles."},
        {"nombre": "Diego Alejandro Torres", "email": "diego.torres@email.com", "titulo": "Mobile Developer", "ubicacion": "Bogotá", "resumen": "Desarrollador móvil con experiencia en Flutter y Kotlin."},
        {"nombre": "Valentina Fernández", "email": "valentina.fernandez@email.com", "titulo": "UX/UI Designer", "ubicacion": "Cartagena", "resumen": "Diseñadora de experiencia de usuario con enfoque en diseño centrado en el usuario."},
        {"nombre": "Santiago Morales", "email": "santiago.morales@email.com", "titulo": "Cloud Architect", "ubicacion": "Bogotá", "resumen": "Arquitecto cloud con certificaciones en AWS y experiencia en infraestructura escalable."},
        {"nombre": "Camila Andrea Vargas", "email": "camila.vargas@email.com", "titulo": "Cybersecurity Analyst", "ubicacion": "Medellín", "resumen": "Analista de ciberseguridad especializada en pentesting y seguridad de redes."},
        {"nombre": "Nicolás Esteban Díaz", "email": "nicolas.diaz@email.com", "titulo": "Full Stack Developer", "ubicacion": "Cali", "resumen": "Desarrollador full-stack con experiencia en JavaScript, TypeScript y Node.js."},
        {"nombre": "Isabella Monsalve", "email": "isabella.monsalve@email.com", "titulo": "Data Engineer", "ubicacion": "Barranquilla", "resumen": "Ingeniera de datos con experiencia en ETL pipelines y bases de datos distribuidas."},
        {"nombre": "Mateo Jiménez", "email": "mateo.jimenez@email.com", "titulo": "Machine Learning Engineer", "ubicacion": "Bogotá", "resumen": "Ingeniero de ML con experiencia en modelos de deep learning y NLP."},
        {"nombre": "Gabriela Ríos", "email": "gabriela.rios@email.com", "titulo": "Scrum Master", "ubicacion": "Cartagena", "resumen": "Scrum Master certificada con experiencia liderando equipos ágiles."},
        {"nombre": "Daniel Alejandro Castillo", "email": "daniel.castillo@email.com", "titulo": "QA Engineer", "ubicacion": "Medellín", "resumen": "Ingeniero de calidad con experiencia en automatización de pruebas y CI/CD."},
    ]
    usuarios = []
    for u in usuarios_data:
        user = db.create_usuario(u)
        usuarios.append(user)
        print(f"  ✓ {user['nombre']} ({user['ubicacion']})")

    # ──────────────────────────── EMPRESAS ────────────────────────────
    print("\n🏢 Creando empresas...")
    empresas_data = [
        {"nombre": "TechColombia SAS", "industria": "Tecnología", "ubicacion": "Bogotá", "descripcion": "Empresa líder en desarrollo de software y soluciones tecnológicas.", "sitio_web": "https://techcolombia.com"},
        {"nombre": "DataSoft Solutions", "industria": "Tecnología", "ubicacion": "Medellín", "descripcion": "Startup especializada en inteligencia artificial y big data.", "sitio_web": "https://datasoft.co"},
        {"nombre": "ConsulTIC", "industria": "Consultoría", "ubicacion": "Bogotá", "descripcion": "Consultora de transformación digital para empresas del sector financiero.", "sitio_web": "https://consultic.com.co"},
        {"nombre": "BancoDigital", "industria": "Banca", "ubicacion": "Bogotá", "descripcion": "Banco digital con enfoque en innovación fintech.", "sitio_web": "https://bancodigital.com.co"},
        {"nombre": "CloudNova", "industria": "Tecnología", "ubicacion": "Cali", "descripcion": "Proveedor de servicios cloud y DevOps para empresas.", "sitio_web": "https://cloudnova.co"},
        {"nombre": "InnovaApps", "industria": "Tecnología", "ubicacion": "Barranquilla", "descripcion": "Empresa de desarrollo de aplicaciones móviles y web.", "sitio_web": "https://innovaapps.com"},
    ]
    empresas = []
    for e in empresas_data:
        emp = db.create_empresa(e)
        empresas.append(emp)
        print(f"  ✓ {emp['nombre']} ({emp['industria']})")

    # ──────────────────────────── HABILIDADES ────────────────────────────
    print("\n💡 Creando habilidades...")
    habilidades_data = [
        {"nombre": "Python", "categoria": "Lenguaje de Programación"},
        {"nombre": "Java", "categoria": "Lenguaje de Programación"},
        {"nombre": "JavaScript", "categoria": "Lenguaje de Programación"},
        {"nombre": "React", "categoria": "Framework Frontend"},
        {"nombre": "Node.js", "categoria": "Framework Backend"},
        {"nombre": "Machine Learning", "categoria": "Inteligencia Artificial"},
        {"nombre": "SQL", "categoria": "Base de Datos"},
        {"nombre": "Docker", "categoria": "DevOps"},
        {"nombre": "AWS", "categoria": "Cloud"},
        {"nombre": "Scrum", "categoria": "Metodología"},
        {"nombre": "Django", "categoria": "Framework Backend"},
        {"nombre": "Angular", "categoria": "Framework Frontend"},
        {"nombre": "TypeScript", "categoria": "Lenguaje de Programación"},
        {"nombre": "Data Science", "categoria": "Ciencia de Datos"},
        {"nombre": "DevOps", "categoria": "Infraestructura"},
        {"nombre": "Ciberseguridad", "categoria": "Seguridad"},
        {"nombre": "UX/UI", "categoria": "Diseño"},
        {"nombre": "Kotlin", "categoria": "Lenguaje de Programación"},
        {"nombre": "Flutter", "categoria": "Framework Móvil"},
        {"nombre": "Git", "categoria": "Herramienta"},
    ]
    habilidades = []
    for h in habilidades_data:
        hab = db.create_habilidad(h)
        habilidades.append(hab)
        print(f"  ✓ {hab['nombre']} ({hab['categoria']})")

    # ──────────────────────────── PROYECTOS ────────────────────────────
    print("\n📂 Creando proyectos...")
    proyectos_data = [
        {"nombre": "Portal de Empleo DigitalCO", "descripcion": "Plataforma web para conectar profesionales con ofertas laborales en Colombia.", "estado": "activo", "fecha_inicio": "2024-01-15"},
        {"nombre": "App Banca Móvil 3.0", "descripcion": "Rediseño completo de la aplicación móvil del BancoDigital.", "estado": "activo", "fecha_inicio": "2024-03-01"},
        {"nombre": "Sistema de Analítica Predictiva", "descripcion": "Motor de análisis predictivo para el sector retail usando ML.", "estado": "activo", "fecha_inicio": "2024-06-10"},
        {"nombre": "Migración Cloud AWS", "descripcion": "Migración de infraestructura on-premise a AWS para ConsulTIC.", "estado": "finalizado", "fecha_inicio": "2023-09-01"},
        {"nombre": "Plataforma IoT Industrial", "descripcion": "Sistema IoT para monitoreo de equipos industriales en tiempo real.", "estado": "activo", "fecha_inicio": "2024-08-20"},
    ]
    proyectos = []
    for p in proyectos_data:
        proy = db.create_proyecto(p)
        proyectos.append(proy)
        print(f"  ✓ {proy['nombre']} ({proy['estado']})")

    # ──────────────────────────── OFERTAS ────────────────────────────
    print("\n💼 Creando ofertas laborales...")
    ofertas_data = [
        {"titulo": "Desarrollador Python Senior", "descripcion": "Buscamos un desarrollador Python senior para nuestro equipo de backend.", "modalidad": "hibrido", "salario": "8000000-12000000 COP", "fecha_publicacion": "2024-10-01"},
        {"titulo": "Data Scientist Junior", "descripcion": "Oportunidad para científico de datos con conocimientos en ML y Python.", "modalidad": "remoto", "salario": "5000000-7000000 COP", "fecha_publicacion": "2024-10-05"},
        {"titulo": "Frontend Developer React", "descripcion": "Desarrollador frontend con experiencia en React y TypeScript.", "modalidad": "presencial", "salario": "6000000-9000000 COP", "fecha_publicacion": "2024-10-10"},
        {"titulo": "DevOps Engineer", "descripcion": "Ingeniero DevOps con experiencia en Docker, AWS y CI/CD.", "modalidad": "remoto", "salario": "9000000-14000000 COP", "fecha_publicacion": "2024-10-12"},
        {"titulo": "Mobile Developer Flutter", "descripcion": "Desarrollador móvil con experiencia en Flutter y Dart.", "modalidad": "hibrido", "salario": "7000000-10000000 COP", "fecha_publicacion": "2024-10-15"},
        {"titulo": "Scrum Master", "descripcion": "Scrum Master certificado para liderar equipos de desarrollo ágil.", "modalidad": "presencial", "salario": "8000000-11000000 COP", "fecha_publicacion": "2024-10-18"},
        {"titulo": "Analista de Ciberseguridad", "descripcion": "Analista de seguridad informática con experiencia en pentesting.", "modalidad": "hibrido", "salario": "7000000-10000000 COP", "fecha_publicacion": "2024-10-20"},
        {"titulo": "Full Stack Developer", "descripcion": "Desarrollador full-stack con experiencia en Node.js y Angular.", "modalidad": "remoto", "salario": "7000000-11000000 COP", "fecha_publicacion": "2024-10-22"},
    ]
    ofertas = []
    for o in ofertas_data:
        oferta = db.create_oferta(o)
        ofertas.append(oferta)
        print(f"  ✓ {oferta['titulo']} ({oferta['modalidad']})")

    # ──────────────────────────── RELACIONES ────────────────────────────

    # Helper: get ids by index
    def uid(i):
        return usuarios[i]["id"]

    def eid(i):
        return empresas[i]["id"]

    def hid(i):
        return habilidades[i]["id"]

    def pid(i):
        return proyectos[i]["id"]

    def oid(i):
        return ofertas[i]["id"]

    # --- TRABAJA_EN (users at companies) ---
    print("\n🔗 Creando relaciones laborales (TRABAJA_EN)...")
    work_relations = [
        # TechColombia (0): Carlos(0), Juan(2), Santiago(8)
        (0, 0, "Ingeniero de Software Senior", "2020-03-15", None, True),
        (0, 4, "Desarrollador Junior", "2018-01-10", "2020-02-28", False),
        (2, 0, "DevOps Engineer", "2021-07-01", None, True),
        (8, 0, "Cloud Architect", "2022-01-10", None, True),
        # DataSoft (1): María(1), Mateo(12), Isabella(11)
        (1, 1, "Data Scientist Lead", "2021-05-20", None, True),
        (12, 1, "ML Engineer", "2022-08-15", None, True),
        (11, 1, "Data Engineer", "2023-02-01", None, True),
        # ConsulTIC (2): Sofía(5), Gabriela(13)
        (5, 2, "Project Manager", "2020-11-01", None, True),
        (13, 2, "Scrum Master", "2021-09-15", None, True),
        # BancoDigital (3): Diego(6), Valentina(7)
        (6, 3, "Mobile Developer Lead", "2022-04-01", None, True),
        (7, 3, "UX/UI Designer Senior", "2021-12-01", None, True),
        # CloudNova (4): Andrés(4), Nicolás(10)
        (4, 4, "Backend Developer Senior", "2022-06-15", None, True),
        (4, 0, "Desarrollador Python", "2019-05-01", "2022-05-30", False),
        (10, 4, "Full Stack Developer", "2023-01-10", None, True),
        # InnovaApps (5): Laura(3), Daniel(14), Camila(9)
        (3, 5, "Frontend Developer Lead", "2021-08-01", None, True),
        (14, 5, "QA Engineer", "2022-10-01", None, True),
        (9, 5, "Cybersecurity Analyst", "2023-03-15", None, True),
    ]
    for item in work_relations:
        if len(item) == 4:
            u_idx, e_idx, cargo, fecha_inicio = item
            fecha_fin, actual = None, True
        else:
            u_idx, e_idx, cargo, fecha_inicio, fecha_fin, actual = item
        db.set_works_at(uid(u_idx), eid(e_idx), cargo, fecha_inicio, fecha_fin, actual)
        estado_str = "Actualmente" if actual else f"hasta {fecha_fin}"
        print(f"  ✓ {usuarios[u_idx]['nombre']} → {empresas[e_idx]['nombre']} ({cargo}) [{fecha_inicio} - {estado_str}]")

    # --- CONECTA_CON (connections between users) ---
    print("\n🤝 Creando conexiones entre usuarios (CONECTA_CON)...")
    connections = [
        # Coworkers at TechColombia
        (0, 2), (0, 8), (2, 8),
        # Coworkers at DataSoft
        (1, 12), (1, 11), (12, 11),
        # Coworkers at ConsulTIC
        (5, 13),
        # Coworkers at BancoDigital
        (6, 7),
        # Coworkers at CloudNova
        (4, 10),
        # Coworkers at InnovaApps
        (3, 14), (3, 9), (14, 9),
        # Cross-company connections
        (0, 1),   # Carlos - María (tech community)
        (0, 5),   # Carlos - Sofía (previous project)
        (1, 12),  # María - Mateo (data science community)
        (2, 4),   # Juan - Andrés (DevOps meetup)
        (3, 7),   # Laura - Valentina (design community)
        (5, 6),   # Sofía - Diego (project management)
        (8, 2),   # Santiago - Juan (cloud community)
        (9, 10),  # Camila - Nicolás (security)
        (1, 4),   # María - Andrés (python community)
        (0, 6),   # Carlos - Diego (university friends)
        (11, 14), # Isabella - Daniel (data community)
        (13, 5),  # Gabriela - Sofía (already coworkers, handled by MERGE)
        (3, 10),  # Laura - Nicolás (JS community)
    ]
    for i, j in connections:
        db.connect_users(uid(i), uid(j))
        print(f"  ✓ {usuarios[i]['nombre']} ↔ {usuarios[j]['nombre']}")

    # --- TIENE_HABILIDAD (user skills) ---
    print("\n🎯 Asignando habilidades a usuarios...")
    # Skills index: 0=Python, 1=Java, 2=JavaScript, 3=React, 4=Node.js,
    # 5=ML, 6=SQL, 7=Docker, 8=AWS, 9=Scrum, 10=Django, 11=Angular,
    # 12=TypeScript, 13=DataScience, 14=DevOps, 15=Ciberseguridad,
    # 16=UX/UI, 17=Kotlin, 18=Flutter, 19=Git
    user_skills = {
        0: [0, 2, 3, 10, 6, 19],         # Carlos: Python, JS, React, Django, SQL, Git
        1: [0, 5, 6, 13, 19],             # María: Python, ML, SQL, DataScience, Git
        2: [0, 7, 8, 14, 19],             # Juan: Python, Docker, AWS, DevOps, Git
        3: [2, 3, 12, 16, 19],            # Laura: JS, React, TypeScript, UX/UI, Git
        4: [0, 10, 4, 6, 7, 19],          # Andrés: Python, Django, Node.js, SQL, Docker, Git
        5: [9, 19],                        # Sofía: Scrum, Git
        6: [1, 17, 18, 19],               # Diego: Java, Kotlin, Flutter, Git
        7: [16, 2, 3, 19],                # Valentina: UX/UI, JS, React, Git
        8: [0, 8, 7, 14, 19],             # Santiago: Python, AWS, Docker, DevOps, Git
        9: [0, 15, 6, 19],                # Camila: Python, Ciberseguridad, SQL, Git
        10: [2, 4, 11, 12, 6, 19],        # Nicolás: JS, Node.js, Angular, TypeScript, SQL, Git
        11: [0, 6, 7, 8, 13, 19],         # Isabella: Python, SQL, Docker, AWS, DataScience, Git
        12: [0, 5, 13, 6, 19],            # Mateo: Python, ML, DataScience, SQL, Git
        13: [9, 19],                       # Gabriela: Scrum, Git
        14: [0, 2, 7, 19, 9],             # Daniel: Python, JS, Docker, Git, Scrum
    }
    for u_idx, skill_indices in user_skills.items():
        for s_idx in skill_indices:
            db.add_skill_to_user(uid(u_idx), hid(s_idx))
        print(f"  ✓ {usuarios[u_idx]['nombre']}: {', '.join(habilidades[s]['nombre'] for s in skill_indices)}")

    # --- PARTICIPA_EN (users in projects) ---
    print("\n📋 Asignando usuarios a proyectos...")
    project_members = [
        # Portal de Empleo DigitalCO (0)
        (0, 0, "Tech Lead"),
        (4, 0, "Backend Developer"),
        (3, 0, "Frontend Developer"),
        (5, 0, "Project Manager"),
        # App Banca Móvil 3.0 (1)
        (6, 1, "Mobile Lead"),
        (7, 1, "UX/UI Designer"),
        (0, 1, "Backend Advisor"),
        (14, 1, "QA Lead"),
        # Sistema de Analítica Predictiva (2)
        (1, 2, "Data Science Lead"),
        (12, 2, "ML Engineer"),
        (11, 2, "Data Engineer"),
        # Migración Cloud AWS (3)
        (2, 3, "DevOps Lead"),
        (8, 3, "Cloud Architect"),
        (9, 3, "Security Specialist"),
        # Plataforma IoT Industrial (4)
        (10, 4, "Full Stack Developer"),
        (4, 4, "Backend Developer"),
        (13, 4, "Scrum Master"),
    ]
    for u_idx, p_idx, rol in project_members:
        db.add_user_to_project(uid(u_idx), pid(p_idx), rol)
        print(f"  ✓ {usuarios[u_idx]['nombre']} → {proyectos[p_idx]['nombre']} ({rol})")

    # --- PUBLICA (companies publish offers) ---
    print("\n📢 Publicando ofertas por empresas...")
    offer_publishers = [
        (0, 0),  # TechColombia -> Desarrollador Python Senior
        (1, 1),  # DataSoft -> Data Scientist Junior
        (5, 2),  # InnovaApps -> Frontend Developer React
        (0, 3),  # TechColombia -> DevOps Engineer
        (3, 4),  # BancoDigital -> Mobile Developer Flutter
        (2, 5),  # ConsulTIC -> Scrum Master
        (5, 6),  # InnovaApps -> Analista de Ciberseguridad
        (4, 7),  # CloudNova -> Full Stack Developer
    ]
    for e_idx, o_idx in offer_publishers:
        db.publish_offer(eid(e_idx), oid(o_idx))
        print(f"  ✓ {empresas[e_idx]['nombre']} → {ofertas[o_idx]['titulo']}")

    # --- REQUIERE (offers require skills) ---
    print("\n📝 Asignando habilidades requeridas a ofertas...")
    offer_skills = {
        0: [0, 10, 6, 7, 19],             # Python Senior: Python, Django, SQL, Docker, Git
        1: [0, 5, 6, 13],                  # Data Scientist: Python, ML, SQL, DataScience
        2: [2, 3, 12, 16],                 # Frontend React: JS, React, TypeScript, UX/UI
        3: [7, 8, 14, 0, 19],             # DevOps: Docker, AWS, DevOps, Python, Git
        4: [18, 17, 19],                   # Mobile Flutter: Flutter, Kotlin, Git
        5: [9],                             # Scrum Master: Scrum
        6: [15, 0, 6],                     # Ciberseguridad: Ciberseguridad, Python, SQL
        7: [2, 4, 11, 12, 6],             # Full Stack: JS, Node.js, Angular, TypeScript, SQL
    }
    for o_idx, skill_indices in offer_skills.items():
        for s_idx in skill_indices:
            db.add_skill_to_offer(oid(o_idx), hid(s_idx))
        print(f"  ✓ {ofertas[o_idx]['titulo']}: {', '.join(habilidades[s]['nombre'] for s in skill_indices)}")

    # --- POSTULA_A (users apply to offers) ---
    print("\n✉️ Creando postulaciones...")
    applications = [
        (4, 0, "2024-10-05"),   # Andrés -> Python Senior
        (10, 7, "2024-10-25"),  # Nicolás -> Full Stack
        (3, 2, "2024-10-12"),   # Laura -> Frontend React
        (7, 2, "2024-10-13"),   # Valentina -> Frontend React
        (2, 3, "2024-10-14"),   # Juan -> DevOps
        (8, 3, "2024-10-15"),   # Santiago -> DevOps
        (6, 4, "2024-10-18"),   # Diego -> Mobile Flutter
        (13, 5, "2024-10-20"),  # Gabriela -> Scrum Master
        (5, 5, "2024-10-21"),   # Sofía -> Scrum Master
        (9, 6, "2024-10-22"),   # Camila -> Ciberseguridad
        (1, 1, "2024-10-08"),   # María -> Data Scientist
        (12, 1, "2024-10-09"),  # Mateo -> Data Scientist
        (0, 0, "2024-10-03"),   # Carlos -> Python Senior
        (14, 3, "2024-10-16"),  # Daniel -> DevOps
    ]
    for u_idx, o_idx, fecha in applications:
        db.apply_to_offer(uid(u_idx), oid(o_idx), fecha)
        print(f"  ✓ {usuarios[u_idx]['nombre']} → {ofertas[o_idx]['titulo']} ({fecha})")

    # ──────────────────────────── RESUMEN ────────────────────────────
    print("\n" + "=" * 60)
    print("  ✅ Base de datos inicializada exitosamente")
    print("=" * 60)
    print(f"\n  📊 Resumen de datos creados:")
    print(f"     • Usuarios:      {len(usuarios)}")
    print(f"     • Empresas:      {len(empresas)}")
    print(f"     • Habilidades:   {len(habilidades)}")
    print(f"     • Proyectos:     {len(proyectos)}")
    print(f"     • Ofertas:       {len(ofertas)}")
    print(f"     • Relaciones laborales (TRABAJA_EN):     {len(work_relations)}")
    print(f"     • Conexiones (CONECTA_CON):              {len(connections)}")
    print(f"     • Habilidades asignadas (TIENE_HABILIDAD): {sum(len(v) for v in user_skills.values())}")
    print(f"     • Membresías en proyectos (PARTICIPA_EN): {len(project_members)}")
    print(f"     • Ofertas publicadas (PUBLICA):          {len(offer_publishers)}")
    print(f"     • Habilidades requeridas (REQUIERE):     {sum(len(v) for v in offer_skills.values())}")
    print(f"     • Postulaciones (POSTULA_A):             {len(applications)}")
    print()

    db.close()


if __name__ == "__main__":
    main()
