#import resource
from import_export import resources  
from .models import Excel  

class ExcelResource(resources.ModelResource):  
    class Meta:  
        model = Excel  