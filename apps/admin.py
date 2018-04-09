from django.contrib import admin
from apps.models import Profile, CompeteQuiz, Quiz, Category, EasyInstruction, MediumInstruction, HardInstruction, Score
# Register your models here.
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(EasyInstruction)
admin.site.register(MediumInstruction)
admin.site.register(HardInstruction)
admin.site.register(Score)
admin.site.register(CompeteQuiz)



class QuizAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Category', {'fields': ['category']}),
        ('Level Of Quiz', {'fields': ['level']}),
        ('Question', {'fields': ['question']}),
        ('Options', {'fields': ['option1', 'option2', 'option3', 'option4'], }),
        ('Answer', {'fields': ['answer'], }),
    ]


admin.site.register(Quiz, QuizAdmin)
