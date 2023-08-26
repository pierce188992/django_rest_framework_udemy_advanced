# from django.shortcuts import render
# # Create your views here.

"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer

"""
泛型視圖類 (generic view classes)

以下是一些 generics 模塊中提供的常見視圖類：

ListCreateAPIView: 用於讀取資源列表和創建新資源的視圖。
RetrieveUpdateDestroyAPIView: 
用於讀取、更新或刪除單一資源的視圖。
ListAPIView: 用於僅讀取資源列表的視圖。
CreateAPIView: 用於僅創建新資源的視圖。
RetrieveAPIView: 用於僅讀取單一資源的視圖。
UpdateAPIView: 用於僅更新單一資源的視圖。
DestroyAPIView: 用於僅刪除單一資源的視圖。
每個視圖都預期有一個指定的序列化器 (serializer) 
用來控制如何將模型資料轉換成 JSON，
以及如何將 JSON 資料驗證和保存到模型中。

混合基礎類 (mixin base classes) 是用來提供某些常見操作（如創建、檢索、更新、刪除）的方法。
CreateModelMixin: 提供了創建模型實例的方法。
ListModelMixin: 提供了列出查詢集 (queryset) 的方法。
RetrieveModelMixin: 提供了檢索特定模型實例的方法。
UpdateModelMixin: 提供了更新模型實例的方法。
DestroyModelMixin: 提供了刪除模型實例的方法。
"""


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer
    """
    這是一個更專用的視圖，僅用於創建模型的新實例。
    它可能比 ModelViewSet 更靈活，可以更容易地自定義或接受多種 Content-Type。
    """


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    """
    TokenAuthentication 的一些基本信息：
    工作原理:

    當用戶首次登錄或註冊時，系統會為該用戶生成一個唯一的令牌。
    這個令牌隨後可以用於認證隨後的API請求。當用戶想要訪問受保護的API端點時，
    他們必須在請求的 Authorization 頭中提供這個令牌。

    在API請求中，令牌通常以以下格式提供：Authorization: Token <token_key>，其中 <token_key> 是實際的令牌。
    安全性:

    TokenAuthentication 是相對簡單的認證方法，適用於許多用途，但可能不適合超高安全性的應用。
    如果令牌泄露，任何人都可以使用該令牌訪問API。因此，令牌應該像密碼一樣保護。
    生命周期:

    令牌可以有一個固定的生命周期（例如24小時），之後它們會過期，或者可以無限期地存在，
    直到用戶登出或明確地撤銷它為止。與其他認證方法的比較:

    相對於其他認證方法（如OAuth2或JWT），TokenAuthentication 較為簡單。
    OAuth2和JWT通常提供更多的功能，如令牌刷新、範圍設定和跨系統認證。
    
    使用 TokenAuthentication，您只需要在 DRF 設置中指定它作為認證類，
    並在您的模型和視圖中進行相應的設置，即可為用戶生成和管理令牌。
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
