import requests
from django.core.management.base import BaseCommand
from feriados.models import Feriado

class Command(BaseCommand):
    help = 'Sincroniza feriados desde la API externa'

    def handle(self, *args, **kwargs):
        API_URL = 'https://calendarific.com/api/v2/holidays'
        API_KEY = '4dlrihgSzDp6to2fNCTTHftITbijBu4c'
        params = {
            'api_key': API_KEY,
            'country': 'CL',
            'year': 2024,
        }

        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            for holiday in data['response']['holidays']:
                # Extraer la fecha en el formato correcto
                full_date = holiday['date']['iso']
                formatted_date = full_date.split("T")[0]  # Tomar solo la parte 'YYYY-MM-DD'

                # Obtener el nombre y la región
                name = holiday.get('name', 'Feriado sin nombre')
                region = holiday.get('locations', 'Nacional')  # Mapea 'Nacional' si no hay región específica

                # Crear o actualizar el feriado
                Feriado.objects.update_or_create(
                    date=formatted_date,
                    defaults={
                        'name': name,
                        'region': region if region != 'Nacional' else None,
                    }
                )
            self.stdout.write(self.style.SUCCESS('Feriados sincronizados correctamente.'))
        else:
            self.stdout.write(self.style.ERROR(f"Error al sincronizar: {response.status_code}"))
