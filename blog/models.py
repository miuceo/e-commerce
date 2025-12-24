from django.db import models

# Create your models here.

class Tag(models.Model):
    tag = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.tag

class Blog(models.Model):
    slug = models.SlugField(unique=True, primary_key=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    quote = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to='blogs')
    tags = models.ManyToManyField(Tag, related_name="blogs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title