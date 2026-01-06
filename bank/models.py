from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.db import models



class Profile (models.Model):
    user = models.OneToOneField (User, null = True, blank = True, on_delete = models.CASCADE)
    name = models.CharField (max_length = 200,  null = True)
    address = models.CharField (max_length = 200,  null = True)
    zip_code = models.CharField (max_length = 200, null = True)
    phone_number = models.CharField (max_length = 200, null = True)
    country = models.CharField (max_length = 200, null = True)
    gender = models.CharField (max_length = 200, null = True)
    date_of_birth = models.CharField (max_length = 200, null = True)
    home_address = models.CharField (max_length = 200, null = True)
    occupation = models.CharField (max_length = 200, null = True)
    annual_income_range = models.CharField (max_length = 200, null = True)
    pin = models.CharField (max_length = 200, null = True)
    profile_pic = models.ImageField (default = "avater.png", null = True, blank = True)


    def __str__(self):
        return str(self.name)


class Deposit (models.Model):
    user = models.OneToOneField (User, null = True, blank = True, on_delete = models.CASCADE)
    name = models.CharField (max_length = 200,  null = True)
    main_balance = models.CharField (max_length = 200,  null = True, default = "0",)
    main_income = models.CharField (max_length = 200, null = True, default = "0",)
    main_expense = models.CharField (max_length = 200, null = True, default = "0",)
    crypto_balance = models.CharField (max_length = 200, null = True, default = "0",)
    crypto_income = models.CharField (max_length = 200, null = True,default = "0",)
    crypto_expense = models.CharField (max_length = 200, null = True, default = "0",)
    currency = models.CharField (max_length = 200, null = True, default = "$",)

    def __str__(self):
        return str(self.name)

class Card (models.Model):
    user = models.OneToOneField (User, null = True, blank = True, on_delete = models.CASCADE)
    name = models.CharField (max_length = 200,  null = True)
    card_type = models.CharField (max_length = 200,  null = True, default = "0",)
    card_number = models.CharField (max_length = 200, null = True, default = "**** **** **** 2563",)
    exp_date = models.CharField (max_length = 200, null = True, default = "12/24",)
    cvv = models.CharField (max_length = 200, null = True, default = "***",)

    def __str__(self):
        return str(self.name)

class Accountnumber (models.Model):
    user = models.OneToOneField (User, null = True, blank = True, on_delete = models.CASCADE)
    name = models.CharField (max_length = 200,  null = True)
    account_number = models.CharField (max_length = 200,  null = True, default = "Generating Account Number...",)


    def __str__(self):
        return str(self.name)


class Transfer(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    swift_code = models.CharField(max_length=200, null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    bank_name = models.CharField(max_length=200, null=True)
    account_number = models.CharField(max_length=200, null=True)
    amount = models.CharField(max_length=200, null=True)
    wallet = models.CharField(max_length=200, null=True)
    paypal_address = models.CharField(max_length=200, null=True)
    wise_address = models.CharField(max_length=200, null=True)
    cashapp = models.CharField(max_length=200, null=True)
    date = models.CharField(max_length=200, null=True)
    reference = models.CharField(max_length=200, null=True)
    gateway = models.CharField(max_length=200, null=True)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Pending',
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.name)



class Withdraw (models.Model):
    user = models.OneToOneField (User, null = True, blank = True, on_delete = models.CASCADE)
    name = models.CharField (max_length = 200,  null = True)
    bank = models.CharField (max_length = 200,  null = True, )
    account_number = models.CharField (max_length = 200,  null = True)
    amount = models.CharField (max_length = 200,  null = True)
    status = models.CharField (max_length = 200,  null = True, default = "Pending", )


    def __str__(self):
        return str(self.name)


class Pin (models.Model):
    user = models.OneToOneField (User, null = True, blank = True, on_delete = models.CASCADE)
    name = models.CharField (max_length = 200,  null = True)
    pin = models.CharField (max_length = 200, null = True, default = "0000")


    def __str__(self):
        return str(self.name)



class BusinessLoan(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    loan_amount = models.CharField(max_length=50)
    loan_term = models.CharField(max_length=50)
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Business Loan - {self.name} - {self.loan_amount}"

class CarLoan(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    loan_amount = models.CharField(max_length=50)
    loan_term = models.CharField(max_length=50)
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Car Loan - {self.name} - {self.loan_amount}"

class EducationLoan(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    loan_amount = models.CharField(max_length=50)
    loan_term = models.CharField(max_length=50)
    country = models.CharField(max_length=100, blank=True, null=True)
    college_name = models.CharField(max_length=200, blank=True, null=True)
    gre_score = models.CharField(max_length=10, blank=True, null=True)
    gmat_score = models.CharField(max_length=10, blank=True, null=True)
    full_time_study = models.CharField(max_length=3, blank=True, null=True)  # Yes/No
    existing_loan = models.CharField(max_length=3, blank=True, null=True)    # Yes/No
    terms_agreed = models.BooleanField(default=False)
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Education Loan - {self.name} - {self.college_name}"

class HomeLoan(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    PROPERTY_TYPE_CHOICES = [
        ('Single Family', 'Single Family Home'),
        ('Condo', 'Condominium'),
        ('Townhouse', 'Townhouse'),
        ('Multi Family', 'Multi-Family'),
        ('Commercial', 'Commercial Property'),
        ('Land', 'Land/Lot'),
    ]
    
    LOAN_PURPOSE_CHOICES = [
        ('Purchase', 'Purchase'),
        ('Refinance', 'Refinance'),
        ('Construction', 'New Construction'),
        ('Renovation', 'Home Renovation'),
        ('Investment', 'Investment Property'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    loan_amount = models.CharField(max_length=50)
    loan_term = models.CharField(max_length=50)
    purchase_price = models.CharField(max_length=50, blank=True, null=True)
    down_payment = models.CharField(max_length=50, blank=True, null=True)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES, blank=True, null=True)
    loan_purpose = models.CharField(max_length=50, choices=LOAN_PURPOSE_CHOICES, blank=True, null=True)
    property_address = models.TextField(blank=True, null=True)
    monthly_payment = models.CharField(max_length=50, blank=True, null=True)
    interest_rate = models.CharField(max_length=20, blank=True, null=True)
    apr = models.CharField(max_length=20, blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Home Loan - {self.name} - {self.property_type}"

class PersonalLoan(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    LOAN_PURPOSE_CHOICES = [
        ('Debt Consolidation', 'Debt Consolidation'),
        ('Home Improvement', 'Home Improvement'),
        ('Medical Expenses', 'Medical Expenses'),
        ('Wedding', 'Wedding'),
        ('Vacation', 'Vacation'),
        ('Education', 'Education'),
        ('Car Purchase', 'Car Purchase'),
        ('Business Startup', 'Business Startup'),
        ('Emergency Funds', 'Emergency Funds'),
        ('Other', 'Other'),
    ]
    
    EMPLOYMENT_CHOICES = [
        ('Employed', 'Employed Full-time'),
        ('Part-time', 'Employed Part-time'),
        ('Self-employed', 'Self-employed'),
        ('Unemployed', 'Unemployed'),
        ('Retired', 'Retired'),
        ('Student', 'Student'),
    ]
    
    CREDIT_SCORE_CHOICES = [
        ('Excellent (720+)', 'Excellent (720+)'),
        ('Good (680-719)', 'Good (680-719)'),
        ('Fair (640-679)', 'Fair (640-679)'),
        ('Poor (639 or less)', 'Poor (639 or less)'),
        ('Not Sure', 'Not Sure'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    loan_amount = models.CharField(max_length=50)
    loan_term = models.CharField(max_length=50)
    loan_purpose = models.CharField(max_length=50, choices=LOAN_PURPOSE_CHOICES, blank=True, null=True)
    employment_status = models.CharField(max_length=50, choices=EMPLOYMENT_CHOICES, blank=True, null=True)
    annual_income = models.CharField(max_length=50, blank=True, null=True)
    credit_score = models.CharField(max_length=50, choices=CREDIT_SCORE_CHOICES, blank=True, null=True)
    loan_description = models.TextField(blank=True, null=True)
    monthly_payment = models.CharField(max_length=50, blank=True, null=True)
    interest_rate = models.CharField(max_length=20, blank=True, null=True)
    apr = models.CharField(max_length=20, blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Personal Loan - {self.name} - {self.loan_purpose}"

