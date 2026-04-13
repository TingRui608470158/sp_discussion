from allauth.account.forms import LoginForm, SignupForm

_FIELD_CLASS = (
    'mt-1 w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900 '
    'shadow-sm focus:border-teal-600 focus:outline-none focus:ring-2 focus:ring-teal-600/30'
)
_CHECKBOX_CLASS = 'h-4 w-4 rounded border-slate-300 text-teal-600 focus:ring-teal-600'


class TailwindLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if getattr(field.widget, 'input_type', None) == 'checkbox' or name == 'remember':
                field.widget.attrs.setdefault('class', _CHECKBOX_CLASS)
            else:
                field.widget.attrs.setdefault('class', _FIELD_CLASS)


class TailwindSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if getattr(field.widget, 'input_type', None) == 'checkbox':
                field.widget.attrs.setdefault('class', _CHECKBOX_CLASS)
            else:
                field.widget.attrs.setdefault('class', _FIELD_CLASS)
