from ninja import NinjaAPI, Schema
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI, api_controller, route
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from validate_email import validate_email
from django.core.exceptions import ValidationError
from ninja_jwt.authentication import JWTAuth
from django.contrib.auth import authenticate
from typing import Dict

# 创建一个NinjaExtraAPI实例
Login = NinjaExtraAPI()
# 注册NinjaJWTDefaultController，用于处理JWT认证相关的路由
Login.register_controllers(NinjaJWTDefaultController)

# 定义一个注册用户的Schema，包含用户名、密码和邮箱
class RegisterSchema(Schema):
    username: str
    password: str
    email: str

# 定义一个登录用户的Schema，包含用户名和密码
class LoginSchema(Schema):
    username: str
    password: str

# 定义一个消息Schema，包含一个消息字符串
class MessageSchema(Schema):
    message: str

# 定义一个TokenSchema，包含访问令牌和刷新令牌
class TokenSchema(Schema):
    access: str
    refresh: str

@Login.post("/register", response={201: MessageSchema, 400: MessageSchema})
def register(request, data: RegisterSchema):
    try:
        # 验证密码强度
        validate_password(data.password)
        
        # 检查用户名是否已存在
        if User.objects.filter(username=data.username).exists():
            return 400, {"message": "用户名已存在"}
            
        # 检查邮箱是否已存在
        if User.objects.filter(email=data.email).exists():
            return 400, {"message": "邮箱已被注册"}
        
        # 创建新用户
        user = User.objects.create_user(
            username=data.username,
            email=data.email,
            password=data.password
        )
        return 201, {"message": "注册成功"}
        
    except ValidationError as e:
        return 400, {"message": str(e.messages[0])}
    except Exception as e:
        return 400, {"message": str(e)}

@Login.post("/login", response={200: TokenSchema, 401: MessageSchema})
def login(request, data: LoginSchema):
    user = authenticate(username=data.username, password=data.password)
    if user is None:
        return 401, {"message": "用户名或密码错误"}
    
    from ninja_jwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    
    return 200, {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "message": "登录成功"
    }

# 测试认证的路由
@Login.get("/test-auth", auth=JWTAuth(), response={200: MessageSchema, 401: MessageSchema})
def test_auth(request):
    return 200, {"message": "认证成功"} 