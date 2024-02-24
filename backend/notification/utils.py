from collections import defaultdict
import json

from notification.models import Notification, User, Post
from notification.serializers import PostSerializer, UserSerializer

def load_notifications(file_path):
    """
    Load notifications from a JSON file and create corresponding User, Post, and Notification objects.

    Parameters:
    - file_path (str): The path to the JSON file containing notification data.

    Raises:
    - FileNotFoundError: If the specified file_path does not exist.

    Note:
    - This function assumes that the JSON file has a specific structure with 'user', 'post', and 'type' keys
      representing user data, post data, and notification type respectively.

    Example:
    ```
    load_notifications("/path/to/notifications.json")
    ```

    This function reads the JSON file, extracts user and post information, creates User and Post objects if they don't
    exist in the database, and then creates Notification objects using the collected data.
    """
    try:
        with open(file_path) as file:
            data = json.load(file)
            bulk_list = []

            for notification in data:
                # Extract user information
                user = notification.get("user")
                user_id = user.get("id")

                # Create User object if it doesn't exist
                if not User.objects.filter(id=user_id):
                    avatar_image_name = user.get("avatar")
                    if avatar_image_name:
                        del user["avatar"]
                    user_data = {
                        **user,
                        "avatar_image_name": avatar_image_name
                    }
                    User.objects.create(**user_data)

                # Extract post information
                post = notification.get("post")
                post_id = post.get("id")

                # Create Post object if it doesn't exist
                if not Post.objects.filter(id=post_id):
                    Post.objects.create(**post)

                # Create Notification object and add to bulk_list
                bulk_list.append(
                    Notification(
                        user_id=user_id,
                        post_id=post_id,
                        type=notification.get("type")
                    )
                )

            # Bulk create Notification objects
            Notification.objects.bulk_create(bulk_list)

    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

def generate_aggregated_notifications():
    """
    Generate aggregated notification data for efficient display.

    Returns:
    - list: A list of dictionaries representing aggregated notification data.
            Each dictionary contains 'type', 'post', and 'users' keys.

    Note:
    - This function assumes that there are Notification, User, and Post models in 'notification.models'.
      It also relies on 'notification.serializers' for serializing User and Post objects.

    Example:
    ```
    aggregated_data = generate_aggregated_notifications()
    ```

    This function retrieves all notifications from the database, aggregates them based on their type and post,
    and returns a list of dictionaries containing information about the notification type, post, and associated users.
    """
    # Use defaultdict to simplify aggregation logic
    aggregated_data = defaultdict(lambda: {"type": None, "post": None, "users": []})

    # Retrieve all notifications with related User and Post objects
    notification_qs = Notification.objects.all().select_related("post", "user")

    for notification in notification_qs:
        post_id = notification.post.id
        notification_type = notification.type

        # Append serialized user data to the 'users' list
        associated_users = UserSerializer(notification.user).data
        aggregated_data[(notification_type, post_id)]["users"].append(associated_users)

        # Update 'type' and 'post' information if not already set
        aggregated_data[(notification_type, post_id)]["type"] = notification_type
        if not aggregated_data[(notification_type, post_id)]["post"]:
            post_data = PostSerializer(notification.post).data
            aggregated_data[(notification_type, post_id)]["post"] = post_data

    # Return a list of aggregated notification data
    return list(aggregated_data.values())