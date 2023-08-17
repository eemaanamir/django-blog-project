from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserSignupForm, ProfileSignupForm, UserEditForm, ProfileEditForm
from .models import Profile

blog_list = [
    {
        'heading': 'Thought you loved Python? Wait until you meet Rust',
        'date': 'Apr. 14th, 2022',
        'headerimage': 'img_1_horizontal.jpg',
        'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Unde, nobis ea quis '
                       'inventore vel voluptas.',
        'topic': 'Business'
    },
    {
        'heading': 'Thought you loved Python? Wait until you meet Rust',
        'date': 'Apr. 14th, 2022',
        'headerimage': 'img_2_horizontal.jpg',
        'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Unde, nobis ea quis '
                       'inventore vel voluptas.',
        'topic': 'Business'
    },
    {
        'heading': 'Thought you loved Python? Wait until you meet Rust',
        'date': 'Apr. 14th, 2022',
        'headerimage': 'img_3_horizontal.jpg',
        'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Unde, nobis ea quis '
                       'inventore vel voluptas.',
        'topic': 'Business'
    },
    {
        'heading': 'Thought you loved Python? Wait until you meet Rust',
        'date': 'Apr. 14th, 2022',
        'headerimage': 'img_4_horizontal.jpg',
        'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Unde, nobis ea quis '
                       'inventore vel voluptas.',
        'topic': 'Business'
    },
    {
        'heading': 'Thought you loved Python? Wait until you meet Rust',
        'date': 'Apr. 14th, 2022',
        'headerimage': 'img_5_horizontal.jpg',
        'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Unde, nobis ea quis '
                       'inventore vel voluptas.',
        'topic': 'Business'
    },
    {
        'heading': 'Thought you loved Python? Wait until you meet Rust',
        'date': 'Apr. 14th, 2022',
        'headerimage': 'img_7_horizontal.jpg',
        'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Unde, nobis ea quis '
                       'inventore vel voluptas.',
        'topic': 'Business'
    },
]

blog = {
    'heading': 'Don’t assume your user data in the cloud is safe',
    'headerimage': 'hero_5.jpg',
    'author': 'Carl Atkinson',
    'authorimage': 'person_5.jpg',
    'date': 'February 10, 2019',
    'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Unde, nobis ea quis inventore vel voluptas.',
    'body': 'Quibusdam autem, quas molestias recusandae aperiam molestiae modi qui ipsam vel. Placeat tenetur veritatis tempore quos impedit dicta, error autem, quae sint inventore ipsa quidem. Quo voluptate quisquam reiciendis, minus, animi minima eum officia doloremque repellat eos, odio doloribus cum.\
                Temporibus quo dolore veritatis doloribus delectus dolores perspiciatis recusandae ducimus, nisi quod, incidunt ut quaerat, magnam cupiditate. Aut, laboriosam magnam, nobis dolore fugiat impedit necessitatibus nisi cupiditate, quas repellat itaque molestias sit libero voluptas eveniet omnis illo ullam dolorem minima.\
                Porro amet accusantium libero fugit totam, deserunt ipsa, dolorem, vero expedita illo similique saepe nisi deleniti. Cumque, laboriosam, porro! Facilis voluptatem sequi nulla quidem, provident eius quos pariatur maxime sapiente illo nostrum quibusdam aliquid fugiat! Earum quod fuga id officia.\
                Illo magnam at dolore ad enim fugiat ut maxime facilis autem, nulla cumque quis commodi eos nisi unde soluta, ipsa eius aspernatur sint atque! Nihil, eveniet illo ea, mollitia fuga accusamus dolor dolorem perspiciatis rerum hic, consectetur error rem aspernatur!\
                Lorem ipsum dolor sit amet, consectetur adipisicing elit. Temporibus magni explicabo id molestiae, minima quas assumenda consectetur, nobis neque rem, incidunt quam tempore perferendis provident obcaecati sapiente, animi vel expedita omnis quae ipsa! Obcaecati eligendi sed odio labore vero reiciendis facere accusamus molestias eaque impedit, consequuntur quae fuga vitae fugit?',
    'topic': 'Business',
    'type': 'Premium'
}
comment_list = [
    {
        'author': 'Jean Doe',
        'authorimage': 'person_1.jpg',
        'date': 'January 9, 2018',
        'time': '2:21pm',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Pariatur quidem laborum necessitatibus, ipsam impedit vitae autem, eum officia, fugiat saepe enim sapiente iste iure! Quam voluptas earum impedit necessitatibus, nihil',
    },
    {
        'author': 'John Doe',
        'authorimage': 'person_2.jpg',
        'date': 'January 9, 2018',
        'time': '2:21pm',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Pariatur quidem laborum necessitatibus, ipsam impedit vitae autem, eum officia, fugiat saepe enim sapiente iste iure! Quam voluptas earum impedit necessitatibus, nihil',
    },
    {
        'author': 'Jean Doe',
        'authorimage': 'person_5.jpg',
        'date': 'January 9, 2018',
        'time': '2:21pm',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Pariatur quidem laborum necessitatibus, ipsam impedit vitae autem, eum officia, fugiat saepe enim sapiente iste iure! Quam voluptas earum impedit necessitatibus, nihil',
    }

]
author = {
    'name': 'Hannah Anderson',
    'fname': 'Hannah',
    'lname': 'Anderson',
    'image': 'person_5.jpg',
    'bio': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Exercitationem facilis sunt repellendus excepturi beatae porro debitis voluptate nulla quo veniam fuga sit molestias minus.',
    'blog_count': '41',
    'likes': '8.9k',
    'followers': '976',
    'user_type': 'Premium User',
    'email': 'hannah.anderson@123.com',
}


def index_view(request):
    return render(request, "blogs/home.html",
                  {"blog_list": blog_list[:6], "home_featured_blogs": blog_list[:5]})


def login_view(request):
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
            else:
                return render(request,'registration/login.html',{'login_form_errors': {'Error while logging in: Invalid Credentials!'}})
        else:
            return render(request, 'registration/login.html', {'login_form_errors': form.errors})

    return render(request, 'registration/login.html')


def signup_view(request):
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

            profile = Profile.objects.get(user_id=user)
            profile.user = user
            profile.user_bio = profile_form.cleaned_data['user_bio']
            profile.save()

            login(request, user)
            return redirect('home')
        else:
            form_errors.update(user_form.errors)
            form_errors.update(profile_form.errors)
            return render(request, 'registration/login.html', {'signup_form_errors': form_errors})

    return redirect('login')


def edit_profile_view(request):
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
            profile = Profile.objects.get(user_id=user)
            profile.user_bio = profile_form.cleaned_data['user_bio']
            profile.save()
        else:
            form_errors.update(user_form.errors)
            form_errors.update(profile_form.errors)
            return render(request, 'users/edit_profile.html', {'form_errors': form_errors})

    return render(request, "users/edit_profile.html")


def edit_dp_view(request):
    if request.method == "POST":
        user = request.user
        if 'user_dp' in request.FILES:
            user.profile.user_dp = request.FILES['user_dp']
            user.save()
        else:
            messages = {"No File Was Selected!"}

            return render(request, "users/edit_profile.html", {'messages': messages})

    return redirect('edit_profile')
