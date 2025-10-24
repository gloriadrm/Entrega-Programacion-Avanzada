import requests
import json
from typing import Optional, Dict, Any

BASE_URL = "http://127.0.0.1:8000"
USER_EMAIL = "user2@api.com"
USER_PWD = "SecurePass222" 

UPDATE_USER_DATA = {
    "age": 22,
    "name": "User2"
}

# --- FUNCIÓN AUXILIAR PARA IMPRIMIR LA RESPUESTA ---
def print_response(step_number: int, title: str, response: requests.Response) -> Optional[Dict[str, Any]]:
    """Función auxiliar para imprimir la respuesta de la API y devolver el JSON."""
    print(f"\n--- {step_number}. {title} ---")
    print(f"Estado: {response.status_code}")
    
    data = None
    try:
        data = response.json()
        print("Respuesta:", json.dumps(data, indent=2))
    except requests.exceptions.JSONDecodeError:
        print("Respuesta (Error sin JSON):", response.text)
        
    print("-" * 30)
    return data
# ----------------------------------------------------

def login_and_get_token():
    # CORRECCIÓN: Cambiar 'data=' por 'json=' para enviar el cuerpo como JSON
    login_data = {"email": USER_EMAIL, "password": USER_PWD} 
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data) 
    data = print_response(1, "POST /auth/login (Obtener Token)", response)
    if response.status_code == 200 and data:
        token = data.get("access_token")
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    print("ERROR FATAL: Login fallido.")
    return None

def update_user(headers: Dict[str, str]):
    """Actualiza el perfil del usuario (PUT)."""
    response = requests.put(f"{BASE_URL}/user/account", headers=headers, json=UPDATE_USER_DATA)
    print_response(2, "PUT /user/account (Actualizar Nombre/Edad)", response)
    return response.status_code == 200

if __name__ == "__main__":
    print("==================================================")
    print("INICIANDO PRUEBA 2: LOGIN Y MODIFICACIÓN DE PERFIL")
    print("==================================================")
    auth_headers = login_and_get_token()
    if auth_headers:
        update_user(auth_headers)
