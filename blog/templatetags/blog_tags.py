from django.template.library import Library
from ..models import Category
register = Library()


@register.filter()
def get_blog_categories(request):
    return Category.objects.all()
