"""
User Views Module
This module contains view functions for user-related actions.
"""
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserSignupForm, ProfileSignupForm, UserEditForm, ProfileEditForm
from .models import Profile

blog_list = [
    {
        'heading': 'Thought you loved Python? Wait until you meet Rust',
        'date': 'Apr. 14th, 2022',
        'headerimage': 'img_1_horizontal.jpg',
        'description': 'Lorem ipsum dolor sit amet consectetur adipisicing '
                       'elit. Unde, nobis ea quis '
                       'inventore vel voluptas.',
        'topic': 'Business'
    },
    {
        'heading': 'Thought you loved Python? Wait until you meet Rust',
        'date': 'Apr. 14th, 2022',
        'headerimage': 'img_2_horizontal.jpg',
        'description': 'Lorem ipsum dolor sit amet consectetur '
                       'adipisicing elit. Unde, nobis ea quis '
                       'inventore vel voluptas.',
        'topic': 'Business'
    },
    {
        'heading': 'Thought you loved Python? Wait until you meet Rust',
        'date': 'Apr. 14th, 2022',
        'headerimage': 'img_3_horizontal.jpg',
        'description': 'Lorem ipsum dolor sit amet consectetur '
                       'adipisicing elit. Unde, nobis ea quis '
                       'inventore vel voluptas.',
        'topic': 'Business'
    },
    {
        'heading': 'Thought you loved Python? Wait until you meet Rust',
        'date': 'Apr. 14th, 2022',
        'headerimage': 'img_4_horizontal.jpg',
        'description': 'Lorem ipsum dolor sit amet consectetur '
                       'adipisicing elit. Unde, nobis ea quis '
                       'inventore vel voluptas.',
        'topic': 'Business'
    },
    {
        'heading': 'Thought you loved Python? Wait until you meet Rust',
        'date': 'Apr. 14th, 2022',
        'headerimage': 'img_5_horizontal.jpg',
        'description': 'Lorem ipsum dolor sit amet consectetur '
                       'adipisicing elit. Unde, nobis ea quis '
                       'inventore vel voluptas.',
        'topic': 'Business'
    },
    {
        'heading': 'Thought you loved Python? Wait until you meet Rust',
        'date': 'Apr. 14th, 2022',
        'headerimage': 'img_7_horizontal.jpg',
        'description': 'Lorem ipsum dolor sit amet consectetur '
                       'adipisicing elit. Unde, nobis ea quis '
                       'inventore vel voluptas.',
        'topic': 'Business'
    },
]


def index_view(request):
    """
    Render the home page with a list of featured blogs.
    """
    return render(request, "blogs/home.html",
                  {"blog_list": blog_list[:6], "home_featured_blogs": blog_list[:5]})


def login_view(request):
    """
    Handle user login.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The login page or redirects to home page after successful login.
    """
    if request.method == 'POST':
        data = {
            'email': request.POST.get('email'),
            'password': request.POST.get('password')
        }
        form = UserLoginForm(data)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            return render(request, 'registration/login.html',
                          {'login_form_errors':
                               {'Error while logging in: Invalid Credentials!'}})
        return render(request, 'registration/login.html', {'login_form_errors': form.errors})

    return render(request, 'registration/login.html')


def signup_view(request):
    """
    Handle user signup.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to login page or displays signup errors.
    """
    form_errors = {}
    if request.method == 'POST':
        user_data = {
            'first_name': request.POST.get('f_name'),
            'last_name': request.POST.get('l_name'),
            'email': request.POST.get('new_email'),
            'password1': request.POST.get('pass1'),
            'password2': request.POST.get('pass2'),
        }
        profile_data = {
            'user_bio': request.POST.get('bio'),
        }
        user_form = UserSignupForm(user_data)
        profile_form = ProfileSignupForm(profile_data)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            profile = Profile.objects.get(user_id=user)     # pylint: disable=no-member
            profile.user = user
            profile.user_bio = profile_form.cleaned_data['user_bio']
            profile.save()

            login(request, user)
            return redirect('home')
        form_errors.update(user_form.errors)
        form_errors.update(profile_form.errors)
        return render(request, 'registration/login.html', {'signup_form_errors': form_errors})

    return redirect('login')


def edit_profile_view(request):
    """
    Handle user profile editing.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The profile editing page or displays form errors after editing.
    """
    if request.method == "POST":
        form_errors = {}
        user_data = {
            'first_name': request.POST.get('input-first-name'),
            'last_name': request.POST.get('input-last-name'),
        }
        profile_data = {
            'user_bio': request.POST.get('user-bio-input'),
        }
        user_form = UserEditForm(user_data, instance=request.user)
        profile_form = ProfileEditForm(profile_data)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = Profile.objects.get(user_id=user)     # pylint: disable=no-member
            profile.user_bio = profile_form.cleaned_data['user_bio']
            profile.save()
            return redirect('edit_profile')
        form_errors.update(user_form.errors)
        form_errors.update(profile_form.errors)
        return render(request, 'users/edit_profile.html', {'form_errors': form_errors})

    return render(request, "users/edit_profile.html")


def edit_dp_view(request):
    """
    Handle user profile picture update.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the profile editing page or displays errors.
    """
    if request.method == "POST":
        user = request.user
        if 'user_dp' in request.FILES:
            user.profile.user_dp = request.FILES['user_dp']
            user.save()
        else:
            messages = {"No File Was Selected!"}

            return render(request, "users/edit_profile.html", {'messages': messages})

    return redirect('edit_profile')
