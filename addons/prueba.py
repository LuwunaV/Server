import subprocess
import re

def update_git_remote_url():
    try:
        # Obtener el nombre de usuario actual de GitHub
        result = subprocess.run(
            ["gh", "api", "user", "--jq", ".login"],
            check=True,
            capture_output=True,
            text=True
        )
        login = result.stdout.strip()
        print(f"Nombre de usuario de GitHub obtenido: {login}")

        # Obtener la URL remota actual
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            check=True,
            capture_output=True,
            text=True
        )
        remote_url = result.stdout.strip()
        print(f"URL remota actual obtenida: {remote_url}")

        # Extraer el nombre del repositorio de la URL remota
        match = re.search(r'github\.com/([^/]+)/([^/]+)\.git', remote_url)
        if match:
            repo_name = match.group(2)
            print(f"Nombre del repositorio obtenido: {repo_name}")

            # Construir la nueva URL remota usando el nombre de usuario y el nombre del repositorio
            new_url = f"https://github.com/{login}/{repo_name}.git"

            # Establecer la nueva URL remota
            subprocess.run(
                ["git", "remote", "set-url", "origin", new_url],
                check=True
            )
            print(f"URL remota actualizada a: {new_url}")
        else:
            print("No se pudo extraer el nombre del repositorio de la URL remota.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        print("GitHub CLI (gh) no está instalado o no se encuentra en el PATH.")

# Llamar a la función
update_git_remote_url()
