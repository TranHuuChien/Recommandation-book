from django import forms
from .models.models import MyUser

class MyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username','first_name','last_name', 'email', 'birth', 'sex', 'address', 'password',]
        widgets={
            'username': forms.TextInput(attrs={'class':'form-control', 'tabindex':'1', 'placeholder':'Username'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'tabindex':'1', 'placeholder':'Email Address', 'required':'true'}),
            'first_name': forms.TextInput(attrs={'class':'form-control', 'tabindex':'1', 'placeholder':'First Name', 'required':'true'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'tabindex':'1', 'placeholder':'Last Name', 'required':'true'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'tabindex':'1', 'placeholder':'Address', 'required':'true'}),
            'birth': forms.DateInput(format=('%Y-%m-%d'),attrs={'type':'date', 'required':'true'}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'tabindex':'1', 'placeholder':'Password', 'required':'true'}),
            'sex': forms.RadioSelect(attrs={'type':'radio', 'required':'true'}),
        }