import requests
import json
from datetime import date
from typing import Optional, Dict, Any

BASE_URL = "http://127.0.0.1:8000"
USER_EMAIL = "user2@api.com"
USER_PWD = "SecurePass222" 

LOG_DATA_UPDATE = {
    "log_date": date.today().isoformat(),
    "sleep_hours": 8.8, # Nuevo valor para PUT
    "exercise_minutes": 45
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

def step_2_update_log(headers: Dict[str, str]):
    """Prueba la actualización de un log existente."""
    response = requests.put(f"{BASE_URL}/user/logs", headers=headers, json=LOG_DATA_UPDATE)
    print_response(2, "PUT /user/logs (Actualizar Log Diario)", response)
    
    if response.status_code == 200:
        print("Resultado: ÉXITO - Log actualizado.")
    else:
        print("ERROR: Falló la actualización del log.")

if __name__ == "__main__":
    print("==================================================")
    print("INICIANDO PRUEBA 4: MODIFICACIÓN DE LOG DIARIO")
    print("==================================================")
    auth_headers = login_and_get_token()
    if auth_headers:
        step_2_update_log(auth_headers)
