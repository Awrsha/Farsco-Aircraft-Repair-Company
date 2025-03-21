# Generated by Django 5.0.7 on 2025-03-20 22:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="courseenrollment",
            name="progress_percent",
        ),
        migrations.RemoveField(
            model_name="coursereview",
            name="updated_at",
        ),
        migrations.AlterField(
            model_name="coursereview",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت"),
        ),
        migrations.AlterField(
            model_name="coursereview",
            name="rating",
            field=models.PositiveSmallIntegerField(
                choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], verbose_name="امتیاز"
            ),
        ),
        migrations.AlterField(
            model_name="coursereview",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="course_reviews",
                to=settings.AUTH_USER_MODEL,
                verbose_name="کاربر",
            ),
        ),
        migrations.CreateModel(
            name="CourseModule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="عنوان ماژول")),
                ("description", models.TextField(blank=True, verbose_name="توضیحات")),
                (
                    "order",
                    models.PositiveSmallIntegerField(
                        default=0, verbose_name="ترتیب نمایش"
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="modules",
                        to="courses.course",
                        verbose_name="دوره",
                    ),
                ),
            ],
            options={
                "verbose_name": "ماژول دوره",
                "verbose_name_plural": "ماژول\u200cهای دوره",
                "ordering": ["course", "order"],
            },
        ),
    ]
