from django import forms
from .models import *

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfileModel
#         fields = '__all__'
#         exclude = ['user']
#         labels = {
#             "biografia": 'Ingrese una biografia: ',
#             "profile_pic": "Ingrese una foto de perfil: "
#         }
class ProfileForm(forms.Form):
    biografia = forms.CharField(widget=forms.Textarea, required=False, label="Ingrese una biografia: ")
    profile_pic = forms.ImageField(required=False, label="Ingrese una foto de perfil: ")

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'excerpt', 'image_name', 'content', 'tags']
        labels = {
            "title": 'Titulo del blog',
            "excerpt": 'Descripcion breve de lo que aborda el blog',
            "image_name": 'Imagen para el blog',
            "content": 'Contenido del blog',
            "tags": 'Tags'
        }
