import os
import django
import random
from django.shortcuts import get_object_or_404


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from datacenter.models import Mark, Chastisement, Schoolkid, Lesson, Commendation

WISHES = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
          'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
          'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!',
          'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!',
          'Замечательно!', 'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!', 'Здорово!',
          'Это как раз то, что нужно!', 'Я тобой горжусь!', 'С каждым разом у тебя получается всё лучше!',
          'Мы с тобой не зря поработали!', 'Я вижу, как ты стараешься!', 'Ты растешь над собой!',
          'Ты многое сделал, я это вижу!', 'Теперь у тебя точно все получится!']


def fix_marks(fio):
    child = get_object_or_404(Schoolkid, full_name__contains=fio)
    schoolkid_marks = Mark.objects.filter(schoolkid=child, points__in=[2, 3])
    schoolkid_marks.update(points=5)


def remove_chastisements(fio):
    child = get_object_or_404(Schoolkid, full_name__contains=fio)
    schoolkid_chastisements = Chastisement.objects.filter(schoolkid=child)
    schoolkid_chastisements.delete()


def create_commendation(fio, subject):
    child = get_object_or_404(Schoolkid, full_name__contains=fio)
    child_random_lesson = Lesson.objects.filter(year_of_study=child.year_of_study,
                                                group_letter=child.group_letter,
                                                subject__title=subject).order_by('?').first()
    Commendation.objects.create(text=random.choice(WISHES),
                                created=child_random_lesson.date,
                                schoolkid=child,
                                subject=child_random_lesson.subject,
                                teacher=child_random_lesson.teacher)
