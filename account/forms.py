from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)
from .models import UserBase


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Mật khẩu',
            'id': 'login-pwd',
        }
    ))


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(
        label='Tên người dùng', min_length=4, max_length=50, help_text='Bắt buộc')
    email = forms.EmailField(max_length=100, help_text='Bắt buộc', error_messages={
        'required': 'Xin lỗi, bạn phải nhập email của mình!'})
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Nhập lại mật khấu', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email',)

    def clean_user_name(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Tên đã được sử dụng.")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Mật khẩu không khớp.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Vui lòng sử dụng email khác, email này đã được sử dụng.')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Tên người dúng'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Email', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Mật khẩu'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Nhập lại mật khẩu'})


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Rất tiếc, chúng tôi không thể tìm thấy địa chỉ email này.')
        return email

class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Mật khẩu mới', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Mật khẩu mới', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Nhập lại mật khẩu', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Nhập lại mật khẩu mới', 'id': 'form-new-pass2'}))

class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email (Không thể thay đổi)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email', 'readonly': 'readonly'}))

    user_name = forms.CharField(
        label='Họ và tên đệm', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Tên người dùng', 'id': 'form-firstname', 'readonly': 'readonly'}))

    first_name = forms.CharField(
        label='Tên người dùng', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'id': 'form-lastname'}))

    class Meta:
        model = UserBase
        fields = ('email', 'user_name', 'first_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True