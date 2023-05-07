from io import BytesIO

from django import forms
from django.shortcuts import render, HttpResponse, redirect

from web import models
from utils.encrypt import md5
from utils.helper import check_code


class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control",
                                      "placeholder": "请输入用户名"})
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class": "form-control",
                                          "placeholder": "请输入用户名"},
                                   render_value=True)
    )
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={'class': "form-control",
                                      'placeholder': '请输入验证码', })

    )


def login(request):
    """ 用户登录 """
    if request.method == 'GET':
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    form = LoginForm(data=request.POST)
    if not form.is_valid():
        return render(request, "login.html", {"form": form})
    # 1.判断验证码是否正确
    image_code = request.session.get("image_code")
    # 验证码失效
    if not image_code:
        form.add_error("code", "验证码过期")
        return render(request, "login.html", {"form": form})
    if image_code.upper() != form.cleaned_data["code"].upper():
        form.add_error("code", "验证码错误")
        return render(request, "login.html", {"form": form})
    # 2.验证码正确去数据库校验密码用户名
    username = form.cleaned_data["username"]
    password = form.cleaned_data["password"]  # md5 加密在与数据库比较
    encrypted_password = md5(password)
    admin_object = models.Admin.objects.filter(username=username, password=encrypted_password).first()
    if not admin_object:
        return render(request, "login.html", {"form": form, "error": "用户名或密码错误"})
    # 保存session，并七天免登录
    request.session["info"] = {"id": admin_object.id, "username": admin_object.username}
    request.session.set_expiry(60 * 60 * 24 * 7)
    return redirect('/home/')


def img_code(request):
    """ 验证码功能 """
    # 1.生成图片
    img_obj, code_str = check_code()

    # 2.把图片写入内存，从内存中读取并返回
    stream = BytesIO()
    img_obj.save(stream, 'png')

    # 3.将图片内容写进session中 + 60s
    request.session["image_code"] = code_str
    request.session.set_expiry(60)

    return HttpResponse(stream.getvalue())


def logout(request):
    """ 注销功能 """
    request.session.clear()
    return redirect("/login/")


def home(request):
    """ 进入主页面"""
    return render(request, "home.html")
