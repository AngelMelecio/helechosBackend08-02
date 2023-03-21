from django.db import models


class Pedido(models.Model):

    idPedido = models.AutoField(auto_created=True, primary_key=True)
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    idModelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    fechaActual = models.DateTimeField()
    fechaEntrega = models.DateTimeField()
    proveedores = models.CharField(max_length=200)


class DetallePedido(models.Model):
    idDetallePedido = models.AutoField(auto_created=True, primary_key=True)
    idPedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    talla = models.CharField(max_length=50)
    cantidad = models.CharField(max_length=50)


class Reposicion(models.Model):
    idReposicion = models.AutoField(auto_created=True, primary_key=True)
    fecha = models.DateTimeField()
    idPedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    idMaquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    idEmpleadoRepuso = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name='%(class)s_empleado_repuso')
    idEmpleadoRevisor = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name='%(class)s_empleado_revisor')
    cantidad = models.CharField(max_length=50)





class Produccion(models.Model):
    idProduccion = models.AutoField(auto_created=True, primary_key=True)
    idPedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    idDetallePedido = models.ForeignKey(
        DetallePedido, on_delete=models.CASCADE)
    idEtiqueta = models.CharField(max_length=20)
    tejido = models.BooleanField()
    fechaTejido = models.DateTimeField()
    idEmpleadoTejedor = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name='%(class)s_empleado_tejedor')
    idMaquinaTejido = models.ForeignKey(
        Maquina,
        on_delete=models.CASCADE,
        related_name='%(class)s_maquina_tejido')
    plancha = models.BooleanField()
    fechaPlancha = models.DateTimeField()
    idEmpleadoPlanchador = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name='%(class)s_empleado_planchador')
    idMaquinaPlancha = models.ForeignKey(
        Maquina,
        on_delete=models.CASCADE,
        related_name='%(class)s_maquina_plancha')
    corte = models.BooleanField()
    fechaCorte = models.DateTimeField()
    idEmpleadoCortador = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name='%(class)s_empleado_cortador')
    idMaquinaCorte = models.ForeignKey(
        Maquina,
        on_delete=models.CASCADE,
        related_name='%(class)s_maquina_corte')
    empaque = models.BooleanField()
    fechaEmpaque = models.DateTimeField()
    idEmpleadoEmpacador = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name='%(class)s_empleado_empacador')
    salida = models.BooleanField()
    fechaSalida = models.DateTimeField()
    idEmpleadoRepartidor = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name='%(class)s_empleado_repartidor')
    numSemana = models.CharField(max_length=20)
