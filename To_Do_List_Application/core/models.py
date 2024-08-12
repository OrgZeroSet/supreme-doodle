from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=350)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created'] 

    def __str__(self):
        return self.title