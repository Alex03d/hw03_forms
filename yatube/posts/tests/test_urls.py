from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Post, Group, User

User = get_user_model()


class PostURLTest(TestCase):
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

    def test_post_id_edit_url_exists_at_desired_location_for_client(self):
        response = self.authorized_client.get(f'/posts/{PostURLTest.post.id}/edit/'/, follow=True)
        self.assertRedirect(response, (f'/posts/{PostURLTest.post.id}/'))

    def test_post_id_edit_url_exists_at_desired_location_for_author(self):
        response = self.author_post.get(f'/posts/{PostURLTest.post.id}/edit/'/, follow=True)
        self.assertRedirect(response, (f'/posts/{PostURLTest.post.id}//edit/'))

    def test_post_create_url_exists_at_desired_location_for_authorized(self):
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_post_create_url_exists_at_desired_location_for_unauthorized(self):
        response = self.authorized_client.get(f'/create/')
        self.assertRedirect(response, ('/'))

    def test_unexisting_url_exists_at_desired_location(self):
        response = self.guest_client.get('/unexising_page/')
        self.assertEqual(response.status_code, 200)

#проверка шаблонов

    def test_home_url_exists_at_desired_location(self):
        response = self.guest_client.get('/')
        self.assertTemplateUsed(response, 'posts/index.html')

    def test_group_slug_url_exists_at_desired_location(self):
        response = self.guest_client.get('/group/<slug>/')
        self.assertTemplateUsed(response, 'posts/group_list.html')

    def test_profile_url_exists_at_desired_location(self):
        response = self.guest_client.get('/profile/<username>/')
        self.assertTemplateUsed(response, 'profile.html')

    def test_post_id_url_exists_at_desired_location(self):
        response = self.guest_client.get('/posts/<post_id>/')
        self.assertTemplateUsed(response, 'posts/detail.html')

    def test_post_id_edit_url_exists_at_desired_location_for_client(self):
        response = self.authorized_client.get(f'/posts/{PostURLTest.post.id}/edit/'/, follow=True)
        self.assertTemplateUsed(response, 'create/post.html')

    def test_post_id_edit_url_exists_at_desired_location_for_author(self):
        response = self.author_post.get(f'/posts/{PostURLTest.post.id}/edit/'/, follow=True)
        self.assertTemplateUsed(response, 'create/post.html')

    def test_post_create_url_exists_at_desired_location_for_authorized(self):
        response = self.authorized_client.get('/create/')
        self.assertTemplateUsed(response, 'create/post.html')

    def test_post_create_url_exists_at_desired_location_for_unauthorized(self):
        response = self.authorized_client.get(f'/create/')
        self.assertTemplateUsed(response, 'posts/index.html')

    def test_unexisting_url_exists_at_desired_location(self):
        response = self.guest_client.get('/unexising_page/')
        self.assertTemplateUsed(response, 'posts/index.html')

# posts/tests/test_urls.py
# from django.test import TestCase, Client
#
#
# class StaticURLTests(TestCase):
#     def setUp(self):
#         self.guest_client = Client()
#
#     def test_about_url_exists_at_desired_location(self):
#         response = self.guest_client.get('/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_about_url_uses_correct_template(self):
#         response = self.guest_client.get('/')
#         self.assertTemplateUsed(response, 'posts/index.html')