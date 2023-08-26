"""
Views for the recipe APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""

    serializer_class = serializers.RecipeDetailSerializer
    """
    序列化器首先將複雜的數據類型（例如 Django 的查詢集或模型實例）轉換為 Python 的原生數據結構（例如字典、列表、字符串、整數等）。
    然後，這些原生數據結構可以進一步被轉換為不同的內容格式，如 JSON、XML 等。

    DRF 默認使用 JSON 格式，
    """
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == "list":
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)

    """
    perform_create 只在 POST 請求（對應於創建操作）時被觸發。但 ModelViewSet 提供了其他方法，
    這些方法允許您在執行 CRUD 操作之前或之後插入自定義邏輯, 可以在其他請求中被覆寫和觸發：

    POST (Create): perform_create(self, serializer)
    在這個方法中，一個新的實例被創建和保存。

    PUT (Update): perform_update(self, serializer)
    此方法在一個已存在的實例被完全更新時被觸發。

    PATCH (Partial Update): perform_update(self, serializer)
    這也會觸發 perform_update，但與 PUT 不同的是，它僅更新提供的字段，而不是整個實例。

    DELETE (Destroy): perform_destroy(self, instance)
    在此方法中，給定的實例被刪除。
    """
