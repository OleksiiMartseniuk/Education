from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


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

    class Meta:
        ordering = ['-created']


class Module(models.Model):
    """Модуль"""
    course = models.ForeignKey(Course,
                                related_name='modules',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Content(models.Model):
    """Содержание"""
    modul = models.ForeignKey(Module,
                            related_name='contents',
                            on_delete=models.CASCADE)
    # внешний ключ, ForeignKey, на модель ContentType                        
    content_type = models.ForeignKey(ContentType,
                                    on_delete=models.CASCADE)
    # идентификатор связанного объекта типа PositiveIntegerField                                
    object_id = models.PositiveIntegerField()
    # поле типа GenericForeignKey, которое обобщает данные из предыду-щих двух
    item = GenericForeignKey('content_type', 'object_id')
