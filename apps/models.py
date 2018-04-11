from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os
import uuid
from django.core.files.images import get_image_dimensions


def upload_profile_image(self, imagename):  # to give unique id to images uploaded
    ext = imagename.split('.')[-1]
    first_part = uuid.uuid4()
    imagename = "%s.%s" % (first_part,  ext)
    return os.path.join('profile_pic/', imagename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    profile_pic = models.ImageField(upload_to=upload_profile_image, default='profile_pic/default.jpg')

    def __str__(self):
        return self.user.username

    def for_json(self):
        return dict(
            name=self.name,
            city=self.city,
            # profile_pic=self.profile_pic
        )


def get_image_name(self, imagename):  # to give unique id to images uploaded
    ext = imagename.split('.')[-1]
    second_part = uuid.uuid4()
    first_part = self.category
    imagename = "%s/%s.%s" % (first_part, second_part,  ext)
    return os.path.join('category_image/', imagename)


class EasyInstruction(models.Model):
    instr = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "EasyInstruction :- " + str(self.id)


class MediumInstruction(models.Model):
    instr = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "MediumInstruction :- " + str(self.id)


class HardInstruction(models.Model):
    instr = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "HardInstruction :- " + str(self.id)


class Category(models.Model):
    category = models.CharField(max_length=200)
    cat_img = models.ImageField(upload_to=get_image_name, default='category_image/default.png', help_text="Aspect ratio must be near 3;2")
    time_per_ques_easy = models.IntegerField(default=20)
    time_per_ques_medium = models.IntegerField(default=40)
    time_per_ques_hard = models.IntegerField(default=60)
    easy_instr = models.ManyToManyField(EasyInstruction)
    medium_instr = models.ManyToManyField(MediumInstruction)
    hard_instr = models.ManyToManyField(HardInstruction)

    def __str__(self):
        return self.category

    def validate(self):
        cat_name = self.category.lower()
        print(cat_name)
        if Category.objects.filter(category=cat_name).exclude(id=self.id).exists():
            raise ValidationError("Category name should be unique")

        width, height = get_image_dimensions(self.cat_img.file)
        ratio = width/height
        if ratio >= 1.6 or ratio <= 1.4:
            raise ValidationError("Image aspect ratio must be near 3:2")

    def save(self, *args, **kwargs):
        self.validate()
        # cat = self.category
        # cat_dict = [cat.category for cat in Category.objects.all()]
        # width, height = get_image_dimensions(self.cat_img.file)
        # ratio = width/height
        # if cat in cat_dict:
        #     raise ValidationError("Category already exist")
        # if ratio>=1.6 or ratio <=1.4:
        #     raise ValidationError("Image aspect ratio must be near 3:2")
        self.category = self.category.lower()
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
            question=self.question,
            option1=self.option1,
            option2=self.option2,
            option3=self.option3,
            option4=self.option4,
            answer=self.answer
        )


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    all_score = models.FloatField(default=0.0)
    easy_score = models.FloatField(default=0.0)
    medium_score = models.FloatField(default=0.0)
    hard_score = models.FloatField(default=0.0)


    def __str__(self):
        return str(self.user.username)+ "_" + str(self.category.category)
