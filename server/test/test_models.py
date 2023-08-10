from django.test import TestCase
from apps.post.models import Post, Path, Step, Category, CategoryTable, Tag, TagTable, BookMarkTable, LikeTable
from apps.user.models import User
from apps.comment.models import PostComment, StepComment


class YourAppModelsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword', intro='Test intro')
        self.post = Post.objects.create(
            user=self.user, title='Test Post', desc='Test description')

        # Create some test categories and tags
        self.category1 = Category.objects.create(name='Category1')
        self.category2 = Category.objects.create(name='Category2')
        self.tag1 = Tag.objects.create(name='Tag1')
        self.tag2 = Tag.objects.create(name='Tag2')

        # Create a test post

        # Add categories and tags to the post using the intermediate models
        CategoryTable.objects.create(post=self.post, category=self.category1)
        CategoryTable.objects.create(post=self.post, category=self.category2)
        TagTable.objects.create(post=self.post, tag=self.tag1)
        TagTable.objects.create(post=self.post, tag=self.tag2)

        # Create a test path for the post
        self.path = Path.objects.create(
            post=self.post, title='Test Path', order=1)

        # Create a test step for the path
        self.step = Step.objects.create(
            path=self.path, title='Test Step', desc='Test step description', order=1)

        # Create a test bookmark
        self.bookmark = BookMarkTable.objects.create(
            post=self.post, user=self.user)

        # Create a test like
        self.like = LikeTable.objects.create(post=self.post, user=self.user)

    def test_post_model(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.user, self.user)

    def test_path_model(self):
        self.assertEqual(self.path.title, 'Test Path')
        self.assertEqual(self.path.post, self.post)

    def test_step_model(self):
        self.assertEqual(self.step.title, 'Test Step')
        self.assertEqual(self.step.path, self.path)

    def test_category_model(self):
        self.assertEqual(self.category1.name, 'Category1')

    def test_tag_model(self):
        self.assertEqual(self.tag2.name, 'Tag2')

    def test_category_table_model(self):
        self.assertEqual(self.post.category_table.count(), 2)

    def test_tag_table_model(self):
        self.assertEqual(self.post.tag_table.count(), 2)

    def test_user_model(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.intro, 'Test intro')
        self.assertEqual(self.user.membership, 'bronze')

    def test_bookmark_model(self):
        self.assertEqual(self.bookmark.post, self.post)
        self.assertEqual(self.bookmark.user, self.user)

    def test_like_model(self):
        self.assertEqual(self.like.post, self.post)
        self.assertEqual(self.like.user, self.user)


class PostCommentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.post = Post.objects.create(
            user=self.user, title='Test Post', desc='Test Description')
        self.post_comment = PostComment.objects.create(
            post=self.post, writer=self.user, text='Test Comment')

    def test_post_comment_model(self):
        self.assertEqual(self.post_comment.post, self.post)
        self.assertEqual(self.post_comment.writer, self.user)
        self.assertEqual(self.post_comment.text, 'Test Comment')
        self.assertIsNone(self.post_comment.parentComment)


class StepCommentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.post = Post.objects.create(
            user=self.user, title='Test Post', desc='Test Description')
        self.path = Path.objects.create(
            post=self.post, title='Test Path', order=1)
        self.step = Step.objects.create(
            path=self.path, title='Test Step', desc='Test Step Description', order=1)
        self.step_comment = StepComment.objects.create(
            step=self.step, writer=self.user, text='Test Comment')

    def test_step_comment_model(self):
        self.assertEqual(self.step_comment.step, self.step)
        self.assertEqual(self.step_comment.writer, self.user)
        self.assertEqual(self.step_comment.text, 'Test Comment')
        self.assertIsNone(self.step_comment.parentComment)
