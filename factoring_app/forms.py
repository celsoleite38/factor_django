from django import forms
from .models import Bordero, Cliente, Banco, Documento, TipoDocumento, Sacado


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


class DocumentoForm(forms.ModelForm):
    """Formulário para criar/editar documentos num borderô"""
    sacado_nome = forms.CharField(
        max_length=150, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome do devedor'
        })
    )
    sacado_cpf_cnpj = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'CPF ou CNPJ'
        })
    )
    desconto = forms.DecimalField(
        max_digits=15,
        decimal_places=2,
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01'
        })
    )
    
    class Meta:
        model = Documento
        fields = [
            'tipo_documento', 'numero_documento', 'valor', 
            'data_vencimento', 'data_emissao', 'valor_liquido'
        ]
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número do documento'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'data_vencimento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'data_emissao': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'valor_liquido': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
        }
