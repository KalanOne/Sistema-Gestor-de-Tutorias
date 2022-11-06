#import resource
from import_export import resources  
from .models import Excel2  

class ExcelResource(resources.ModelResource):  
    class Meta:  
        model = Excel2  