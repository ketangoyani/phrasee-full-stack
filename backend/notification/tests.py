import os
import json
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from notification.models import Notification, User, Post
from notification.serializers import UserSerializer, PostSerializer
from notification.utils import load_notifications, generate_aggregated_notifications
from backend.utils import build_absolute_url
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse


class NotificationTestCase(TestCase):
    def setUp(self):
        self.notification_data = [{
    "type": "Like",
    "post": {
        "id": "b1638f970c3ddd528671df76c4dcf13e",
        "title": "Acme Inc dynamically scales niches worldwide"
    },
    "user": {
        "id": "403f220c3d413fe9cb0b36142ebfb35d",
        "name": "Mary T. Price"
    }
},{
    "type": "Like",
    "post": {
        "id": "7d78ff348647b782cb3027d836d23e09",
        "title": "How to professionally administrate seamless growth strategies in 10 steps"
    },
    "user": {
        "id": "cc81a8b1fceb3306997be05426b668e4",
        "name": "Bojana Novaković",
        "avatar": "portrait_01.png"
    }
},{
    "type": "Comment",
    "post": {
        "id": "c4cfbe322bb834ada81719036f9b287b",
        "title": "How to distinctively leverage existing wireless ROI"
    },
    "comment":{
        "id": "9c6adba459bca33ee8ae81e4b1ca420c",
        "commentText": "True! And after that they should functionalize core competencies"
    },
    "user":{
        "id": "7305d0a8bb9d7166b8d26ca856930b8d",
        "name": "Ali Sage",
        "avatar": "portrait_02.png"
    }
},{
    "type": "Like",
    "post": {
        "id": "7d78ff348647b782cb3027d836d23e09",
        "title": "How to professionally administrate seamless growth strategies in 10 steps"
    },
    "user": {
        "id": "ac487e5866d80dfcb77a89f55d2b0055",
        "name": "Mr Smartypants",
        "avatar": "portrait_03.png"
    }
},{
    "type": "Like",
    "post": {
        "id": "7d78ff348647b782cb3027d836d23e09",
        "title": "How to professionally administrate seamless growth strategies in 10 steps"
    },
    "user": {
        "id": "13e175f3a6ce2f07451b697238202c2c",
        "name": "Katie Blackman",
        "avatar": "portrait_04.png"
    }
},{
    "type": "Like",
    "post": {
        "id": "b1638f970c3ddd528671df76c4dcf13e",
        "title": "Acme Inc dynamically scales niches worldwide"
    },
    "user": {
        "id": "5497afbf9df3f6ff6f9ba11cdef5310f",
        "name": "Suoma Narjus",
        "avatar": "portrait_05.png"
    }
},{
    "type": "Like",
    "post": {
        "id": "7d78ff348647b782cb3027d836d23e09",
        "title": "How to professionally administrate seamless growth strategies in 10 steps"
    },
    "user": {
        "id": "9a1afe07885bac989383b7b145c516d6",
        "name": "Chuck Looij",
        "avatar": "portrait_06.png"
    }
},{
    "type": "Comment",
    "post": {
        "id": "c4cfbe322bb834ada81719036f9b287b",
        "title": "How to distinctively leverage existing wireless ROI"
    },
    "comment":{
        "id": "e1788fb8b05d79c793c2002d57e80182",
        "commentText": "😩 I really disagree with the content of this post. I belive the the client should really try to synthesize internal or 'organic' sources before not after leveraging!"
    },
    "user":{
        "id": "f1333326efc51be3d620d80f72c55944",
        "name": "Harold Lachlan",
        "avatar": "portrait_07.png"
    }
},{
    "type": "Like",
    "post": {
        "id": "de8b75335ba7e52e62c8227c6697def2",
        "title": "This company enthusiastically deployed extensive values, the rest is history"
    },
    "user": {
        "id": "38bbd19a89ac307cff5ab2b5bf83783a",
        "name": "",
        "avatar": "portrait_08.png"
    }
},{
    "type": "Comment",
    "post": {
        "id": "c4cfbe322bb834ada81719036f9b287b",
        "title": "How to distinctively leverage existing wireless ROI"
    },
    "comment":{
        "id": "410065f8dee7354ba6fa7f5552092657",
        "commentText": "😂 That'll be the day!"
    },
    "user":{
        "id": "f1333326efc51be3d620d80f72c55944",
        "name": "Harold Lachlan",
        "avatar": "portrait_07.png"
    }
},{
    "type": "Comment",
    "post": {
        "id": "b1638f970c3ddd528671df76c4dcf13e",
        "title": "Acme Inc dynamically scales niches worldwide"
    },
    "comment":{
        "id": "46f72ffb3a5717dcd71e26369d1e13a5",
        "commentText": "Acme remains one of my fave company ever! The way they scale is so dynamic that makes HTML5 look static!"
    },
    "user":{
        "id": "5497afbf9df3f6ff6f9ba11cdef5310f",
        "name": "Suoma Narjus",
        "avatar": "portrait_05.png"
    }
},{
    "type": "Like",
    "post": {
        "id": "b1638f970c3ddd528671df76c4dcf13e",
        "title": "Acme Inc dynamically scales niches worldwide"
    },
    "user": {
        "id": "fa527981cbbcb070be95854985c3188f",
        "name": "Sandra Ortega",
        "avatar": "portrait_09.png"
    }
},{
    "type": "Like",
    "post": {
        "id": "b1638f970c3ddd528671df76c4dcf13e",
        "title": "Acme Inc dynamically scales niches worldwide"
    },
    "user": {
        "id": "4c18d43d4deccbac21a26c55f1033f53",
        "name": "William Hunt",
        "avatar": "portrait_10.png"
    }
},{
    "type": "Like",
    "post": {
        "id": "7d78ff348647b782cb3027d836d23e09",
        "title": "How to professionally administrate seamless growth strategies in 10 steps"
    },
    "user": {
        "id": "7bd3695eba3be49ef29bd423b12555bc",
        "name": "Hamish Sutcliffe",
        "avatar": "portrait_11.png"
    }
},{
    "type": "Like",
    "post": {
        "id": "b1638f970c3ddd528671df76c4dcf13e",
        "title": "Acme Inc dynamically scales niches worldwide"
    },
    "user": {
        "id": "38be3079117301f2f61264d6e0fbf7db",
        "name": "An Mao",
        "avatar": "portrait_12.png"
    }
},{
    "type": "Like",
    "post": {
        "id": "7d78ff348647b782cb3027d836d23e09",
        "title": "How to professionally administrate seamless growth strategies in 10 steps"
    },
    "user": {
        "id": "084300a01df3060f41fad4700a70b6fe",
        "name": "Eugenio Bertè",
        "avatar": "portrait_13.png"
    }
},{
    "type": "Comment",
    "post": {
        "id": "57e0d6328c9287bd1b66bc327efbcdfa",
        "title": "Boom&Bust to uniquely coordinate standardized meta-services"
    },
    "comment":{
        "id":"a82f598e7723c68599e597b5939ad437",
        "commentText": "Here we go again!"
    },
    "user":{
        "id": "9a1afe07885bac989383b7b145c516d6",
        "name": "Chuck Looij",
        "avatar": "portrait_14.png"
    }
}]

    def test_load_notifications(self):
        file_path = "test_notifications.json"
        with open(file_path, 'w') as file:
            json.dump(self.notification_data, file)

        load_notifications(file_path)

        # Check if User, Post, and Notification objects are created correctly
        user_count = User.objects.count()
        post_count = Post.objects.count()
        notification_count = Notification.objects.count()

        self.assertEqual(user_count, 14)  # Update this value based on the actual number of users in the data
        self.assertEqual(post_count, 5)
        self.assertEqual(notification_count, len(self.notification_data))

        # Clean up
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass

    def test_generate_aggregated_notifications(self):
        # Create User and Post objects for the test data
        file_path = "test_notifications.json"
        with open(file_path, 'w') as file:
            json.dump(self.notification_data, file)

        load_notifications(file_path)

        # Test the generate_aggregated_notifications function
        aggregated_data = generate_aggregated_notifications()

        # Update this assertion based on the actual aggregated data
        self.assertEqual(len(aggregated_data), 6)

        # Clean up
        User.objects.all().delete()
        Post.objects.all().delete()
        Notification.objects.all().delete()


class UserSerializerTestCase(TestCase):
    def setUp(self):
        # Create a User instance for testing
        self.user = User.objects.create(
            id="test_user",
            name="Test User",
            avatar_image_name="test_avatar.png"
        )
        self.serializer = UserSerializer(instance=self.user)

    def test_serializer_fields(self):
        # Test if the serialized data contains the expected fields
        data = self.serializer.data
        self.assertIn("id", data)
        self.assertIn("name", data)
        self.assertIn("avatar_url", data)

    def test_avatar_url_generation(self):
        # Test if the avatar_url is generated correctly
        avatar_url = self.serializer.data["avatar_url"]
        expected_url = build_absolute_url(staticfiles_storage.url("portraits/test_avatar.png"))
        self.assertEqual(avatar_url, expected_url)

    def test_no_avatar_url_if_no_image_name(self):
        # Test if avatar_url is None when avatar_image_name is not present
        self.user.avatar_image_name = None
        self.user.save()
        serializer = UserSerializer(instance=self.user)
        avatar_url = serializer.data["avatar_url"]
        self.assertIsNone(avatar_url)

    def test_name_override_in_to_representation(self):
        # Test if the name field is overridden in to_representation
        serializer = UserSerializer(instance=self.user)
        data = serializer.to_representation(self.user)
        self.assertEqual(data["name"], "Test User")
