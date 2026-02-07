from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from secondapp.models import Plot

def home(request):
    recent_plots = Plot.objects.prefetch_related('images').order_by('-created_at')
    context = {
        'plots': recent_plots
    }
    return render(request, 'index.html', context)

def properties(request):
    all_plots = Plot.objects.prefetch_related('images').order_by('-created_at')
    context = {
        'plots': all_plots
    }
    response = render(request, 'properties.html', context)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

def property_single(request, plot_id):
    from django.http import Http404
    try:
        plot = Plot.objects.prefetch_related('images').get(id=plot_id)
    except Plot.DoesNotExist:
        raise Http404("Plot not found")

    plan = 'none'
    can_view_fully = False
    can_sell = False

    if request.user.is_authenticated:
        plan = getattr(request.user, 'plan', 'none') or 'none'

        if plan == 'free':
            free_expires_at = getattr(request.user, 'free_expires_at', None)
            if not free_expires_at or free_expires_at < timezone.now():
                plan = 'none'

        if plan == 'premium':
            can_view_fully = True
            can_sell = True
        elif plan == 'basic':
            can_sell = True
            allowed_ids = list(
                Plot.objects.order_by('created_at').values_list('id', flat=True)[:5]
            )
            can_view_fully = plot.id in allowed_ids
        elif plan == 'free':
            can_view_fully = True

    context = {
        'plot': plot,
        'plan': plan,
        'can_view_fully': can_view_fully,
        'can_sell': can_sell,
    }
    return render(request, 'properties-single.html', context)

def single(request):
	return render(request, 'single.html')

def signup(request):
	
	if request.user.is_authenticated:
		return redirect('home')
	
	if request.method == 'POST':
		username = request.POST.get('username', '').strip()
		email = request.POST.get('email', '').strip()
		phone = request.POST.get('phone', '').strip()
		address = request.POST.get('address', '').strip()
		profile_picture = request.FILES.get('profile_picture')
		password1 = request.POST.get('password1', '')
		password2 = request.POST.get('password2', '')

		if not username or not password1 or not password2:
			messages.error(request, 'Please fill in all required fields.')
			return redirect('signup')
		if password1 != password2:
			messages.error(request, 'Passwords do not match.')
			return redirect('signup')
		User = get_user_model()
		if User.objects.filter(username=username).exists():
			messages.error(request, 'Username already taken.')
			return redirect('signup')
		if email and User.objects.filter(email=email).exists():
			messages.error(request, 'Email already registered.')
			return redirect('signup')

		user = User.objects.create_user(
			username=username,
			email=email or None,
			password=password1,
			phone=phone or '',
			address=address or '',
		)
		login(request, user)
		messages.success(request, 'Account created successfully.')
		return redirect('myapp:home')

	return render(request, 'signup.html')

def signin(request):
	
	if request.user.is_authenticated:
		return redirect('home')
	
	if request.method == 'POST':
		username = request.POST.get('username', '').strip()
		password = request.POST.get('password', '')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, 'Signed in successfully.')
			return redirect('myapp:home')
		messages.error(request, 'Invalid username or password.')
		return redirect('signin')

	return render(request, 'signin.html')

def signout(request):
	logout(request)
	messages.success(request, 'Signed out successfully.')
	return redirect('myapp:home')

@login_required(login_url='signin')
def profile(request):
	user = request.user
	User = get_user_model()

	if request.method == 'POST':
		username = request.POST.get('username', '').strip()
		email = request.POST.get('email', '').strip()
		phone = request.POST.get('phone', '').strip()
		address = request.POST.get('address', '').strip()
		profile_picture = request.FILES.get('profile_picture')
		password1 = request.POST.get('password1', '')
		password2 = request.POST.get('password2', '')

		has_error = False

		if not username:
			messages.error(request, 'Username is required.')
			has_error = True
		elif User.objects.filter(username=username).exclude(pk=user.pk).exists():
			messages.error(request, 'Username already taken.')
			has_error = True

		if email and User.objects.filter(email=email).exclude(pk=user.pk).exists():
			messages.error(request, 'Email already registered.')
			has_error = True

		if password1 or password2:
			if password1 != password2:
				messages.error(request, 'Passwords do not match.')
				has_error = True
			elif len(password1) < 6:
				messages.error(request, 'Password must be at least 6 characters long.')
				has_error = True

		if has_error:
			return redirect('myapp:profile')

		user.username = username
		user.email = email or ''
		user.phone = phone
		user.address = address
		if profile_picture:
			user.profile_picture = profile_picture

		password_changed = False
		if password1:
			user.set_password(password1)
			password_changed = True

		user.save()

		if password_changed:
			update_session_auth_hash(request, user)

		messages.success(request, 'Profile updated successfully.')
		return redirect('myapp:profile')

	# GET request: just render profile page
	return render(request, 'profile.html')


@login_required(login_url='signin')
def subscription(request):
	user = request.user

	if request.method == 'POST':
		selected_plan = request.POST.get('plan')

		if selected_plan == 'free':
			user.plan = 'free'
			user.free_expires_at = timezone.now() + timedelta(days=1)
			user.save()
			messages.success(
				request,
				'Free plan activated. You have unlimited access to all properties for 1 day.'
			)
			return redirect('myapp:subscription')

		if selected_plan in ('basic', 'premium'):
			user.plan = selected_plan
			user.free_expires_at = None
			user.save()
			if selected_plan == 'basic':
				msg = 'Basic plan selected. You can view details of 5 properties and sell properties.'
			else:
				msg = 'Premium plan selected. You have unlimited access and can sell properties.'
			messages.success(request, msg)
			return redirect('myapp:subscription')

	current_plan = getattr(user, 'plan', 'none') or 'none'
	free_expires_at = getattr(user, 'free_expires_at', None)

	context = {
		'current_plan': current_plan,
		'free_expires_at': free_expires_at,
	}
	return render(request, 'subscription.html', context)

	return render(request, 'profile.html')

