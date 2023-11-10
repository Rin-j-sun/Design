from .models import CastomUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django import forms


from .validators import validate_pasword_len


class RegisterUserForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Имя',
        validators=[RegexValidator('^[а-яА-Я- -]+$',
                                   message="Разрешены только кириллица, дефис и пробелы")],
        error_messages={'required': 'Обязательное поле', }
    )
    last_name = forms.CharField(
        label='Фамилия',
        validators=[RegexValidator('^[а-яА-Я- -]+$',
                                   message="Разрешены только кириллица, дефис и пробелы")],
        error_messages={'required': 'Обязательное поле', }
    )
    username = forms.CharField(label='Логин',
                                validators=[RegexValidator('^[a-zA-Z0-9-]+$',
                                                                message = "Разрешены только латиница, цифры или тире")],
                                error_messages={
                                        'required': 'Обязательное поле',
                                        'unique': 'Данный логин занят'
                                })
    email = forms.EmailField(label='Anpec злектронной почт',
                            error_messages={
                                'invalid': 'Hе правильный формат адреса',
                                'unique': 'Данный адрес занят'
                            })
    password = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput,
                                validators=[validate_pasword_len],
                                error_messages={
                                    'required': 'Обязательное поле',
                                })
    password2 = forms.CharField(label='Пapоль (повторно)',
                                widget=forms.PasswordInput,
                                error_messages={
                                    'required': 'Обязательное поле',
                                })
    rules = forms.BooleanField(required=True,
                                label='Согласие с правилами регистрации',
                               error_messages={
                                   'required': 'Обязательное поле',
                               })
    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError({
                'password2': ValidationError('Введенные пароли не совпадант', соdе='password_mismatch')
        })
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user
    class Meta:
        model = CastomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'password2', 'rules')



