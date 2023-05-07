from django import forms
from django.http import JsonResponse
from django.shortcuts import render, redirect

from web import models


def phone_list(request):
    """ 手机号查询 """
    queryset = models.Phone.objects.all().order_by("id")
    return render(request, "phone_list.html", {"queryset": queryset})


class PhoneModelForm(forms.ModelForm):
    class Meta:
        model = models.Phone
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 自定义操作
        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


def add_phone(request):
    """ 添加手机号 """
    if request.method == 'GET':
        form = PhoneModelForm()
        return render(request, "phone_form.html", {"form": form})

    form = PhoneModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, "phone_form.html", {"form": form})
    form.save()
    return redirect('/phone/list/')


def edit_phone(request, pid):
    """ 修改手机号 """
    phone_object = models.Phone.objects.filter(id=pid).first()

    if request.method == "GET":
        form = PhoneModelForm(instance=phone_object)
        return render(request, "phone_form.html", {"form": form})

    form = PhoneModelForm(instance=phone_object, data=request.POST)
    if not form.is_valid():
        return render(request, "phone_form.html", {"form": form})
    form.save()
    return redirect("/phone/list/")


def delete_phone(request):
    """ 删除手机号 """
    pid = request.GET.get('pid')
    models.Phone.objects.filter(id=pid).delete()

    # 内部进行序列化
    return JsonResponse({"status": True})
