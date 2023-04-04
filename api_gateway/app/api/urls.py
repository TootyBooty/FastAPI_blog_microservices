from core.config import Config

# users service
user_auth_url: str = f'{Config.USERS_SERVICE_URL}/auth/login'
user_base_url: str = f'{Config.USERS_SERVICE_URL}/user'

#blog service
blog_post_url: str = f'{Config.BLOG_SERVICE_URL}/blog/post'
blog_comment_url: str = f'{Config.BLOG_SERVICE_URL}/blog/comment'