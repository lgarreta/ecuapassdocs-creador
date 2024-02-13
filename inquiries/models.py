from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class AdministrativeRequests(models.Model):
    subject = models.CharField(max_length=100, help_text="Enter the Subject of your Request")
    body = models.TextField(max_length=2000, help_text="Enter Description of your Administrative Request Here")
    request_date = models.DateTimeField(auto_now_add=True, help_text="Date and time when the request was made")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_admin_requests', help_text="Sending to...")
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_admin_requests', help_text="Sent By...", default=None)
    reply =  models.TextField(max_length=2000, help_text="Enter a response to the Administrative Request Above", default="No Response Yet...")


    def __str__(self):
        return f"{self.subject}"
    
    def save(self, *args, **kwargs):
        if not self.sender_id:
            self.sender = self._request.user if self._request else None
        super(AdministrativeRequests, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Administrative Requests"

class AcademicRequests(models.Model):
    subject = models.CharField(max_length=100, help_text="Enter the Subject of your Academic Request")
    body = models.TextField(max_length=2000, help_text="Enter Description of your Academic Request Here")
    request_date = models.DateTimeField(auto_now_add=True, help_text="Date and time when the request was made")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_academic_requests', help_text="Sending to...")
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_academic_requests', help_text="Sent By...", default=None)
    reply =  models.TextField(max_length=2000, help_text="Enter a response to the Academic Request Above", default="No Response Yet...")


    def __str__(self):
        return f"{self.subject}"
    
    def save(self, *args, **kwargs):
        if not self.sender_id:
            self.sender = self._request.user if self._request else None
        super(AcademicRequests, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Academic Requests"



