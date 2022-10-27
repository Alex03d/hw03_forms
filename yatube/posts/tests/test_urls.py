from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Post, Group, User

User = get_user_model()


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Post.objects.create(
            text='Тестовый текст',
            pub_date='Дата публикации',
            author='Автор',
            group='Группа'
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_home_url_exists_at_desired_location(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_slug_url_exists_at_desired_location(self):
        response = self.guest_client.get('/group/<slug>/')
        self.assertEqual(response.status_code, 200)

    def test_profile_url_exists_at_desired_location(self):
        response = self.guest_client.get('/profile/<username>/')
        self.assertEqual(response.status_code, 200)

    def test_post_id_url_exists_at_desired_location(self):
        response = self.guest_client.get('/posts/<post_id>/')
        self.assertEqual(response.status_code, 200)

    def test_post_id_edit_url_exists_at_desired_location(self):
        response = self.authorized_client.get('/posts/<post_id>/')
        self.assertEqual(response.status_code, 200)

    def test_post_create_url_exists_at_desired_location(self):
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_unexisting_url_exists_at_desired_location(self):
        response = self.guest_client.get('/unexising_page/')
        self.assertEqual(response.status_code, 200)

    # Проверяем доступность страниц для авторизованного пользователя
    def test_task_list_url_exists_at_desired_location(self):
        """Страница /task/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/task/')
        self.assertEqual(response.status_code, 200)

    def test_task_detail_url_exists_at_desired_location_authorized(self):
        """Страница /task/test-slug/ доступна авторизованному
        пользователю."""
        response = self.authorized_client.get('/task/test-slug/')
        self.assertEqual(response.status_code, 200)

    # Проверяем редиректы для неавторизованного пользователя
    def test_task_list_url_redirect_anonymous(self):
        """Страница /task/ перенаправляет анонимного пользователя."""
        response = self.guest_client.get('/task/')
        self.assertEqual(response.status_code, 302)

    def test_task_detail_url_redirect_anonymous(self):
        """Страница /task/test-slug/ перенаправляет анонимного
        пользователя.
        """
        response = self.guest_client.get('/task/test-slug/')
        self.assertEqual(response.status_code, 302)


# posts/tests/test_urls.py
from django.test import TestCase, Client


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_url_exists_at_desired_location(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about_url_uses_correct_template(self):
        response = self.guest_client.get('/')
        self.assertTemplateUsed(response, 'posts/index.html')