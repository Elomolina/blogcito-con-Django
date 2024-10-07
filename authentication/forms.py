from django import forms

class LoginForm(forms.Form):
    username_email = forms.CharField(max_length=200, required=True, label="Ingrese username o email: ",error_messages={
        'required': 'This field is required'
    })
    password = forms.CharField(max_length=200, widget=forms.PasswordInput, label="Contraseña: ",required=True, error_messages={
        'required': 'This field is required'
    })


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)
    last_name = forms.CharField(max_length=200, required=True)
    username = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(max_length=200, required=True)
    #include image field
    password = forms.CharField(max_length=200, required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=200, required=True, widget=forms.PasswordInput)