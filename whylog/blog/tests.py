import coverage
cov = coverage.Coverage()
cov.start()

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Blog, Category, Comment, Like
from .views import like_comment_toggle, like_blog_toggle, search
from .forms import BlogForm, CommentForm

class BoardViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_board_view(self):
        response = self.client.get(reverse('board'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'board.html')

    def test_write_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('write'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'write.html')

    def test_write_view_with_blog_id(self):
        self.client.login(username='testuser', password='testpassword')
        category = Category.objects.create(category='Test Category')
        blog = Blog.objects.create(
            title='Test Blog',
            content='Test Content',
            user=self.user,
            in_private=False,
            temporary=False,
            count=0,
            category=category,
        )
        response = self.client.get(reverse('write', args=[blog.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'write.html')

class CommentViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        category = Category.objects.create(category='Test Category')
        self.blog = Blog.objects.create(
            title='Test Blog',
            content='Test Content',
            user=self.user,
            in_private=False,
            temporary=False,
            count=0,
            category=category,
        )

    def test_comment_write_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('comment_write', args=[self.blog.id]), {'comment': 'Test Comment'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)

    def test_comment_delete_view(self):
        comment = Comment.objects.create(
            user=self.user,
            blog=self.blog,
            comment='Test Comment',
        )

        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('comment_delete', args=[comment.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)

    def test_comment_edit_view(self):
        comment = Comment.objects.create(
            user=self.user,
            blog=self.blog,
            comment='Test Comment',
        )

        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('comment_edit', args=[comment.id]), {'edited_comment': 'Updated Comment'})
        self.assertEqual(response.status_code, 200)
        comment.refresh_from_db()
        self.assertEqual(comment.comment, 'Updated Comment')

class LikeCommentToggleTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.category = Category.objects.create(category='Test Category')
        self.blog = Blog.objects.create(
            title='Test Blog',
            content='Test Content',
            user=self.user,
            in_private=False,
            temporary=False,
            count=0,
            category=self.category,
        )
        self.comment = Comment.objects.create(
            user=self.user,
            blog=self.blog,
            comment='Test Comment',
        )

    def test_like_comment_toggle(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('like_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.count(), 1)

        response = self.client.post(reverse('like_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.count(), 0)

class LikeBlogToggleTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.category = Category.objects.create(category='Test Category')
        self.blog = Blog.objects.create(
            title='Test Blog',
            content='Test Content',
            user=self.user,
            in_private=False,
            temporary=False,
            count=0,
            category=self.category,
        )

    def test_like_blog_toggle(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('like_blog', args=[self.blog.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.count(), 1)

        response = self.client.post(reverse('like_blog', args=[self.blog.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.count(), 0)

class SearchTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.category = Category.objects.create(category='Test Category')
        self.blog = Blog.objects.create(
            title='Test Blog',
            content='Test Content',
            user=self.user,
            in_private=False,
            temporary=False,
            count=0,
            category=self.category,
        )

    def test_search(self):
        response = self.client.get(reverse('search') + '?searchBox-input=Test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Blog')

        Comment.objects.create(
            user=self.user,
            blog=self.blog,
            comment='Test Comment',
        )
        response = self.client.get(reverse('search') + '?searchBox-input=Comment')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Blog')

class WriteViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.category = Category.objects.create(category='Test Category')

        self.blog_data = {
            'title': 'Test Blog Title',
            'content': 'Test Blog Content',
            'topic': self.category.id,
        }

    def test_write_new_blog(self):
        self.blog_data['topic'] = self.category.id
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('write'), data=self.blog_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Blog.objects.count(), 1)
        new_blog = Blog.objects.first()
        self.assertEqual(new_blog.title, self.blog_data['title'])
        self.assertEqual(new_blog.content, self.blog_data['content'])
        self.assertEqual(new_blog.category.id, self.blog_data['topic'])
        self.assertEqual(new_blog.user, self.user)


    def test_edit_blog(self):
        self.client.login(username='testuser', password='testpassword')
        category = Category.objects.create(category='Test Category')
        blog = Blog.objects.create(
            title='Test Blog',
            content='Test Content',
            user=self.user,
            in_private=False,
            temporary=False,
            count=0,
            category=category,
        )
        edited_data = {
            'title': 'Edited Title',
            'content': 'Edited Content',
            'topic': self.category.id,
        }
        response = self.client.post(reverse('write', args=[blog.id]), data=edited_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('board_detail', args=[blog.id])))
        edited_blog = Blog.objects.get(id=blog.id)
        self.assertEqual(edited_blog.title, edited_data['title'])
        self.assertEqual(edited_blog.content, edited_data['content'])
        self.assertEqual(edited_blog.category.id, edited_data['topic'])

    def test_delete_blog(self):
        self.client.login(username='testuser', password='testpassword')
        category = Category.objects.create(category='Test Category')
        blog = Blog.objects.create(
            title='To be deleted',
            content='This blog will be deleted',
            user=self.user,
            category=category,
            in_private=False,
            temporary=False,
            count=0,
        )

        response = self.client.post(reverse('board_delete', args=[blog.id]), {'delete-button': 'true'})

        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Blog.objects.filter(id=blog.id).count(), 0) 

class CommentWriteTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(category='Test Category')
        self.blog = Blog.objects.create(
            title='Test Blog',
            content='Test Content',
            user=self.user,
            in_private=False,
            temporary=False,
            count=0,
            category=self.category,
        )
        self.url = reverse('comment_write', args=[self.blog.id])

    def test_comment_write_post(self):
        self.client.login(username='testuser', password='testpassword')
        form_data = {'comment': 'Test comment'}
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302)

    def test_comment_write_redirect(self):
        self.client.login(username='testuser', password='testpassword')
        form_data = {'comment': 'Test comment'}
        response = self.client.post(self.url, data=form_data)
        self.assertRedirects(response, reverse('board_detail', args=[self.blog.id]))

class CommentDeleteTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.comment_user = User.objects.create_user(username='commentuser', password='testpassword')
        self.category = Category.objects.create(category='Test Category')
        self.blog = Blog.objects.create(
            title='Test Blog',
            content='Test Content',
            user=self.user,
            in_private=False,
            temporary=False,
            count=0,
            category=self.category,
        )
        self.comment = Comment.objects.create(comment='Test comment', user=self.comment_user, blog=self.blog)
        self.url = reverse('comment_delete', args=[self.comment.id])

    def test_comment_delete_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_comment_delete_redirect(self):
        self.client.login(username='commentuser', password='testpassword')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

class CommentEditTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.comment_user = User.objects.create_user(username='commentuser', password='testpassword')
        self.category = Category.objects.create(category='Test Category')
        self.blog = Blog.objects.create(
            title='Test Blog',
            content='Test Content',
            user=self.user,
            in_private=False,
            temporary=False,
            count=0,
            category=self.category,
        )
        self.comment = Comment.objects.create(comment='Test comment', user=self.comment_user, blog=self.blog)
        self.url = reverse('comment_edit', args=[self.comment.id])

    def test_comment_edit_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_comment_edit_post(self):
        self.client.login(username='commentuser', password='testpassword')
        form_data = {'edited_comment': 'Edited comment'}
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        edited_comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(edited_comment.comment, 'Edited comment')

cov.stop()
cov.save()
cov.html_report()