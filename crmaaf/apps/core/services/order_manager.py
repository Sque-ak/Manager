from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from crmaaf.apps.core.models import TimeExecutionUser
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core import mail
from smtplib import SMTPException


import datetime

__all__ = ["move_users_to_disallow_group", "send_email_new_order", "move_users_to_allow_group", "check_time_execution_have"]

def send_email_new_order(url_html, subject, users, context) -> None:
    """ Send email about new order to the group users.
    """
    self_html_message = render_to_string(url_html, {'context': context})
    self_plain_message = strip_tags(self_html_message)


    for i in users:
        try:
            mail.send_mass_mail(datatuple = [(subject, self_plain_message, settings.DEFAULT_FROM_EMAIL, [i.email])], fail_silently = False)
        except SMTPException as e:
            print('ERROR: SMTP Exception, maybe you sented a lot of emails and got from mail server ban. Try later.')
            print('Exception: ' + e)
            print('Data: ' + [(subject, self_plain_message, settings.DEFAULT_FROM_EMAIL, [i.email])]) #Need some logger in futer. 
    pass

def move_users_to_disallow_group(self, in_order_obj) -> None:
    """ This is def will be moved all users with group controlling,
    to the group controlling_disallow.
    """
    for i in in_order_obj.controlling.all():
        if in_order_obj.status != "p" and self.user == i: #if the order isn't progressing then could change the status;
            in_order_obj.controlling_disallow.add(self.user)
            in_order_obj.controlling.remove(self.user)
            in_order_obj.status = "d"
            
            if TimeExecutionUser.objects.filter(order_by = in_order_obj, user = self.user):
                try:
                    self__get_time_execution = TimeExecutionUser.objects.get(order_by = in_order_obj, user = self.user)
                    self__get_time_execution.time = datetime.datetime.now()
                    self__get_time_execution.save()
                except (ObjectDoesNotExist, MultipleObjectsReturned):
                    print("ERROR: Auto created user, but the shit before it wasn't worked. ;-; \f \
                           or the object return multi time execution. ") #Need some logger in futer. 
            else:
                self__date_time = TimeExecutionUser(order_by = in_order_obj, time = datetime.datetime.now(), time_got_order = datetime.datetime.now(), user = self.user, got_order = True)
                self__date_time.save()
                print("ERROR: Auto created user, but the shit before it wasn't worked. ;-;") #Need some logger in futer. 
                
            in_order_obj.save()
    pass

def check_time_execution_have(self, in_order_obj) -> None:
    """ Check order. If user will seen the order then got order = true.
    """
    for i in in_order_obj.controlling.all(): 
        if self.user == i:
            if TimeExecutionUser.objects.filter(order_by = in_order_obj, user = self.user):
                break
            else:
                self__date_time = TimeExecutionUser(order_by = in_order_obj, time_got_order = datetime.datetime.now(), user = self.user, got_order = True)
                self__date_time.save()
    pass

def move_users_to_allow_group(self, in_order_obj, user_pack, self_user_name) -> None:
    """ The opposite the move_users_to_disallow_group,
    will moved to the group controlling_allow. 
    """
    for i in in_order_obj.controlling.all():
        if in_order_obj.status != "p" and self_user_name == i: #if the order isn't progressing then could change the status;

            in_order_obj.controlling_allow.add(self_user_name)
            in_order_obj.controlling.remove(self_user_name)

            if TimeExecutionUser.objects.filter(order_by = in_order_obj, user = self_user_name):
                try:
                    self__get_time_execution = TimeExecutionUser.objects.get(order_by = in_order_obj, user = self_user_name)
                    self__get_time_execution.time = datetime.datetime.now()
                    self__get_time_execution.save()
                except (ObjectDoesNotExist, MultipleObjectsReturned):
                    print("ERROR: Auto created user, but the shit before it wasn't worked. ;-; \f \
                           or the object return multi time execution. ") #Need some logger in futer. 
            else:
                self__date_time = TimeExecutionUser(order_by = in_order_obj, time = datetime.datetime.now(), time_got_order = datetime.datetime.now(), user = self_user_name, got_order = True)
                self__date_time.save()
                print("ERROR: Auto created user, but the shit before it was worked. ;-; \f \
                       may the user didn't seed the order.") #Need some logger in futer.

            in_order_obj.save()
                
            if not user_pack and in_order_obj.controlling.all():
                in_order_obj.status = "j"
                if not in_order_obj.date_allow:
                    in_order_obj.date_allow = datetime.datetime.now()
                in_order_obj.save()

                send_email_new_order('core/message/to_work_order.html', f'Поступило распоряжение "{ in_order_obj.title }" на исполнениия.',
                                     in_order_obj.controlling.all(), in_order_obj)

            if not in_order_obj.controlling_disallow.all() and not in_order_obj.controlling.all():
                in_order_obj.status = "a"
                in_order_obj.date_finish = datetime.datetime.now()
                in_order_obj.save()

                self__users_pack = [in_order_obj.created_by]
                send_email_new_order('core/message/order_done.html', f'Распоряжение "{ in_order_obj.title }" было исполненно.',
                                     self__users_pack, in_order_obj)
    pass