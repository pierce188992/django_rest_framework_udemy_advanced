"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
router.register("recipes", views.RecipeViewSet)
router.register("tags", views.TagViewSet)

"""
DefaultRouter 會為每個操作自動生成相應的 URL，並與視圖集中的方法相匹配。例如，對於 RecipeViewSet：

GET /recipes/ 會觸發視圖集中的 list 方法，列出所有食譜。
POST /recipes/ 會觸發 create 方法，建立新的食譜。
GET /recipes/<id>/ 會觸發 retrieve 方法，獲取特定食譜的詳細信息。
PUT /recipes/<id>/ 和 PATCH /recipes/<id>/ 會觸發 update 方法。
DELETE /recipes/<id>/ 會觸發 destroy 方法，刪除特定食譜。
"""

app_name = "recipe"

urlpatterns = [
    path("", include(router.urls)),
]
