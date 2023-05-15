from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=32,widget=forms.TextInput(attrs={
        'class': 'input', 'placeholder':'用户名/邮箱'
    }))
    password = forms.CharField(label='密码',min_length=6,widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder':'密码'
    }))

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password =self.cleaned_data.get('password')

        if username == password:
            raise forms.ValidationError('用户名与密码不能相同！')
        return password

class RegisterForm(forms.ModelForm):

    username = forms.CharField(label='用户名',max_length=32,widget=forms.TextInput(attrs={
        'class': 'input', 'placeholder':'用户名'
    }))

    email = forms.EmailField(label='邮箱',max_length=32,widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder':'邮箱'
    }))

    password = forms.CharField(label='密码',min_length=6,widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder':'密码'
    }))

    password1 = forms.CharField(label='再次输入密码',min_length=6,widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder':'再次密码'
    }))

    class Meta:
        model = User
        fields = ('username','email')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('用户已存在')
        return email

    def clean_password1(self):
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise forms.ValidationError('两次密码输入不一致')
        return self.cleaned_data['password']
    

class ForgetPwdForm(forms.Form):
    """ 填写邮箱地址表单 """
    email = forms.EmailField(label='请输入注册邮箱地址', min_length=4, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': '用户名/邮箱'
    }))

class ModifyPwdForm(forms.Form):
	"""Form definition for UserProfile."""
	password = forms.CharField(label='输入新密码', min_length=6, 
		widget=forms.PasswordInput(attrs={'class':'input', 'placeholder':'输入新密码'}))

class UserForm(forms.ModelForm):
    """ User模型的表单,只允许修改email一个数据,用户名不允许修改 """
    email = forms.EmailField( min_length=4, widget=forms.EmailInput(attrs={
        'class': 'input'
    }))
    nick_name = forms.CharField( min_length=4, widget=forms.EmailInput(attrs={
        'class': 'input'
    }))
    class Meta:
        model = User
        fields = ('email',)


class UserProfileForm(forms.ModelForm):
    """ UserProfile的表单 """
    class Meta:
        """Meta definition for UserInfoform."""
        model = UserProfile
        fields = ('nick_name','desc', 'birthday', 'gexing', 'gender', 'address', 'image')