from django.contrib import admin
from .models import Subject, Course, Module

"""Регистрация модели Предметы"""
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


"""Добавления модели Модуль в модель Курс"""
class ModuleInline(admin.StackedInline):
    model = Module


"""Регистрация модели Курс"""
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
