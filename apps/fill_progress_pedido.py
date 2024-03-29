
from django.db import transaction
from apps.Pedidos.models import Pedido
from apps.Produccion.models import Produccion

# Inicia una transacción para asegurar la consistencia de la base de datos
with transaction.atomic():
    for pedido in Pedido.objects.all():
            print(pedido)
            total_empacado = 0
            total_ordinario = 0

            # Filtra los registros de producción de tipo 'Ordinario' para este pedido
            producciones_ordinarias = Produccion.objects.filter(detallePedido__pedido=pedido, tipo='Ordinario')
            total_ordinario = sum(produccion.cantidad for produccion in producciones_ordinarias)

            # Filtra los registros de producción 'Empacados' para este pedido
            producciones_empacadas = Produccion.objects.filter(detallePedido__pedido=pedido, estacionActual='empacado', tipo='Ordinario')
            total_empacado = sum(produccion.cantidad for produccion in producciones_empacadas)

            # Prepara el nuevo valor para el campo 'progreso'
            progreso_data = {
                'total': total_ordinario,
                'progreso': total_empacado,
                'estado': 'Terminado' if total_ordinario == total_empacado else 'Pendiente'
            }
            print(progreso_data)
            # Actualiza el pedido con el nuevo valor de 'progreso'
            pedido.progreso = progreso_data
            pedido.save()