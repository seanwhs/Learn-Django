# category app forms.py
from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']

    def clean_title(self):
        title = self.cleaned_data['title'].strip().title()
        if Category.objects.filter(title__iexact=title).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This category already exists.")
        return title
