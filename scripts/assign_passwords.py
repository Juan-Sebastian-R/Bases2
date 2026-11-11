import random
from database import Neo4jDB

db = Neo4jDB()
with db.driver.session() as session:
    result = session.run("MATCH (n:Usuario) RETURN n.id AS id, n.nombre AS nombre, n.password AS password")
    records = list(result)
    print(f"Total usuarios en base de datos: {len(records)}")
    
    for r in records:
        uid = r["id"]
        current_pwd = r["password"]
        if not current_pwd:
            new_pwd = str(random.randint(100000, 999999))
            session.run("MATCH (n:Usuario {id: $id}) SET n.password = $pwd", id=uid, pwd=new_pwd)
            print(f"  ✓ Asignada clave a {r['nombre']}: {new_pwd}")
        else:
            print(f"  ✓ {r['nombre']} ya tiene clave: {current_pwd}")

print("\n¡Listo! Todos los usuarios tienen contraseñas de 6 dígitos.")
