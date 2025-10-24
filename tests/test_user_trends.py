import requests
import json
from typing import Optional, Dict, Any
from enum import Enum


BASE_URL = "http://127.0.0.1:8000"
USER_EMAIL = "user3@api.com"
USER_PWD = "SecurePass333"
DAYS_TO_QUERY = 5

# --- Definición de Métricas  ---
class MetricType(str, Enum):
    """Tipos de métricas disponibles para la consulta de tendencias."""
    AVERAGE = "avg"
    MINIMUM = "min"
    MAXIMUM = "max"


# --- Funciones Auxiliares ---
def print_response(title: str, response: requests.Response) -> Optional[Dict[str, Any]]:
    """Función auxiliar para imprimir la respuesta de la API."""
    print(f"\n--- {title} ---")
    print(f"Estado: {response.status_code}")
    data = None
    try:
        data = response.json()
        print("Respuesta:", json.dumps(data, indent=2))
    except requests.exceptions.JSONDecodeError:
        print("Respuesta (Error sin JSON):", response.text)
        
    print("-" * 30)
    return data

def login_and_get_token(email: str, pwd: str) -> Optional[Dict[str, str]]:
    """Intenta iniciar sesión y devuelve el diccionario de headers con el token si tiene éxito."""
    login_data = {"email": email, "password": pwd}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    data = print_response("POST /auth/login (Obtener Token)", response) 
    
    if response.status_code == 200 and data:
        token = data.get("access_token")
        if token:
            return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    print("ERROR FATAL: Login fallido. No se pudo obtener el token de acceso.")
    return None

def run_trends_test(headers: Dict[str, str], last_days: int, metric: MetricType):
    """Ejecuta la consulta GET /user/trends con una métrica específica."""
    metric_value = metric.value
    metric_name = metric.name
    
    url = f"{BASE_URL}/user/trends?last_days={last_days}&metric_type={metric_value}"
    
    response = requests.get(url, headers=headers)
    print_response(f"GET /user/trends (Tipo: {metric_name})", response)
    
    if response.status_code != 200:
        print(f"ATENCIÓN: La prueba {metric_name} falló con el código de estado {response.status_code}.")
    else:
        print(f"ÉXITO: La prueba {metric_name} completó satisfactoriamente.")


# ----------------------------------------------------------------------
# FLUJO PRINCIPAL DE PRUEBA
# ----------------------------------------------------------------------

if __name__ == "__main__":
    print("="*50)
    print("INICIANDO PRUEBAS: CONSULTA DE TENDENCIAS DINÁMICAS")
    print("="*50)

    # 1. LOGIN
    headers = login_and_get_token(USER_EMAIL, USER_PWD)

    if headers:
        print("\n--- INICIANDO PRUEBAS DE TENDENCIAS ---")
        
        # 2. PROBAR AVG (PROMEDIO)
        run_trends_test(headers, DAYS_TO_QUERY, MetricType.AVERAGE)

        # 3. PROBAR MIN (MÍNIMO)
        run_trends_test(headers, DAYS_TO_QUERY, MetricType.MINIMUM)

        # 4. PROBAR MAX (MÁXIMO)
        run_trends_test(headers, DAYS_TO_QUERY, MetricType.MAXIMUM)
        
        print("\n" + "="*50)
    else:
        print("\n" + "="*50)
        print("PRUEBAS NO EJECUTADAS debido al fallo de Login.")
        
    print("PRUEBAS DE TENDENCIAS COMPLETADAS.")
    print("="*50)