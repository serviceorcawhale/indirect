from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q
from .forms import UserRegistrationForm, UserLoginForm, SetPasswordForm, PasswordResetForm, BusinessLoanForm, CarLoanForm, EducationLoanForm, HomeLoanForm, PersonalLoanForm
from .decorators import user_not_authenticated
from .tokens import account_activation_token
from .models import *
from .forms import *
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
import threading
import random
import string
from datetime import datetime, timedelta

# Create your views here.
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('login')



def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("bank/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear  {user} , please go to you email {to_email}  inbox and click on \
                received activation link to confirm and complete the registration.  Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

def template_activate_account(request):
    context = {}
    return render (request, "bank/template-activate-account.html", context)

def home( request):
    return render (request, 'bank/home.html') 

def about( request):
    return render (request, 'bank/about.html') 


def contact( request):
    return render (request, 'bank/contact.html') 

def account_details( request):
    return render (request, 'bank/account-details.html') 

def account( request):
    return render (request, 'bank/account.html') 

@login_required (login_url = "login")
def bill( request):
    return render (request, 'bank/bill.html') 

@login_required(login_url="login")
def business_loan(request):
    if request.method == 'POST':
        form = BusinessLoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.user = request.user if request.user.is_authenticated else None
            loan.save()
            messages.success(request, "Your business loan application has been submitted successfully!")
            return redirect('business-loan')
    else:
        form = BusinessLoanForm()
    
    return render(request, 'bank/business-loan.html', {'form': form}) 

@login_required(login_url="login")
def car_loan(request):
    if request.method == 'POST':
        form = CarLoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.user = request.user if request.user.is_authenticated else None
            loan.save()
            messages.success(request, "Your car loan application has been submitted successfully!")
            return redirect('car-loan')
    else:
        form = CarLoanForm()
    
    return render(request, 'bank/car-loan.html', {'form': form}) 

def card( request):
    return render (request, 'bank/card.html') 

@login_required (login_url = "login")
def cards( request):
    card = request.user.card
    form = CardForm (instance = card)

    if request.method == 'POST':
        form = CardForm (request.POST, request.FILES, instance = card)
        if form.is_valid ():
            form.save ()

    context = {'form': form}
    return render (request, 'bank/cards.html', context) 

def career_single( request):
    return render (request, 'bank/career-single.html') 

 
@login_required (login_url = "login")
def change_password( request):
    return render (request, 'bank/change-password.html') 

@login_required (login_url = "login")
def generate_bulk_transfers(request):
    if request.method == "POST":
        try:
            num = int(request.POST.get("count", 1))
            if num < 1 or num > 300:
                messages.error(request, "Please enter a number between 1 and 200.")
                return redirect('generate_bulk_transfers')
        except ValueError:
            messages.error(request, "Invalid number entered.")
            return redirect('generate_bulk_transfers')

        # Get start and end date from form
        start_date_str = request.POST.get("start_date")
        end_date_str = request.POST.get("end_date")

        if not start_date_str or not end_date_str:
            messages.error(request, "Please select both start and end dates.")
            return redirect('generate_bulk_transfers')

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
            return redirect('generate_bulk_transfers')

        if start_date > end_date:
            messages.error(request, "Start date cannot be after end date.")
            return redirect('generate_bulk_transfers')

        # U.S. Banks only
        BANKS = [
            'Bank of America', 'Wells Fargo', 'Chase Bank', 'Citibank',
            'U.S. Bank', 'Capital One', 'PNC Bank', 'TD Bank',
            'Goldman Sachs', 'Morgan Stanley', 'Ally Bank', 'Discover Bank'
        ]
        STATUS = ['Pending', 'Completed']
        GATEWAYS = ['PayPal', 'Wise', 'CashApp', 'Bank']

        # Generate transfers
        for i in range(num):
            random_ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            random_wallet = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            random_days = random.randint(0, (end_date - start_date).days)
            random_date = start_date + timedelta(days=random_days)

            Transfer.objects.create(
                user=request.user,
                name=f"Transfer {i+1}",
                swift_code=f"US{random.randint(1000,9999)}",
                first_name=request.user.first_name or "John",
                last_name=request.user.last_name or "Doe",
                bank_name=random.choice(BANKS),
                account_number=str(random.randint(1000000000, 9999999999)),
                amount=str(random.randint(1000, 50000)),
                wallet=random_wallet,
                paypal_address=f"user{i+1}@example.com",
                wise_address=f"user{i+1}@wise.com",
                cashapp=f"${request.user.username or 'user'}{i+1}",
                date=random_date.strftime("%Y-%m-%d"),
                reference=random_ref,
                gateway=random.choice(GATEWAYS),
                status=random.choice(STATUS),
            )

        messages.success(request, f"{num} transfers generated between {start_date_str} and {end_date_str}!")
        return redirect('transaction-history')

    return render(request, 'bank/generate_bulk_transfers.html')


    
@login_required (login_url = "login")
def coin_details( request):
    return render (request, 'bank/coin-details.html') 

@login_required (login_url = "login")
def pin_validation( request):
    pin = request.user.pin
    form = PinForm (instance = pin)

    if request.method == 'POST':
        form = PinForm (request.POST, request.FILES, instance = pin)
        if form.is_valid ():
            form.save ()

    context = {'form': form}
    return render (request, 'bank/pin-validation.html', context) 

@login_required (login_url = "login")
def crypto_send( request):
    return render (request, 'bank/crypto-send.html') 

@login_required (login_url = "login")
def crypto_transaction( request):
    return render (request, 'bank/crypto-transaction.html') 

@login_required (login_url = "login")
def crypto_view_transaction( request):
    return render (request, 'bank/crypto-view-transaction.html') 

@login_required (login_url = "login")
def crypto_withdraw( request):
    return render (request, 'bank/crypto-withdraw.html') 

@login_required (login_url = "login")
def crypto( request):
    return render (request, 'bank/crypto.html') 

@login_required (login_url = "login")
def dashboard( request):
    return render (request, 'bank/dashboard.html') 

@login_required(login_url="login")
def educations_loan(request):
    if request.method == 'POST':
        form = EducationLoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.user = request.user if request.user.is_authenticated else None
            loan.save()
            messages.success(request, "Your education loan application has been submitted successfully!")
            return redirect('educations-loan')
    else:
        form = EducationLoanForm()
    
    return render(request, 'bank/educations-loan.html', {'form': form}) 

@login_required (login_url = "login")
def forgot_password( request):
    return render (request, 'bank/forgot-password.html') 

@login_required (login_url = "login")
def help( request):
    return render (request, 'bank/help.html') 

@login_required(login_url="login")
def home_loan(request):
    if request.method == 'POST':
        form = HomeLoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.user = request.user if request.user.is_authenticated else None
            loan.save()
            messages.success(request, "Your home loan application has been submitted successfully!")
            return redirect('home-loan')
    else:
        form = HomeLoanForm()
    
    return render(request, 'bank/home-loan.html', {'form': form}) 

def home( request):
    return render (request, 'bank/home.html') 

def insight( request):
    return render (request, 'bank/insight.html') 

@login_required (login_url = "login")
def make_payment( request):
    return render (request, 'bank/make-payment.html') 

@login_required (login_url = "login")
def my_account( request):
    profile = request.user.profile
    form = ProfileForm (instance = profile)

    if request.method == 'POST':
        form = ProfileForm (request.POST, request.FILES, instance = profile)
        if form.is_valid ():
            form.save ()

    context = {'form': form}
    return render (request, 'bank/my-account.html', context)

@login_required (login_url = "login")
def my_portfolio( request):
    return render (request, 'bank/my-portfolio.html') 

@login_required (login_url = "login")
def news_update_details( request):
    return render (request, 'bank/news-update-details.html') 

@login_required (login_url = "login")
def news_update( request):
    return render (request, 'bank/news-update.html') 

@login_required (login_url = "login")
def notification( request):
    return render (request, 'bank/notification.html') 

@login_required (login_url = "login")
def otp( request):
    return render (request, 'bank/otp.html') 

@login_required (login_url = "login")
def pay_successfully( request):
    return render (request, 'bank/pay-successfully.html') 


def personal_identity( request):

    return render (request, 'bank/personal-identity.html') 


@login_required(login_url="login")
def personal_loan(request):
    if request.method == 'POST':
        form = PersonalLoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.user = request.user if request.user.is_authenticated else None
            loan.save()
            messages.success(request, "Your personal loan application has been submitted successfully!")
            return redirect('personal-loan')
    else:
        form = PersonalLoanForm()
    
    return render(request, 'bank/personal-loan.html', {'form': form}) 

def preloader( request):
    return render (request, 'bank/preloader.html') 

def privacy_policy( request):
    return render (request, 'bank/privacy-policy.html') 

def product( request):
    return render (request, 'bank/product.html') 

@login_required (login_url = "login")
def profile( request):
    return render (request, 'bank/profile.html') 

@user_not_authenticated
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=True
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('login')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request=request,
        template_name="bank/register.html",
        context={"form": form}
        )


@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("dashboard")

@user_not_authenticated
def custom_login(request):
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                return redirect("signin-successfully")

        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test")
                    continue
                
                messages.error(request, error) 

    form = UserLoginForm()

    return render(
        request=request,
        template_name="bank/login.html",
        context={"form": form}
        )

@login_required (login_url = "login")
def reset_password( request):
    return render (request, 'bank/reset-password.html') 

def secure( request):
    return render (request, 'bank/secure.html') 


def service( request):
    return render (request, 'bank/service.html') 

@login_required (login_url = "login")
def setting( request):
    return render (request, 'bank/setting.html') 

@login_required (login_url = "login")
def signin_successfully( request):
    return render (request, 'bank/signin-successfully.html') 

@login_required (login_url = "login")
def successfully_signin( request):
    return render (request, 'bank/successfully-signin.html') 

@login_required (login_url = "login")
def successfully_signup( request):
    return render (request, 'bank/successfully-signup.html') 

def terms_conditions( request):
    return render (request, 'bank/terms-conditions.html') 

@login_required (login_url = "login")
def transaction_history( request):
    user = request.user

    transfer = Transfer.objects.filter(user=user)

    context = {'transfer':transfer}
    return render (request, 'bank/transaction-history.html', context) 

@login_required(login_url="login")
def send_withdrawal_email(user, amount, gateway, reference, date):
    """Send withdrawal processing email after 2 minutes."""
    subject = "Withdrawal Request Received"
    message = (
        f"Dear {user.username},\n\n"
        f"Your withdrawal request of {amount} via {gateway} has been received and is currently being processed.\n"
        f"Reference ID: {reference}\n"
        f"Date: {date}\n\n"
        "You will receive another email once the transaction is completed.\n\n"
        "Thank you for choosing our services.\n\n"
        "— mPay Support Team"
    )
    from_email = "service.hsbcredex@gmail.com"
    recipient_list = [user.email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)
    except Exception:
        pass


@login_required(login_url="login")
def transfer(request):
    user = request.user

    # Use related_name='transfers' in model if defined; else keep transfer_set
    transfer_records = getattr(user, "transfer_set").all()

    if request.method == "POST":
        name = request.POST.get("name")
        swift_code = request.POST.get("swift_code")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        amount = request.POST.get("amount")
        wallet = request.POST.get("wallet")
        paypal_address = request.POST.get("paypal_address")
        wise_address = request.POST.get("wise_address")
        cashapp = request.POST.get("cashapp")
        date = request.POST.get("date")
        reference = request.POST.get("reference")
        gateway = request.POST.get("gateway")
        bank_name = request.POST.get("bank_name")
        account_number = request.POST.get("account_number")
        status = request.POST.get("status", "Pending")

        # Save or create new transfer record
        transfer, created = Transfer.objects.get_or_create(
            user=user,
            name=name,
            swift_code=swift_code,
            first_name=first_name,
            last_name=last_name,
            amount=amount,
            wallet=wallet,
            paypal_address=paypal_address,
            wise_address=wise_address,
            cashapp=cashapp,
            date=date,
            reference=reference,
            gateway=gateway,
            bank_name=bank_name,
            account_number=account_number,
            status=status,
        )

        # 🕒 Delay email sending by 2 minutes (120 seconds)
        threading.Timer(120, send_withdrawal_email, args=[user, amount, gateway, reference, date]).start()

        messages.success(request, "Withdrawal request submitted. Confirmation email will be sent shortly.")
        return redirect("pin")

    context = {"transfer": transfer_records}
    return render(request, "bank/transfer.html", context)

@login_required (login_url = "login")
def withdraw( request):
    withdraw = request.user.withdraw
    form = WithdrawForm (instance = withdraw)

    if request.method == 'POST':
        form = WithdrawForm (request.POST, request.FILES, instance = withdraw)
        if form.is_valid ():
            form.save ()

    context = {'form': form}
    return render (request, 'bank/withdraw.html', context) 

@login_required (login_url = "index")
def viewSuccess(request, pk):
    transfer = Transfer.objects.get(id=pk)
    return render (request, "bank/success.html", {'transfer': transfer})

@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'bank/change-password.html', {'form': form})


@user_not_authenticated
def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("bank/template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        <h2>Password reset sent</h2><hr>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        </p>
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('login')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="bank/reset-password.html", 
        context={"form": form}
        )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'bank/change-password.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("login")


@login_required (login_url = "login")
def pin(request):
    context = {}
    return render (request, "bank/pin.html", context)


@login_required (login_url = "login")
def deposit(request):
    context = {}
    return render (request, "bank/deposit.html", context)