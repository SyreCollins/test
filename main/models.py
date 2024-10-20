from django.db import models


class Question(models.Model):
    question_main = models.TextField(help_text="Main Question", null=True, blank=True, max_length=50000)
    a = models.TextField(null=True, blank=True)
    b = models.TextField(null=True, blank=True)
    c = models.TextField(null=True, blank=True)
    d = models.TextField(null=True, blank=True)
    e = models.TextField(null=True, blank=True)  # Optional field for answer E

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_main
