from import_export import resources  
from .models import *

class ExcelResource(resources.ModelResource):  
    class Meta:  
        model = registrarAlumno  

class ExcelPersonalTec(resources.ModelResource):  
    class Meta:  
        model = registrarPersonalTec