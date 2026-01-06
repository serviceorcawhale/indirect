from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,  SetPasswordForm, PasswordResetForm
from django.contrib.auth import get_user_model
from .models import *
from django.forms import ModelForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username or Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)



class ProfileForm (ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user', 'name', 'address']


class DepositForm (ModelForm):
    class Meta:
        model = Deposit
        fields = '__all__'
        exclude = ['user']

class CardForm (ModelForm):
    class Meta:
        model = Card
        fields = '__all__'
        exclude = ['user']


class AccountnumberForm (ModelForm):
    class Meta:
        model = Accountnumber
        fields = '__all__'
        exclude = ['user']


class TransferForm (ModelForm):
    class Meta:
        model = Transfer
        fields = '__all__'
        exclude = ['user', 'name', 'status']

class WithdrawForm (ModelForm):
    class Meta:
        model = Withdraw
        fields = '__all__'
        exclude = ['user', 'name', 'status']

class PinForm (ModelForm):
    class Meta:
        model = Pin
        fields = '__all__'
        exclude = ['user', 'name']


# Add these to your existing forms.py or create a new loan_forms.py

from django import forms
from .models import BusinessLoan, CarLoan, EducationLoan, HomeLoan, PersonalLoan

class BusinessLoanForm(forms.ModelForm):
    class Meta:
        model = BusinessLoan
        fields = ['name', 'email', 'phone', 'state', 'loan_amount', 'loan_term']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "What's your name?"}),
            'email': forms.EmailInput(attrs={'placeholder': "What's your email?"}),
            'phone': forms.TextInput(attrs={'placeholder': "(123) 480 - 3540"}),
            'state': forms.TextInput(attrs={'placeholder': "California"}),
            'loan_amount': forms.TextInput(attrs={'placeholder': "Ex. $8,000 USD"}),
            'loan_term': forms.TextInput(attrs={'placeholder': "Ex. 12 months"}),
        }

class CarLoanForm(forms.ModelForm):
    class Meta:
        model = CarLoan
        fields = ['name', 'email', 'phone', 'state', 'loan_amount', 'loan_term']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "What's your name?"}),
            'email': forms.EmailInput(attrs={'placeholder': "What's your email?"}),
            'phone': forms.TextInput(attrs={'placeholder': "(123) 480 - 3540"}),
            'state': forms.TextInput(attrs={'placeholder': "California"}),
            'loan_amount': forms.TextInput(attrs={'placeholder': "Ex. $8,000 USD"}),
            'loan_term': forms.TextInput(attrs={'placeholder': "Ex. 12 months"}),
        }

class EducationLoanForm(forms.ModelForm):
    terms_agreed = forms.BooleanField(
        required=True,
        error_messages={'required': 'You must agree to the terms and conditions'}
    )
    
    class Meta:
        model = EducationLoan
        fields = [
            'name', 'email', 'phone', 'state', 
            'loan_amount', 'loan_term', 'country',
            'college_name', 'gre_score', 'gmat_score',
            'full_time_study', 'existing_loan', 'terms_agreed'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': "What's your name?",
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': "What's your email?",
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': "(123) 480 - 3540",
                'required': True
            }),
            'state': forms.TextInput(attrs={
                'placeholder': "California",
                'required': True
            }),
            'loan_amount': forms.TextInput(attrs={
                'placeholder': "Ex. $8,000 USD",
                'required': True
            }),
            'loan_term': forms.TextInput(attrs={
                'placeholder': "Ex. 12 months",
                'required': True
            }),
            'country': forms.TextInput(attrs={
                'placeholder': "Country you are going",
                'required': True
            }),
            'college_name': forms.TextInput(attrs={
                'placeholder': "Enter your college/university name",
                'required': True
            }),
            'gre_score': forms.TextInput(attrs={'placeholder': "Enter GRE Score"}),
            'gmat_score': forms.TextInput(attrs={'placeholder': "Enter GMAT Score"}),
            'full_time_study': forms.HiddenInput(),
            'existing_loan': forms.HiddenInput(),
        }
        labels = {
            'college_name': 'College/University Name',
            'gre_score': 'GRE Score (if applicable)',
            'gmat_score': 'GMAT Score (if applicable)',
        }

class HomeLoanForm(forms.ModelForm):
    class Meta:
        model = HomeLoan
        fields = [
            'name', 'email', 'phone', 'state',
            'loan_amount', 'loan_term', 'purchase_price',
            'down_payment', 'property_type', 'loan_purpose',
            'property_address', 'monthly_payment', 'interest_rate', 'apr'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': "What's your name?",
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': "What's your email?",
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': "(123) 480 - 3540",
                'required': True
            }),
            'state': forms.TextInput(attrs={
                'placeholder': "California",
                'required': True
            }),
            'loan_amount': forms.TextInput(attrs={
                'placeholder': "Ex. $300,000 USD",
                'required': True
            }),
            'loan_term': forms.TextInput(attrs={
                'placeholder': "Ex. 30 Year Fixed",
                'required': True
            }),
            'purchase_price': forms.TextInput(attrs={
                'placeholder': "Ex. $375,000 USD"
            }),
            'down_payment': forms.TextInput(attrs={
                'placeholder': "Ex. $75,000 USD (20%)"
            }),
            'property_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'loan_purpose': forms.Select(attrs={
                'class': 'form-select'
            }),
            'property_address': forms.Textarea(attrs={
                'placeholder': "Enter property address (optional)",
                'rows': 3
            }),
            'monthly_payment': forms.HiddenInput(),
            'interest_rate': forms.HiddenInput(),
            'apr': forms.HiddenInput(),
        }
        labels = {
            'property_type': 'Type of Property',
            'loan_purpose': 'Purpose of Loan',
            'property_address': 'Property Address (if known)',
        }

class PersonalLoanForm(forms.ModelForm):
    class Meta:
        model = PersonalLoan
        fields = [
            'name', 'email', 'phone', 'state',
            'loan_amount', 'loan_term', 'loan_purpose',
            'employment_status', 'annual_income', 'credit_score',
            'loan_description', 'monthly_payment', 'interest_rate', 'apr'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': "What's your name?",
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': "What's your email?",
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': "(123) 480 - 3540",
                'required': True
            }),
            'state': forms.TextInput(attrs={
                'placeholder': "California",
                'required': True
            }),
            'loan_amount': forms.TextInput(attrs={
                'placeholder': "Ex. $8,000 USD",
                'required': True
            }),
            'loan_term': forms.TextInput(attrs={
                'placeholder': "Ex. 12 Months",
                'required': True
            }),
            'loan_purpose': forms.Select(attrs={
                'class': 'form-select'
            }),
            'employment_status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'annual_income': forms.TextInput(attrs={
                'placeholder': "Ex. $50,000"
            }),
            'credit_score': forms.Select(attrs={
                'class': 'form-select'
            }),
            'loan_description': forms.Textarea(attrs={
                'placeholder': "Briefly describe what you need the loan for...",
                'rows': 3
            }),
            'monthly_payment': forms.HiddenInput(),
            'interest_rate': forms.HiddenInput(),
            'apr': forms.HiddenInput(),
        }
        labels = {
            'loan_purpose': 'What will you use the loan for?',
            'employment_status': 'Current Employment Status',
            'annual_income': 'Annual Income (optional)',
            'credit_score': 'Credit Score Range (optional)',
            'loan_description': 'Additional Information',
        }