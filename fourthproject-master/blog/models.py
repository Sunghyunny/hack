from django.db import models
from django.urls import reverse_lazy
from user.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    writer = models.CharField(max_length=100)
    post_date = models.DateTimeField(auto_now_add=True)
    post_title = models.CharField(max_length=100)
    post_contents = RichTextUploadingField()
    post_hit = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.post_title

    def get_absolute_url(self):
        return reverse_lazy('post_detail', args=[str(self.id)])

    def get_previous_post(self):
        return self.get_previous_by_post_date()

    def get_next_post(self):
        return self.get_next_by_post_date()

    @property
    def update_counter(self):
        self.post_hit = self.post_hit + 1
        self.save()

    @property
    def is_auth(self, nick):
        if writer != nick:
            return False
        else:
            return True


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name='comments')
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_contents = models.CharField(max_length=200)
    comment_writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-id']
