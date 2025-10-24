import requests
import json
from datetime import date, timedelta
from typing import Optional, Dict, Any

BASE_URL = "http://127.0.0.1:8000"
USER_EMAIL = "user3@api.com"
USER_PWD = "SecurePass333"

# Calculamos fechas anteriores
DATE_YESTERDAY = date.today() - timedelta(days=5)

LOG_DATA_CREATE = {
    "log_date": DATE_YESTERDAY.isoformat(),   # date.today().isoformat() 
    "steps": 3000,
    "exercise_minutes": 60,
    "sleep_hours": 8,
    "diet_score": 7,
    "water_liters": 1,
    "mood": 8
}

# --- FUNCIÓN AUXILIAR PARA IMPRIMIR LA RESPUESTA ---
def print_response(title: str, response: requests.Response) -> Optional[Dict[str, Any]]:
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

def step_2_create_log(headers: Dict[str, str]):
    """Crea el registro diario (POST)."""
    response = requests.post(f"{BASE_URL}/user/logs", headers=headers, json=LOG_DATA_CREATE)
    print_response(2, "POST /user/logs (Crear Log Diario)", response)
    
    if response.status_code in [200, 201]:
        print("Resultado: ÉXITO - Log creado.")
    elif response.status_code == 400 and "Ya existe un log" in response.text:
        print("Resultado: INFO - Log ya existía.")
    else:
        print("ERROR: Falló la creación del log.")

if __name__ == "__main__":
    print("==================================================")
    print("INICIANDO PRUEBA 3: CREACIÓN DE LOG DIARIO")
    print("==================================================")
    auth_headers = login_and_get_token()
    if auth_headers:
        step_2_create_log(auth_headers)
