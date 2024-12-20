from django.db import models


class List(models.Model):
    ...


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.text
