from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from ..models.user import User
from django.db.models import Q

def create_user(data: dict) :
    try:
        user = User.objects.create(**data)
    except IntegrityError as e:
        error_message = str(e)
        raise IntegrityError(error_message)
    return user

def get_user(user_id: int) :
    try:
        return User.objects.get(pk=user_id)
    except ObjectDoesNotExist as e:
        raise ObjectDoesNotExist("User not found.") from e

def get_all_users(name_contains: str = "", **kwargs) -> list[User]:
    try:
        query = Q(**kwargs)
        if name_contains:
            query &= Q(name__icontains=name_contains)
        return User.objects.filter(query)
    except ObjectDoesNotExist as e:
        raise ObjectDoesNotExist("User not found.") from e

def update_user(user_id: int, data: dict) :
    user = get_user(user_id)
    for field, value in data.items():
        setattr(user, field, value)
    try:
        user.save()
    except IntegrityError as e:
        error_message = str(e)
        raise IntegrityError(error_message)
    return user

def delete_user(user_id: int) :
    user = get_user(user_id)
    user.delete()
    return user