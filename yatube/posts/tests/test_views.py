# deals/tests/test_views.py
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group

User = get_user_model()


class PostURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author_post = User.objects.create_user(username='author_post')
        cls.simple_user = User.objects.create_user(username='simple_user')
        cls.group = Group.objects.create(
            title='Тестовая гурппа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.author_post,
            text='Текстовый пост',
    )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTest.simple_user)
        self.author_post = Client()
        self.author_post.force_login(PostURLTest.author_post)

    # Проверяем используемые шаблоны
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse('posts:group_list'),
            'posts/profile.html': reverse('posts:profile'),
            'posts/post_detail.html': reverse('posts:post_detail'),
            'posts/create_post.html': reverse('posts:post_edit'),
            'posts/create_post.html': reverse('posts:create_post'),
            # 'deals/task_detail.html': (
            #     reverse('deals:task_detail', kwargs={'slug': 'test-slug'})
            # ),
        }
        # Проверяем, что при обращении к name вызывается соответствующий HTML-шаблон
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)


    # def test_urls_uses_correct_template_authorized(self):
    #     url_templates_names = {
    #         '/': 'posts/index.html',
    #         f'/group/{self.group.slug}/': 'posts/group_list.html',
    #         f'/profile/{self.post.author}/': 'posts/profile.html',
    #         '/create/': 'posts/create_post.html',
    #         f'/posts/{PostURLTest.post.id}/': 'posts/post_detail.html',
    #         # f'/posts/{PostURLTest.post.id}/edit/': 'posts/post_detail.html'
    #     }
    #
    #     for address, template in url_templates_names.items():
    #         with self.subTest(address=address):
    #             response = self.authorized_client.get(address)
    #             self.assertTemplateUsed(response, template)