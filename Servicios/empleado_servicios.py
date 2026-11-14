from modelos.empleado import Empleado
from Datos import EmpleadoDAO

class EmpleadoService:
    """Clase intermediaria que orquesta las reglas de negocio y el acceso a datos."""
    
    @staticmethod
    def registrar_empleado(id_empleado, nombre, direccion, telefono, correo, fecha_inicio, salario, id_departamento):
        
        
        nuevo_empleado = Empleado(
            id_empleado=id_empleado,
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            correo_electronico=correo,
            fecha_inicio_contrato=fecha_inicio,
            salario=salario
        )
        
        
        EmpleadoDAO.registrar_empleado(
            id_empleado=nuevo_empleado.id_empleado,
            nombre=nuevo_empleado.nombre,
            direccion=nuevo_empleado.direccion,
            telefono=nuevo_empleado.telefono,
            correo=nuevo_empleado.correo_electronico,
            fecha_inicio=str(nuevo_empleado.fecha_inicio_contrato), 
            salario=nuevo_empleado.salario,
            id_departamento=id_departamento
        )
        
        
        return nuevo_empleado