import django
from django.conf import settings
from django.template.loader import get_template

settings.configure(TEMPLATES=[{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    # if you want to render using template file
    'DIRS': [r'C:\Users\15314\PycharmProjects\Blog_Aggregator\blog_aggregator\templates' ]
}])

django.setup()



