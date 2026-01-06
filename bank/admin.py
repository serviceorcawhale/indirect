from django.contrib import admin
from .models import *

@admin.register(BusinessLoan)
class BusinessLoanAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'loan_amount', 'loan_term', 'status', 'submission_date')
    list_filter = ('status', 'submission_date', 'state')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('submission_date',)

@admin.register(CarLoan)
class CarLoanAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'loan_amount', 'loan_term', 'status', 'submission_date')
    list_filter = ('status', 'submission_date', 'state')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('submission_date',)

@admin.register(EducationLoan)
class EducationLoanAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'college_name', 'loan_amount', 'status', 'submission_date')
    list_filter = ('status', 'submission_date', 'country')
    search_fields = ('name', 'email', 'college_name')
    readonly_fields = ('submission_date',)

@admin.register(HomeLoan)
class HomeLoanAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'loan_amount', 'loan_term', 'status', 'submission_date')
    list_filter = ('status', 'submission_date', 'state')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('submission_date',)

@admin.register(PersonalLoan)
class PersonalLoanAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'loan_amount', 'loan_term', 'status', 'submission_date')
    list_filter = ('status', 'submission_date', 'state')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('submission_date',)

admin.site.register (Profile)
admin.site.register (Deposit)
admin.site.register (Card)
admin.site.register (Accountnumber)
admin.site.register (Transfer)
admin.site.register (Withdraw)
admin.site.register (Pin)