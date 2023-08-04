from core.config import Config

# users service
user_auth_url: str = f"{Config.USERS_SERVICE_URL}/login/token/"
user_base_url: str = f"{Config.USERS_SERVICE_URL}/user/"
user_ping_url: str = f"{Config.USERS_SERVICE_URL}/ping/"
user_list_url: str = user_base_url
user_profile_url: str = f"{user_base_url}/profile/"
user_role_url: str = f"{user_base_url}/role/"

# blog service
blog_base_url: str = f"{Config.BLOG_SERVICE_URL}/blog/"
blog_ping_url: str = f"{Config.BLOG_SERVICE_URL}/ping/"
blog_post_url: str = f"{blog_base_url}/post/"
blog_comment_url: str = f"{blog_base_url}comment/"
