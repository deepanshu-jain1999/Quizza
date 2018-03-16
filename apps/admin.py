from django.contrib import admin
from apps.models import Profile, Quiz, Category
# Register your models here.
admin.site.register(Profile)
admin.site.register(Category)


class QuizAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Category', {'fields': ['category']}),
        ('Level Of Quiz', {'fields': ['level']}),
        ('Question', {'fields': ['question']}),
        ('Options', {'fields': ['option1', 'option2', 'option3', 'option4'], }),
        ('Answer', {'fields': ['answer'], }),
    ]


admin.site.register(Quiz, QuizAdmin)
