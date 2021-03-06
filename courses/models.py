from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.backends.base import base
from .fields import OrderField
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class Subject(models.Model):
    """Предмет"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    """Курс"""
    owner = models.ForeignKey(User,
                                related_name='courses_created',
                                on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True) 
    students = models.ManyToManyField(User,
                                        related_name='courses_joined',
                                        blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model):
    """Модуль"""
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # орядок будет больше на единицу, чем у предыдущего модуля курса
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.title}'


class Content(models.Model):
    """Содержание"""
    module = models.ForeignKey(Module,
                                related_name='contents',
                                on_delete=models.CASCADE)
    # внешний ключ, ForeignKey, на модель ContentType                        
    content_type = models.ForeignKey(ContentType,
                                    on_delete=models.CASCADE,
                                    limit_choices_to={'model__in':(
                                        'text',
                                        'video',
                                        'image',
                                        'file'
                                    )})
    # идентификатор связанного объекта типа PositiveIntegerField                                
    object_id = models.PositiveIntegerField()
    # поле типа GenericForeignKey, которое обобщает данные из предыду-щих двух
    item = GenericForeignKey('content_type', 'object_id')
    # порядковые номера объектов будут задаваться в рамках одного модуля
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    """Абстрактный клас"""
    owner = models.ForeignKey(User,
                            related_name='%(class)s_related',
                            on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string('courses/content/{}.html'.format(
            self._meta.model_name), {'item': self})


class Text(ItemBase):
    """для текста"""
    content = models.TextField()


class File(ItemBase):
    """для файлов"""
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    """для картинок"""
    file = models.FileField(upload_to='images') 


class Video(ItemBase):
    """для видео"""
    url = models.URLField()