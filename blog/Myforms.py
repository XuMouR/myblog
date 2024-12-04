# form组件的钩子需要使用的模块
from django import forms
# widgets插件，给Form生成的标签添加class等属性
from django.forms import widgets
from .models import UserInfo
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError


class UserForm(forms.Form):
    # 用户forms验证表
    user = forms.CharField(max_length=32, label="用户名",
                           widget=widgets.TextInput(attrs={"class": "form-control"}),
                           error_messages={
                               "required": "用户名不能为空"
                           })
    pwd = forms.CharField(max_length=32, label="密码",
                          widget=widgets.PasswordInput(attrs={"class": "form-control"}),
                          error_messages={
                              "required": "密码不能为空"
                          })
    r_pwd = forms.CharField(max_length=32, label="确认密码",
                            widget=widgets.PasswordInput(attrs={"class": "form-control"}),
                            error_messages={
                                "required": "确认密码不能为空"
                            })
    email = forms.EmailField(max_length=32, label="注册邮箱", required=False,
                             widget=widgets.EmailInput(attrs={"class": "form-control"}))

    #
    def clean_user(self):
        user = self.cleaned_data.get("user")
        print("钩子中的user〉〉〉", user)
        user_obj = UserInfo.objects.filter(username=user).first()
        print("从数据库中匹配的user对象〉〉〉",user_obj)
        if not user_obj:
            return user
        else:
            raise ValidationError("用户名已经被注册")

    def clean(self):
        pwd = self.cleaned_data.get("pwd")
        r_pwd = self.cleaned_data.get("r_pwd")

        if pwd == r_pwd:
            return self.cleaned_data
        else:
            raise ValidationError("两次密码不一致")


class ChangePwdForm(forms.Form):
    oldpwd=forms.CharField(
        required=True,
        label=u"原密码",
        error_messages={'required':u"请输入原密码"},
        widget=forms.PasswordInput(
            attrs={
                "placeholder":u"原密码",
            }
        ),
    )

    newpwd1=forms.CharField(
        required=True,
        label=u"新密码",
        error_messages={"required":u"请输入新密码"},
        widget=forms.PasswordInput(
            attrs={
                "placehold":u"新密码",
            }
        ),
    )

    newpwd2=forms.CharField(
        required=True,
        label=u"确认密码",
        error_messages={"required":u"请再次输入新密码"},
        widget=forms.PasswordInput(
            attrs={
                "placehold":u'确认密码',
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"所有项都为必填项")
        elif self.cleaned_data['newpwd1'] != self.cleaned_data['newpwd2']:
            raise forms.ValidationError(u"两次输入的密码不一致")
        else:
            cleaned_data=super(ChangePwdForm,self).clean()

        return cleaned_data