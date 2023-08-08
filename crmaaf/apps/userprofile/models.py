from django.db import models
from django.contrib.auth.models import User
 
 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_position = models.CharField(max_length = 120, help_text = 'Должность', verbose_name = 'Должность')

    user_accept = models.CharField(max_length = 120, help_text = 'Подпись согласования', verbose_name = 'Согласования', default = 'Исполнено')
    user_disaccept = models.CharField(max_length = 120, help_text = 'Подпись отказа', verbose_name = 'Отказ', default = 'Отказано')
    user_in_working = models.CharField(max_length = 120, help_text = 'Подпись в процессе', verbose_name = 'Процесс', default = 'В работе')

    def __unicode__(self):
        return f'{self.user.first_name} {self.user.last_name}'
 
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

User.__str__ = lambda user: user.get_full_name() or user.get_username() 