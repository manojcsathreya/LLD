import uuid
from datetime import datetime
from enum import Enum
from concurrent.futures import ThreadPoolExecutor

# Enum classes for Notification and related statuses
class NotificationType(Enum):
    FRIEND_REQUEST = 1
    FRIEND_REQUEST_ACCEPTED = 2
    LIKE = 3
    COMMENT = 4
    MENTION = 5

# User class to represent user profiles
class User:
    def __init__(self, id, name, email, password, profile_picture, bio, friends, posts):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.profile_picture = profile_picture
        self.bio = bio
        self.friends = friends
        self.posts = posts

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def get_profile_picture(self):
        return self.profile_picture

    def get_bio(self):
        return self.bio

    def get_friends(self):
        return self.friends

    def get_posts(self):
        return self.posts

# Comment class to handle post comments
class Comment:
    def __init__(self, id, user_id, post_id, content, timestamp):
        self.id = id
        self.user_id = user_id
        self.post_id = post_id
        self.content = content
        self.timestamp = timestamp

    def get_id(self):
        return self.id

    def get_user_id(self):
        return self.user_id

    def get_post_id(self):
        return self.post_id

    def get_content(self):
        return self.content

    def get_timestamp(self):
        return self.timestamp

# Notification class for user notifications
class Notification:
    def __init__(self, id, user_id, notification_type, content, timestamp):
        self.id = id
        self.user_id = user_id
        self.type = notification_type
        self.content = content
        self.timestamp = timestamp

    def get_id(self):
        return self.id

    def get_user_id(self):
        return self.user_id

    def get_type(self):
        return self.type

    def get_content(self):
        return self.content

    def get_timestamp(self):
        return self.timestamp

# Post class to represent user posts
class Post:
    def __init__(self, id, user_id, content, image_urls, video_urls, timestamp, likes, comments):
        self.id = id
        self.user_id = user_id
        self.content = content
        self.image_urls = image_urls
        self.video_urls = video_urls
        self.timestamp = timestamp
        self.likes = likes
        self.comments = comments

    def get_id(self):
        return self.id

    def get_user_id(self):
        return self.user_id

    def get_content(self):
        return self.content

    def get_image_urls(self):
        return self.image_urls

    def get_video_urls(self):
        return self.video_urls

    def get_timestamp(self):
        return self.timestamp

    def get_likes(self):
        return self.likes

    def get_comments(self):
        return self.comments

# Social Networking Service class (Singleton pattern)
class SocialNetworkingService:
    _instance = None
    _lock = ThreadPoolExecutor(max_workers=1)

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.users = {}
        self.posts = {}
        self.notifications = {}

    def register_user(self, user):
        self.users[user.get_id()] = user

    def login_user(self, email, password):
        for user in self.users.values():
            if user.get_email() == email and user.get_password() == password:
                return user
        return None

    def update_user_profile(self, user):
        self.users[user.get_id()] = user

    def send_friend_request(self, sender_id, receiver_id):
        receiver = self.users.get(receiver_id)
        if receiver:
            notification = Notification(str(uuid.uuid4()), receiver_id, NotificationType.FRIEND_REQUEST,
                                        f"Friend request from {sender_id}", datetime.now())
            self._add_notification(receiver_id, notification)

    def accept_friend_request(self, user_id, friend_id):
        user = self.users.get(user_id)
        friend = self.users.get(friend_id)
        if user and friend:
            user.get_friends().append(friend_id)
            friend.get_friends().append(user_id)
            notification = Notification(str(uuid.uuid4()), friend_id, NotificationType.FRIEND_REQUEST_ACCEPTED,
                                        f"Friend request accepted by {user_id}", datetime.now())
            self._add_notification(friend_id, notification)

    def create_post(self, post):
        self.posts[post.get_id()] = post
        user = self.users.get(post.get_user_id())
        if user:
            user.get_posts().append(post)

    def get_newsfeed(self, user_id):
        newsfeed = []
        user = self.users.get(user_id)
        if user:
            friend_ids = user.get_friends()
            for friend_id in friend_ids:
                friend = self.users.get(friend_id)
                if friend:
                    newsfeed.extend(friend.get_posts())
            newsfeed.extend(user.get_posts())
            newsfeed.sort(key=lambda post: post.get_timestamp(), reverse=True)
        return newsfeed

    def like_post(self, user_id, post_id):
        post = self.posts.get(post_id)
        if post and user_id not in post.get_likes():
            post.get_likes().append(user_id)
            notification = Notification(str(uuid.uuid4()), post.get_user_id(), NotificationType.LIKE,
                                        f"Your post was liked by {user_id}", datetime.now())
            self._add_notification(post.get_user_id(), notification)

    def comment_on_post(self, comment):
        post = self.posts.get(comment.get_post_id())
        if post:
            post.get_comments().append(comment)
            notification = Notification(str(uuid.uuid4()), post.get_user_id(), NotificationType.COMMENT,
                                        f"Your post received a comment from {comment.get_user_id()}", datetime.now())
            self._add_notification(post.get_user_id(), notification)

    def _add_notification(self, user_id, notification):
        if user_id not in self.notifications:
            self.notifications[user_id] = []
        self.notifications[user_id].append(notification)

    def get_notifications(self, user_id):
        return self.notifications.get(user_id, [])

# Demo class to showcase functionality
class SocialNetworkingServiceDemo:
    @staticmethod
    def run():
        social_networking_service = SocialNetworkingService()

        # User registration
        user1 = User("1", "John Doe", "john@example.com", "password", "profile1.jpg", "I love coding!", [], [])
        user2 = User("2", "Jane Smith", "jane@example.com", "password", "profile2.jpg", "Exploring the world!", [], [])
        social_networking_service.register_user(user1)
        social_networking_service.register_user(user2)

        # User login
        logged_in_user = social_networking_service.login_user("john@example.com", "password")
        if logged_in_user:
            print(f"User logged in: {logged_in_user.get_name()}")
        else:
            print("Invalid email or password.")

        # Send friend request
        social_networking_service.send_friend_request(user1.get_id(), user2.get_id())

        # Accept friend request
        social_networking_service.accept_friend_request(user2.get_id(), user1.get_id())

        # Create posts
        post1 = Post("post1", user1.get_id(), "My first post!", [], [], datetime.now(), [], [])
        post2 = Post("post2", user2.get_id(), "Having a great day!", [], [], datetime.now(), [], [])
        social_networking_service.create_post(post1)
        social_networking_service.create_post(post2)

        # Like a post
        social_networking_service.like_post(user2.get_id(), post1.get_id())

        # Comment on a post
        comment = Comment("comment1", user2.get_id(), post1.get_id(), "Great post!", datetime.now())
        social_networking_service.comment_on_post(comment)

        # Get newsfeed
        newsfeed = social_networking_service.get_newsfeed(user1.get_id())
        print("Newsfeed:")
        for post in newsfeed:
            print(f"Post: {post.get_content()}")
            print(f"Likes: {len(post.get_likes())}")
            print(f"Comments: {len(post.get_comments())}")
            print()

        # Get notifications
        notifications = social_networking_service.get_notifications(user1.get_id())
        print("Notifications:")
        for notification in notifications:
            print(f"Type: {notification.get_type()}")
            print(f"Content: {notification.get_content()}")
            print()

# Running the demo
if __name__ == "__main__":
    SocialNetworkingServiceDemo.run()
