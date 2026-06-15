from django.db import models


class ContactMessage(models.Model):
    """A message submitted through the public contact form.

    Stored server-side so staff can follow up. Kept deliberately small;
    extend with status/assignment fields as the site grows.
    """

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    subject = models.CharField(max_length=160, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "contact message"
        verbose_name_plural = "contact messages"

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"
