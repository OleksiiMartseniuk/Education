from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Course


class OwnerMixin(object):
    # получения базового QuerySetʼа
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin ,ListView):
    """Cписок курсов, созданных пользователем"""
    template_name = 'courses/manage/course/list.html'


class CourseCreateView(PermissionRequiredMixin, OwnerCourseEditMixin, CreateView):
    """Использует модельную форму для создания нового курса"""
    permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin, OwnerCourseEditMixin, UpdateView):
    """Позволяет владельцу курса редактировать его"""
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin, OwnerCourseMixin, DeleteView):
    """Позволяет владельцу удалить курс"""
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')
    permission_required = 'courses.delete_course'
