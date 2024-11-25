import requests
from datetime import datetime
from feriados.models import Feriado


def obtener_feriados(api_key, country="CL", year="2024"):
    """
    Obtiene los feriados de la API de Calendarific.

    :param api_key: Clave de acceso a la API.
    :param country: Código del país (por defecto 'CL' para Chile).
    :param year: Año para el cual se consultarán los feriados.
    :return: Lista de feriados obtenidos de la API o None en caso de error.
    """
    url = "https://calendarific.com/api/v2/holidays"
    params = {
        "api_key": api_key, 
        "country": country,
        "year": year,
    }
    print(f"Enviando solicitud a la API de Calendarific...\nURL: {url}\nParámetros: {params}")
    
    try:
        response = requests.get(url, params=params)
        print(f"Código de estado: {response.status_code}")
        response.raise_for_status() 
        data = response.json()
        holidays = data.get("response", {}).get("holidays", [])
        print(f"Feriados obtenidos: {len(holidays)}")
        return holidays
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con la API: {e}")
        return None
    except ValueError as e:
        print(f"Error al procesar JSON de la API: {e}")
        return None


def guardar_feriados(feriados):
    """
    Guarda los feriados obtenidos en la base de datos.

    :param feriados: Lista de feriados obtenidos de la API.
    """
    if not feriados:
        print("No se recibieron feriados para guardar.")
        return

    for feriado in feriados:
        try:
            iso_date = feriado["date"]["iso"]
            date = iso_date.split("T")[0] 
            region = feriado.get("locations", "Nacional") 

            
            obj, created = Feriado.objects.get_or_create(
                name=feriado["name"],
                date=date,
                defaults={"region": region},
            )

            if created:
                print(f"Feriado creado: {obj.name} ({obj.date})")
            else:
                print(f"Feriado ya existente: {obj.name} ({obj.date})")

        except Exception as e:
            print(f"Error al procesar el feriado '{feriado.get('name', 'Desconocido')}': {e}")


def actualizar_feriados():
    """
    Función principal para obtener y guardar los feriados desde la API externa.
    """
    api_key = "4dlrihgSzDp6to2fNCTTHftITbijBu4c"  
    feriados = obtener_feriados(api_key)
    if feriados:
        guardar_feriados(feriados)
    else:
        print("No se pudieron obtener feriados desde la API.")
