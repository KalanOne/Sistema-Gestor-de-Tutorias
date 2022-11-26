from import_export import resources  
from .models import registrarAlumno  

class ExcelResource(resources.ModelResource):  
    class Meta:  
        model = registrarAlumno  