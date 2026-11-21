from proyecto_final_programacion.conexion import engine
from proyecto_final_programacion.modelos import Base

def crear_tablas():
    Base.metadata.create_all(engine)
    print("Tablas de categorias, equipos, clientes y arriendos creadas correctamente")

if __name__ == "__main__":
    crear_tablas()

