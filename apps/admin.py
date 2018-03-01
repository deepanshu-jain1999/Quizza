from django.contrib import admin
from apps.models import Profile, Quiz
# Register your models here.
admin.site.register(Profile)


class QuizAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Category', {'fields': ['category']}),
        ('Question', {'fields': ['question']}),
        ('Options', {'fields': ['option1', 'option2', 'option3', 'option4'], }),
        ('Answer', {'fields': ['answer'], }),
    ]


admin.site.register(Quiz, QuizAdmin)
