from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.db.models.signals import post_save
# Create your models here.

STATUS = (
    (0, "Draft"),
    (1, "Published")
)


class Category(models.Model):  # Category for the Article
    title = models.CharField(max_length=200)  # Title of the Category
    created_on = models.DateTimeField(auto_now_add=True)  # Date of creation

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:by-category', kwargs={'title': self.title})


class BlogPost(models.Model):
    # Title of the Article
    title = models.CharField(max_length=200, unique=True)
    # Unique identifier for the article
    slug = models.SlugField(max_length=200, blank=True, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')  # Author of the Article
    # Short Description of the article
    description = models.CharField(max_length=500)
    # Content of the article, you need to install CKEditor
    content = RichTextUploadingField(config_name='awesome_ckeditor')
    tags = TaggableManager()  # Tags for a Particular Article, You need to install Taggit
    category = models.ForeignKey(
        'Category', related_name='category', on_delete=models.CASCADE)  # Category of the article
    keywords = models.CharField(max_length=250)  # Keywords to be used in SEO
    # Cover Image of the article
    cover = models.ImageField(upload_to='images/')
    created_on = models.DateTimeField(auto_now_add=True)  # Date of creation
    updated_on = models.DateTimeField(auto_now=True)  # Date of updation
    # Status of the Article either Draft or Published
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:blog-detail", kwargs={'slug': self.slug, 'date': str(self.created_on.date())})

    def get_add_comment_url(self):
        return reverse('blog:add-comment', kwargs={'blog_id': self.id})


class Comment(models.Model):
    user = models.ForeignKey(
        User,  on_delete=models.CASCADE,  related_name='blog_comments')
    comment = models.TextField(max_length=5000)
    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, null=True, related_name='comments')
    replies = models.ManyToManyField(
        'Comment', related_name='parent_comment', blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)  # Date of creation
    updated_on = models.DateTimeField(auto_now=True)  # Date of updation

    def get_reply_url(self):
        return reverse('blog:reply-comment', kwargs={'pk': self.pk})

    def get_delete_comment_url(self):
        return reverse('blog:delete-comment', kwargs={'pk': self.pk})


def gen_slug(sender, created, instance: BlogPost, *args, **kwargs):
    if created:
        slug = slugify(instance.title)
        instance.slug = slug
        instance.save()


post_save.connect(gen_slug, sender=BlogPost)
