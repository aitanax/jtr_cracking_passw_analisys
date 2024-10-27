import bcrypt
from concurrent.futures import ThreadPoolExecutor
import os
import time


def cargar_credenciales(archivo):
    """Carga las credenciales de un archivo en un diccionario."""
    with open(archivo, 'r', encoding='utf-8') as f:
        return {usuario: hash_contraseña for usuario, hash_contraseña in
                (linea.strip().split(':') for linea in f)}


def verificar_contraseña(contraseña, hash_contraseña):
    """Verifica la contraseña contra el hash bcrypt."""
    return bcrypt.checkpw(contraseña.encode('utf-8'), hash_contraseña.encode('utf-8'))


def procesar_usuario(usuario, contraseña, credenciales_meneate, resultados):
    """Procesa un usuario verificando la contraseña y guarda el resultado si coincide."""
    if usuario in credenciales_meneate and verificar_contraseña(contraseña, credenciales_meneate[usuario]):
        resultados.append(f"{usuario}:{contraseña}\n")


def main():
    inicio = time.time()
    
    # Archivos de entrada y salida
    archivo_passwords_cracked = 'g22_foromotos.txt' # DataSet crackeado de foromotos
    archivo_meneate = 'g22_meneate_entrada.txt' # DataSet sin crackear 
    archivo_resultados = 'g22_meneate.txt' # DataSet crackeado de meneate

    # Cargar credenciales de archivos
    if not all(map(os.path.exists, [archivo_passwords_cracked, archivo_meneate])):
        print("Uno o más archivos no encontrados.")
        return

    print("Cargando credenciales...")
    credenciales_passwords = cargar_credenciales(archivo_passwords_cracked)
    credenciales_meneate = cargar_credenciales(archivo_meneate)

    resultados = []

    # Verificación en paralelo
    print("Verificando contraseñas...")
    with ThreadPoolExecutor(max_workers=8) as executor:
        for usuario, contraseña in credenciales_passwords.items():
            executor.submit(procesar_usuario, usuario, contraseña, credenciales_meneate, resultados)

    # Guardar resultados
    with open(archivo_resultados, 'w', encoding='utf-8') as f:
        f.writelines(resultados)

    print(f"Total de contraseñas encontradas: {len(resultados)}.")
    print(f"Resultados guardados en {archivo_resultados}")
    print(f"Tiempo de ejecución: {time.time() - inicio:.2f} segundos.")


if __name__ == '__main__':
    main()
