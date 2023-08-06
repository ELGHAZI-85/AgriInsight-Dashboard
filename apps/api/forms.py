# Automated Form Generation for SQLAlchemy Models in Flask using WTForms-Alchemy

from wtforms import Form
from wtforms_alchemy import model_form_factory
from apps.models import *



ModelForm = model_form_factory(Form)

class BookForm(ModelForm):
    class Meta:
        model = Book
        
        
        
BaseModelForm = model_form_factory(Form)

class VentilationForm(BaseModelForm):
    class Meta:
        model = Ventilation

