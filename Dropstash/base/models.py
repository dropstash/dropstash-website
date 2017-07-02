from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='user', on_delete=models.CASCADE, primary_key=True)
    avatar = models.ImageField(verbose_name='avatar')
    
    # @property
    # def stash(self):


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Post(models.Model):
    author = models.ForeignKey(User, verbose_name='author', on_delete=models.CASCADE)

    link = models.URLField(verbose_name='hyperlink')
    headline = models.CharField(max_length=200, verbose_name='headline')
    description = models.TextField(verbose_name='comment')
    content = models.TextField(verbose_name='quote')
    preview_picture = models.ImageField(verbose_name='preview picture', blank=True)

    clusters = models.ManyToManyField(Cluster, verbose_name='used in clusters')

    submission_datetime = models.DateTimeField(verbose_name='submission datetime', default=datetime.now, blank=True)
    is_published = models.BooleanField(default=False, blank=True, verbose_name='publication marker')
    publication_datetime = models.DateTimeField(verbose_name='publication datetime', default=datetime.now, blank=True)

    def publish(self):
        if not self.is_published:
            self.is_published = True
            self.publication_datetime = datetime.now()
            # TODO: also reposts

    def conceal(self):
        if self.is_published:
            self.is_published = False
            # TODO: also reposts


class PostComment(models.Model):
    post = models.ForeignKey(Post, verbose_name='linked post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='linked user', on_delete=models.CASCADE)
    message = models.TextField(verbose_name='comment')


class PostVoteUp(models.Model):
    user = models.ForeignKey(User, verbose_name='linked user', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name='linked post')

    class Meta:
        unique_together = ('user', 'post',)


class PostVoteDown(models.Model):
    user = models.ForeignKey(User, verbose_name='linked user', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name='linked post')

    class Meta:
        unique_together = ('user', 'post',)


class Repost(models.Model):
    user = models.ForeignKey(User, verbose_name='reposted by', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name='post')
    publication_datetime = models.DateTimeField(verbose_name='publication datetime', default=datetime.now, blank=True)


class Cluster(models.Model):
    headline = models.CharField(max_length=200, verbose_name='headline')
    content = models.TextField(verbose_name='cluster overlay')


class ClusterComment(models.Model):
    cluster = models.ForeignKey(Cluster, 'linked cluster', on_delete=models.CASCADE)
    user = models.ForeignKey(User, 'linked user', on_delete=models.CASCADE)
    message = models.TextField(verbose_name='comment')


class ClusterVoteUp(models.Model):
    user = models.ForeignKey(User, verbose_name='linked user', on_delete=models.CASCADE)
    cluster = models.ForeignKey(Cluster, verbose_name='linked post')

    class Meta:
        unique_together = ('user', 'cluster',)


class ClusterVoteDown(models.Model):
    user = models.ForeignKey(User, verbose_name='linked user', on_delete=models.CASCADE)
    cluster = models.ForeignKey(Cluster, verbose_name='linked post')

    class Meta:
        unique_together = ('user', 'cluster',)


class Tag(models.Model):
    title = models.CharField(max_length=200, verbose_name='tag')

