from django.contrib.auth.models import User


__all__ = ['add_controlling_pack_to_order', 'add_user_controlling_by_group_to_order']

def add_controlling_pack_to_order(self, group_name):
    """ Auto add users to m2m in controlling.
    """
    self.controlling_pack = User.objects.filter(groups__name=group_name).all()
    if self.controlling_pack:
        for i in self.controlling_pack:
            self.controlling.add(i)
    pass

def add_users_controlling_by_group_to_order(self):
    """ The function add users by group to the order.
    """

    self.controlling.clear()

    add_controlling_pack_to_order(self, 'BOSS')# Add all users with group is BOSS to the order.

    if self.type_order == 'kp': # Then we can will added KPK or other users to the order.
        add_controlling_pack_to_order(self, 'KPK')
    elif self.type_order == 'kz': 
        add_controlling_pack_to_order(self, 'KZ')
    else:
        add_controlling_pack_to_order(self, 'ML') 

    return self