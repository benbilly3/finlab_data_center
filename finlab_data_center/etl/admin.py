from django.contrib import admin
from django_q import models as q_models
from django_q import admin as q_admin

admin.site.unregister([q_models.Success])


@admin.register(q_models.Success)
class ChildClassAdmin(q_admin.TaskAdmin):
    list_display = ("group", "name", "func", "started", "stopped", "time_taken", "result",)
    search_fields = ("name", "func")
    list_filter = ("group", "func")


admin.site.unregister([q_models.Failure])


@admin.register(q_models.Failure)
class ChildClassAdmin(q_admin.FailAdmin):
    list_display = ('group', 'name', 'func', 'result', 'started')
    search_fields = ("name", "func")
    list_filter = ("group", "func")
