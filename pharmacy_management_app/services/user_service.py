from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from ..models.user import User

def create_user(data):
    try:
        user = User.objects.create(**data)
    except IntegrityError as e:
        error_message = str(e)
        raise IntegrityError(error_message)
    return user


def get_user(user_id: int):
    try:
        return User.objects.get(pk=user_id)
    except ObjectDoesNotExist as e:
        raise ObjectDoesNotExist("User not found.") from e

def update_user(user_id: int, data: dict):
 
    user = get_user(user_id)
    for field, value in data.items():
        setattr(user, field, value)
    try:
        user.save()
    except IntegrityError as e:
        error_message = str(e)
        raise IntegrityError(error_message)
    return user

def delete_user(user_id: int):
    user = get_user(user_id)
    user.delete()
    return user