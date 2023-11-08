import django
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from django.utils import timezone


class Category (models.Model):
    name = models.CharField(max_length=100, help_text="Введите категории")
    def __str__(self):
        return self.name

class CastomUser(AbstractUser):
    first_name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    last_name = models.CharField(max_length=254, verbose_name='Фамилия', blank=False)
    email = models.CharField(max_length=254, verbose_name='Пoчтa', blank=False)
    password = models.CharField(max_length=254, verbose_name='Пapoль', blank=False)
    role = models.CharField(max_length=254, verbose_name='Poль',
                            choices=(('admin', 'Администратор'), ('user', 'Пoльзователь')), default='user')

class Application(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(help_text="Опишите свою заявку ")
    STATUS_CHOICES = [
        ('N', 'Новая'),
        ('P', 'Принято в работу'),
        ('C', 'Выполнено')
    ]

    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 2.0
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    category = models.ForeignKey(Category, help_text='Выберите категорию', on_delete=models.CASCADE)
    photo_file = models.ImageField(max_length=254, upload_to='image/', validators=[validate_image, FileExtensionValidator(['jpg', 'jpeg', 'png', 'bmp'])])
    status = models.CharField(max_length=254, verbose_name='Статус', choices=STATUS_CHOICES, default='N')
    date = models.DateTimeField(verbose_name='Дата добавления', default=django.utils.timezone.now)
    user = models.ForeignKey(CastomUser, verbose_name='Пользователь', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('application_leist', args=[str(self.id)])

    def __str__(self):
        return self.title
