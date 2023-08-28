"""
Core views for app.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health_check(request):
    """Returns successful response."""
    return Response({"healthy": True})


"""
@api_view(["GET"])：這是一個裝飾器，用於指定此視圖只接受GET請求。
任何其他類型的請求（例如POST或PUT）都會返回405 Method Not Allowed響應。

def health_check(request):
這是視圖的定義。它接受一個參數 request，該參數包含請求的所有細節。

return Response({"healthy": True})：
這將返回一個包含 { "healthy": True } 的響應，並使用預設的HTTP狀態碼200 OK。
{在這裡，它是一個Python字典，其中包含一個鍵（"healthy"）和一個值（True）。

當 Response 將其轉換為HTTP響應時，這個字典將被序列化為JSON格式。

#example

@api_view(['GET'])
def my_view(request):
    data = {"message": "Hello, World!"}
    headers = {"Content-Type": "application/json"}
    return Response(data, headers=headers)

DRF 的 Response 物件返回 JSON 數據時，Content-Type 標頭預設已經是 application/json。

"""
