from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px; border-radius: 8px; background: rgba(15,23,42,0.8); color: #fff; border: 1px solid rgba(255,255,255,0.2); margin-bottom: 15px;'}),
            'category': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px; border-radius: 8px; background: rgba(15,23,42,0.8); color: #fff; border: 1px solid rgba(255,255,255,0.2); margin-bottom: 15px;'}),
            'content': forms.Textarea(attrs={'rows': 5, 'style': 'width: 100%; padding: 10px; border-radius: 8px; background: rgba(15,23,42,0.8); color: #fff; border: 1px solid rgba(255,255,255,0.2); margin-bottom: 15px;'}),
            'image': forms.FileInput(attrs={'style': 'margin-bottom: 15px; color: #fff;'}),
        }