"""
Views for the recipe APIs
"""
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""

    serializer_class = serializers.RecipeDetailSerializer
    """
    序列化器首先將複雜的數據類型（例如 Django 的查詢集或模型實例）轉換為 Python 的原生數據結構（例如字典、列表、字符串、整數等）。
    然後，然後這些原生數據結構再進一步被轉換為不同的內容格式，如 JSON、XML 等。DRF 默認使用 JSON 格式
    1.ModelViewSet，很多序列化和反序列化的工作都會自動完成。
    2.ModelViewSet（或大多數其他內置的 DRF 視圖）時，它的預設行為是期望請求主體中的數據為 JSON 格式。這是因為：

    易於使用：JSON 是一種常見的數據格式，它易於使用且在多個平台和語言中都有支持。
    標準化：使用 JSON 作為標準格式可以確保 API 的一致性，無論調用者在哪裡或使用什麼技術。
    內置支持：DRF 內置了 JSONParser，這是一個專門用於解析 JSON 請求主體的解析器。

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
    create 方法處理 POST 請求的邏輯，它是用於創建資料的主要方法。
    這個方法首先會初始化序列化器，檢查序列化器是否有效，然後保存資料。
    它還負責返回適當的響應，如成功的 201 Created 或錯誤的 400 Bad Request。
    perform_create:

    perform_create 是 create 方法中用來實際保存模型實例的部分。
    它的主要目的是提供一個可以輕鬆覆蓋的方法，以自定義保存行為，而無需重寫整個 create 方法。
    例如，如果你想在保存之前設置某些屬性或觸發某些操作，你可以覆蓋 perform_create。

    #其他方法
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


class TagViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Manage tags in the database."""

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-name")


"""
mixins.ListModelMixin:
這個 mixin 提供了將查詢集列出為一個列表的功能。
當您的視圖集接收到一個 GET 請求時，如果視圖集繼承了 ListModelMixin，
那麼這個 mixin 中的 list 方法會被調用，返回查詢集的列表。

viewsets.GenericViewSet:
這是 DRF 的一個基本視圖集。它提供了視圖集的核心功能，
例如 get_object、get_serializer 等方法，但不包含任何特定的動作，
如 create、update、delete 等。這意味著，單獨使用 GenericViewSet 不會提供 CRUD 操作。
但是，當它與其他 mixins（如 ListModelMixin、CreateModelMixin、UpdateModelMixin 等）組合時，
它可以用來創建具有特定功能的視圖集。

1.Mixins:
目的: Mixins 的主要目的是提供單一、特定的功能。例如，提供對象創建、檢索、更新或刪除的功能。
組合性: 通常，多個 mixins 可以被組合在一起，以在單一的視圖中提供多個功能。
常見的 Mixins:
ListModelMixin: 提供列表視圖功能。
CreateModelMixin: 提供對象創建功能。
RetrieveModelMixin: 提供單一對象的檢索功能。
UpdateModelMixin: 提供對象更新功能。
DestroyModelMixin: 提供對象刪除功能。
使用方式: Mixins 被設計為與其他視圖基礎類組合使用，如 GenericAPIView。

2.Viewsets:
目的: Viewsets 是用來表示一組完整的 CRUD (Create, Retrieve, Update, Delete) 操作的。它們通常與模型和序列化器一起使用。
簡化性: Viewsets 的目的是簡化常見的模型視圖模式。
常見的 Viewsets:
ModelViewSet: 它包含了 CRUD 操作的全部方法。實際上，ModelViewSet 繼承了多個 mixins，給出了完整的 CRUD 功能。
ReadOnlyModelViewSet: 只提供列表和檢索操作。
使用方式: Viewsets 被設計為與 DRF 的 routers 一起使用，以自動生成 URL 模式。

3.結論:
mixins 是較小的、功能單一的組件，通常與其他視圖基礎類組合使用，以提供所需的功能。
viewsets 提供一組完整的 CRUD 操作，通常與 DRF 的 routers 一起使用，以自動生成 URL 模式。
"""


# 發送請求的方式
"""
import requests

url = "http://127.0.0.1:8000/api/recipe/recipes/"
headers = {
    "accept": "application/json",
    "Authorization": "Token 4159325a68f6b0c3548de9ef8ba9007d96b57e26",
    "X-CSRFToken": "j0NuS2tGKvRF2yOaGmGC028ZyulnmOehBLrzQEZAQTSYUdDlLUBZ8nsBOxL1KYKM", # get方法不需要
}

response = requests.get(url, headers=headers)

# 處理響應
if response.status_code == 200:
    print(response.json())  # 如果返回的是 JSON 數據
else:
    print("Error:", response.status_code)
"""
