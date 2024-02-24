from django.db import models

class User(models.Model):
    """
    Model representing a user in the database.

    Fields:
    - id (str): Primary key for the user, with a maximum length of 34 characters.
    - name (str): The name of the user, with a maximum length of 255 characters.
    - avatar_image_name (str, optional): The filename of the user's avatar image, with a maximum length of 50 characters.
                                         Can be null or blank.
    """
    id = models.CharField(max_length=34, primary_key=True)
    name = models.CharField(max_length=255)
    avatar_image_name = models.CharField(max_length=50, null=True, blank=True)

class Post(models.Model):
    """
    Model representing a post in the database.

    Fields:
    - id (str): Primary key for the post, with a maximum length of 34 characters.
    - title (str): The title of the post, with a maximum length of 512 characters.
    """
    id = models.CharField(max_length=34, primary_key=True)
    title = models.CharField(max_length=512)

class Notification(models.Model):
    """
    Model representing a notification in the database.

    Fields:
    - type (str): The type of notification, with a maximum length of 10 characters.
    - post (Post): ForeignKey relationship to the Post model, allowing a notification to be associated with a post.
                   If the associated post is deleted, the reference is set to NULL.
    - user (User): ForeignKey relationship to the User model, allowing a notification to be associated with a user.
                   If the associated user is deleted, the reference is set to NULL.
    """
    type = models.CharField(max_length=10)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

