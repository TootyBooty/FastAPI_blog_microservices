from core.config import Config

# users service
user_auth_url: str = f"{Config.USERS_SERVICE_URL}/login/token"
user_base_url: str = f"{Config.USERS_SERVICE_URL}/user"
user_all_url: str = f"{user_base_url}/all"
user_profile_url: str = f"{user_base_url}/profile"
user_role_url: str = f"{user_base_url}/role"

# blog service
blog_base_url: str = f"{Config.BLOG_SERVICE_URL}/blog"
blog_post_url: str = f"{blog_base_url}/post"
blog_comment_url: str = f"{blog_base_url}comment"
blog_all_posts_url: str = f"{blog_base_url}/all"
