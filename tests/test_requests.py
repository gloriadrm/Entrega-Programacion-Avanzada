# Script de prueba para validar la funcionalidad central de la API (Usuario y Logs).
# Debe ejecutarse en un entorno donde el servidor (uvicorn main:app --reload) esté activo.

import requests
import json
from typing import Optional, Dict

# --- Configuración ---
BASE_URL = "http://127.0.0.1:8000"
TEST_USER = "test.user@healthy.com"
TEST_PWD = "Pwd123456"
TEST_DATE = "2025-10-23" # Usar una fecha que no sea futura

# --- Datos de Prueba ---
SIGNUP_DATA = {
    "name": "Maria Test",
    "age": 28,
    "email": TEST_USER,
    "password": TEST_PWD
}

UPDATE_USER_DATA = {
    "age": 29
}

LOG_DATA_CREATE = {
    "log_date": TEST_DATE,
    "steps": 10500,
    "exercise_minutes": 60,
    "sleep_hours": 7.8,
    "water_liters": 2.5,
    "diet_score": 8,
    "mood": 9
}

LOG_DATA_UPDATE = {
    "log_date": TEST_DATE,
    "sleep_hours": 8.5  # Actualizamos solo las horas de sueño (PUT)
}

# ----------------------------------------------------------------------
# FUNCIONES DE UTILIDAD
# ----------------------------------------------------------------------

def print_response(step_number: int, title: str, response: requests.Response):
    """Función auxiliar para imprimir la respuesta de la API."""
    print(f"\n--- {step_number}. {title} ---")
    print(f"Estado: {response.status_code}")
    try:
        data = response.json()
        print("Respuesta:", json.dumps(data, indent=2))
        return data
    except requests.exceptions.JSONDecodeError:
        print("Respuesta (Error sin JSON):", response.text)
        return None
    print("-" * 30)

def get_auth_headers(token: str) -> Dict[str, str]:
    """Devuelve el diccionario de headers de autenticación."""
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# ----------------------------------------------------------------------
# FUNCIONES DE SOLICITUDES ESPECÍFICAS
# ----------------------------------------------------------------------

def run_signup(step: int, data: Dict) -> bool:
    """Ejecuta el endpoint de creación de cuenta."""
    response = requests.post(f"{BASE_URL}/auth/signup", json=data)
    print_response(step, "SIGN UP (POST)", response)
    
    if response.status_code == 400 and "ya está registrado" in response.text:
        print("INFO: Usuario ya existe. Continuando con el Login.")
    
    return True

def run_login(step: int, user: str, pwd: str) -> Optional[str]:
    """Ejecuta el endpoint de login y devuelve el token JWT."""
    login_data = {"email": user, "password": pwd}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    data = print_response(step, "LOGIN (POST)", response)
    
    if response.status_code == 200 and data and "access_token" in data:
        return data["access_token"]
    else:
        print("ERROR FATAL: Login fallido. Terminando prueba.")
        return None

def run_get_profile(step: int, headers: Dict[str, str]):
    """Ejecuta el GET del perfil de usuario."""
    response = requests.get(f"{BASE_URL}/user/account", headers=headers)
    print_response(step, "GET PERFIL", response)

def run_update_user(step: int, headers: Dict[str, str], data: Dict):
    """Ejecuta el PUT de actualización de usuario."""
    response = requests.put(f"{BASE_URL}/user/account", headers=headers, json=data)
    print_response(step, "PUT ACTUALIZAR EDAD", response)

def run_create_log(step: int, headers: Dict[str, str], data: Dict):
    """Ejecuta el POST para crear un log diario."""
    response = requests.post(f"{BASE_URL}/user/logs", headers=headers, json=data)
    print_response(step, "POST CREAR LOG", response)

def run_update_log(step: int, headers: Dict[str, str], data: Dict):
    """Ejecuta el PUT para actualizar un log diario existente."""
    response = requests.put(f"{BASE_URL}/user/logs", headers=headers, json=data)
    print_response(step, "PUT ACTUALIZAR LOG", response)

# ----------------------------------------------------------------------
# FUNCIÓN PRINCIPAL DE EJECUCIÓN
# ----------------------------------------------------------------------

def main():
    print("\n" + "="*50)
    print(f"INICIANDO PRUEBAS CORE DE API EN: {BASE_URL}")
    print("="*50)
    
    try:
        # 1. SIGN UP (POST)
        run_signup(1, SIGNUP_DATA)
        
        # 2. LOGIN (POST)
        token = run_login(2, TEST_USER, TEST_PWD)
        if not token:
            return

        headers = get_auth_headers(token)

        # 3. GET PERFIL (GET)
        run_get_profile(3, headers)
        
        # 4. PUT ACTUALIZAR EDAD (PUT)
        run_update_user(4, headers, UPDATE_USER_DATA)
        
        # 5. POST CREAR LOG (POST)
        run_create_log(5, headers, LOG_DATA_CREATE)
        
        # 6. PUT ACTUALIZAR LOG (PUT)
        run_update_log(6, headers, LOG_DATA_UPDATE)

        print("\n" + "="*50)
        print("PRUEBAS BÁSICAS COMPLETADAS. VERIFIQUE LOS ESTADOS 200/201.")
        print("="*50)

    except requests.exceptions.ConnectionError:
        print("\nERROR: No se pudo conectar a la API.")
        print("Asegúrate de que 'uvicorn main:app --reload' esté corriendo en otra terminal.")
    except Exception as e:
        print(f"\nERROR INESPERADO: {e}")

if __name__ == "__main__":
    main()
