from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.core.exceptions import ValidationError
from .models import AssetRecord
import pandas as pd









# Register A New User

class CreateUserForm(UserCreationForm):
    class Meta:
        
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
        
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput()) 
    password = forms.CharField(widget=PasswordInput()) 
    
class AddRecordForm(forms.ModelForm):
    excel_file = forms.FileField(required=False)
    
    class Meta:
        model = AssetRecord
        fields = ['description', 'asset_code', 'serial_number_t24', 'nomenclature', 'serial_number', 'location',  'price', 'unit', 'date_purchase', 'supplier', 'warranty', 'comments', 'excel_file']
                 


class UpdateRecordForm(forms.ModelForm):
    
    class Meta:
        model = AssetRecord
        fields = ['description', 'asset_code', 'serial_number_t24', 'nomenclature', 'serial_number', 'location',  'price', 'unit', 'date_purchase', 'supplier', 'warranty', 'comments']
                 
                