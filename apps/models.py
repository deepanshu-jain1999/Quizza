from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os, uuid
from django.core.files.images import get_image_dimensions

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic/', blank=True)

    def __str__(self):
        return self.user.username


def get_image_name(self, imagename):  # to give unique id to images uploaded
    ext = imagename.split('.')[-1]
    second_part = uuid.uuid4()
    first_part = self.category
    imagename = "%s/%s.%s" % (first_part, second_part,  ext)
    return os.path.join('category_image/', imagename)


class Category(models.Model):
    category = models.CharField(max_length=200)
    cat_img = models.ImageField(upload_to=get_image_name, default='category_image/default.png', help_text="Aspect ratio must be near 3;2")

    def __str__(self):
        return self.category

    def save(self, *args, **kwargs):
        cat = self.category
        cat_dict = [cat.category for cat in Category.objects.all()]
        width, height = get_image_dimensions(self.cat_img.file)
        ratio = width/height
        if cat in cat_dict:
            raise ValidationError("Category already exist")
        if ratio>=1.6 or ratio <=1.4:
            raise ValidationError("Image aspect ratio must be near 3:2")
        super().save(*args, **kwargs)

    def for_json(self):
        image_url = self.get_absolute_image_url()
        return dict(
            cat=self.category,
            img=image_url,
        )

    def get_absolute_image_url(self):
        print(self.cat_img.url)
        return "{0}".format(self.cat_img.url)


# choice = (("PRIVATE", "Private"), ("PUBLIC", "Public"),)
level_choice = (("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard"))


class Quiz(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=level_choice, default="NONE")
    question = models.TextField(max_length=1000)
    option1 = models.CharField(max_length=500)
    option2 = models.CharField(max_length=500)
    option3 = models.CharField(max_length=500)
    option4 = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)

    def __str__(self):
        return str(self.category.category)

    def for_json(self):
        return dict(
            id=self.id,
            question=self.question,
            option1=self.option1,
            option2=self.option2,
            option3=self.option3,
            option4=self.option4,
            answer=self.answer
        )


class CompeteQuiz(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question = models.TextField(max_length=1000)
    option1 = models.CharField(max_length=500)
    option2 = models.CharField(max_length=500)
    option3 = models.CharField(max_length=500)
    option4 = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)

    def __str__(self):
        return str(self.category.category)

    def for_json(self):
        return dict(
            id=self.id,
            question=self.question,
            option1=self.option1,
            option2=self.option2,
            option3=self.option3,
            option4=self.option4,
            answer=self.answer
        )


