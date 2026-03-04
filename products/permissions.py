from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    # Редактирование для владельца, чтение доступно всем
    def has_object_permission(self, request, view, obj):
        # Разрешаем чтение для безопасных методов
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        # Разрешаем редактирование только владельцу
        return obj.owner == request.user