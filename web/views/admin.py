from django import forms
from django.http import JsonResponse
from django.shortcuts import render, redirect

from web import models
from utils.encrypt import md5


def admin_list(request):
    """ 管理员列表 """

    # queryst : [obj,obj,...]
    queryset = models.Admin.objects.all().order_by("id")

    return render(request, "admin_list.html", {"queryset": queryset})


class AdminModelForm(forms.ModelForm):
    class Meta:
        model = models.Admin
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 自定义操作
        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


def add_admin(request):
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, "admin_form.html", {"form": form})

    form = AdminModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, "admin_form.html", {"form": form})

    # 密码更新为md5加密
    form.instance.password = md5(form.instance.password)
    form.save()
    return redirect('/admin/list/')


class AdminEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Admin
        fields = ["username", "age", "gender", "depart_id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 自定义操作
        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


def edit_admin(request, aid):
    admin_object = models.Admin.objects.filter(id=aid).first()

    if request.method == 'GET':
        form = AdminEditModelForm(instance=admin_object)
        return render(request, 'admin_form.html', {"form": form})

    form = AdminEditModelForm(instance=admin_object, data=request.POST)
    if not form.is_valid():
        return render(request, "admin_form.html", {"form": form})
    # 更新
    form.save()
    return redirect('/admin/list/')


def delete_admin(request):
    aid = request.GET.get('aid')
    models.Admin.objects.filter(id=aid).delete()

    # 内部进行序列化
    return JsonResponse({"status": True})
