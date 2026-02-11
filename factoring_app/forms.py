from django import forms
from .models import Bordero, Cliente, Banco


class BorderoForm(forms.ModelForm):
    class Meta:
        model = Bordero
        fields = ['numero', 'cliente', 'banco', 'data_envio', 'observacoes']
        widgets = {
            'data_envio': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        if not numero:
            raise forms.ValidationError('O número do bordero é obrigatório.')
        if Bordero.objects.filter(numero=numero).exists():
            raise forms.ValidationError('Número já cadastrado.')
        return numero
