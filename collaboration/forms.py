from django import forms

from .models import PainPoint

_FIELD_CLASS = (
    'mt-1 w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900 '
    'shadow-sm focus:border-accent-500 focus:outline-none focus:ring-2 focus:ring-accent-500/30'
)


class PainPointForm(forms.ModelForm):
    class Meta:
        model = PainPoint
        fields = [
            'category',
            'title',
            'context',
            'current_solution',
            'pain_score',
            'potential_value',
        ]
        widgets = {
            'context': forms.Textarea(attrs={'rows': 8}),
            'current_solution': forms.Textarea(attrs={'rows': 6}),
            'potential_value': forms.Textarea(attrs={'rows': 4}),
            'title': forms.TextInput(),
            'category': forms.Select(),
            'pain_score': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _name, field in self.fields.items():
            field.widget.attrs.setdefault('class', _FIELD_CLASS)
