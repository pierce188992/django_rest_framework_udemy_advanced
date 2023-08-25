"""
Tests for the Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and client."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="testpass123",
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="testpass123", name="Test User"
        )

    def test_users_lists(self):
        """Test that users are listed on page."""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
        """
        在 test_users_lists 測試方法中，它首先通過 reverse 函數獲得 Django admin 中用戶列表的 URL。
        然後，它使用 self.client.get(url) 模擬向該 URL 發送 GET 請求，並將結果存儲在 res 中。
        最後，它使用 assertContains 方法檢查響應 res 中是否包含 self.user 的名稱和電子郵件。
        因此，這個測試確保在 Django admin 的用戶列表頁面中，
        可以看到先前在 setUp 方法中創建的普通用戶 self.user 的名稱和電子郵件。
        """

    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
