// ============================================================================
// CONSULTAS CYPHER PARA LA RED PROFESIONAL EN NEO4J
// ProNet Graph - Proyecto Bases de Datos No Relacionales
// ============================================================================

// ----------------------------------------------------------------------------
// 1. RECOMENDACIÓN Y CONEXIONES ENTRE USUARIOS
// ----------------------------------------------------------------------------

// 1.1 ¿Qué usuarios tienen habilidades similares a un usuario dado?
MATCH (u:Usuario {id: $user_id})-[:TIENE_HABILIDAD]->(h:Habilidad)<-[:TIENE_HABILIDAD]-(other:Usuario)
WHERE u.id <> other.id
RETURN other.id AS id, other.nombre AS nombre, other.titulo AS titulo, count(h) AS habilidades_compartidas
ORDER BY habilidades_compartidas DESC
LIMIT 10;

// 1.2 ¿Qué contactos en común existen entre dos profesionales?
MATCH (u1:Usuario {id: $user1_id})-[:CONECTA_CON]-(common:Usuario)-[:CONECTA_CON]-(u2:Usuario {id: $user2_id})
WHERE u1.id <> u2.id
RETURN DISTINCT common.id AS id, common.nombre AS nombre, common.titulo AS titulo;

// 1.3 Recomendación de contactos (Amigos de amigos no conectados aún):
MATCH (u:Usuario {id: $user_id})-[:CONECTA_CON]-(friend:Usuario)-[:CONECTA_CON]-(fof:Usuario)
WHERE u.id <> fof.id 
  AND NOT (u)-[:CONECTA_CON]-(fof)
RETURN fof.id AS id, fof.nombre AS nombre, fof.titulo AS titulo, count(DISTINCT friend) AS contactos_en_comun
ORDER BY contactos_en_comun DESC
LIMIT 10;

// ----------------------------------------------------------------------------
// 2. CAMINOS Y RUTAS MÁS CORTAS
// ----------------------------------------------------------------------------

// 2.1 ¿Cuál es la ruta más corta entre un usuario y una empresa?
MATCH p = shortestPath((u:Usuario {id: $user_id})-[*]-(e:Empresa {id: $company_id}))
RETURN [node IN nodes(p) | {id: node.id, nombre: coalesce(node.nombre, node.titulo), label: labels(node)[0]}] AS ruta,
       length(p) AS distancia;

// ----------------------------------------------------------------------------
// 3. EMPLEABILIDAD Y VINCULACIÓN CANDIDATO - OFERTA
// ----------------------------------------------------------------------------

// 3.1 ¿Qué candidatos podrían recomendarse para una oferta según sus competencias?
MATCH (o:Oferta {id: $offer_id})-[:REQUIERE]->(h:Habilidad)<-[:TIENE_HABILIDAD]-(u:Usuario)
WHERE NOT (u)-[:POSTULA_A]->(o)
RETURN u.id AS id, u.nombre AS nombre, u.titulo AS titulo, count(h) AS habilidades_coincidentes
ORDER BY habilidades_coincidentes DESC
LIMIT 10;

// 3.2 ¿Qué ofertas laborales se le recomiendan a un usuario según sus habilidades?
MATCH (u:Usuario {id: $user_id})-[:TIENE_HABILIDAD]->(h:Habilidad)<-[:REQUIERE]-(o:Oferta)
OPTIONAL MATCH (e:Empresa)-[:PUBLICA]->(o)
WHERE NOT (u)-[:POSTULA_A]->(o)
RETURN o.id AS id, o.titulo AS titulo, o.modalidad AS modalidad, o.salario AS salario,
       e.nombre AS empresa, count(h) AS habilidades_coincidentes
ORDER BY habilidades_coincidentes DESC
LIMIT 10;

// ----------------------------------------------------------------------------
// 4. COLABORACIÓN Y PROYECTOS
// ----------------------------------------------------------------------------

// 4.1 ¿Qué proyectos comparten tecnologías o miembros relacionados?
MATCH (p1:Proyecto {id: $project_id})<-[:PARTICIPA_EN]-(u:Usuario)-[:PARTICIPA_EN]->(p2:Proyecto)
WHERE p1.id <> p2.id
RETURN DISTINCT p2.id AS id, p2.nombre AS nombre, p2.estado AS estado, count(u) AS miembros_compartidos
ORDER BY miembros_compartidos DESC;

// ----------------------------------------------------------------------------
// 5. PANEL DE ANALÍTICA DE GRAFOS
// ----------------------------------------------------------------------------

// 5.1 ¿Qué habilidades son las más demandadas en las ofertas?
MATCH (o:Oferta)-[:REQUIERE]->(h:Habilidad)
RETURN h.id AS id, h.nombre AS nombre, h.categoria AS categoria, count(o) AS demanda
ORDER BY demanda DESC
LIMIT 10;

// 5.2 Usuarios más influyentes (Grado de conectividad global en la red):
MATCH (u:Usuario)
OPTIONAL MATCH (u)-[:CONECTA_CON]->(c:Usuario)
WITH u, count(DISTINCT c) AS conexiones
OPTIONAL MATCH (u)-[:TRABAJA_EN]->(e:Empresa)
WITH u, conexiones, count(DISTINCT e) AS empleos
OPTIONAL MATCH (u)-[:PARTICIPA_EN]->(p:Proyecto)
WITH u, conexiones, empleos, count(DISTINCT p) AS proyectos
RETURN u.id AS id, u.nombre AS nombre, u.titulo AS titulo,
       (conexiones + empleos + proyectos) AS total_conexiones
ORDER BY total_conexiones DESC
LIMIT 10;

// 5.3 Detección de comunidades / componentes conexos de la red de usuarios:
MATCH (u:Usuario)
OPTIONAL MATCH path = (u)-[:CONECTA_CON*1..6]-(connected:Usuario)
WITH u, collect(DISTINCT connected.id) + [u.id] AS comunidad
RETURN DISTINCT comunidad;

