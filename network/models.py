from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
	post_id = models.AutoField(primary_key=True)
	#Could be foreign key
	post_username = models.CharField(max_length=100)
	post_user_id= models.CharField(max_length=11, blank=True, null=True)
	post_date = models.CharField(max_length=11, blank=True, null=True)
	post_message = models.CharField(max_length=600)
	post_likes = models.CharField(max_length=600)
	post_comments = models.CharField(max_length=600)
	#Foreign key
	#post_likes = models.ForeignKey(Like, db_column='like_id', on_delete=models.DO_NOTHING)
	#Foreign key
	#post_comments = models.ForeignKey(Comment, db_column='comment_id', on_delete=models.DO_NOTHING)

	def __str__(self):
		return '%s' % (self.post_message)


# Likes model
class Like(models.Model):
	like_id = models.AutoField(primary_key=True)
	post_id = models.IntegerField()
	username_id = models.IntegerField()



# Follow model
class Follow(models.Model):
	follow_id = models.AutoField(primary_key=True)
	user_id = models.CharField(max_length=11)
	following_id = models.CharField(max_length=11)

