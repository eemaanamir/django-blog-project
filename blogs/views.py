"""
Blog Views Module
This module contains view functions for blog-related actions.
"""
from django.shortcuts import render

blog_list = [
        {
            'heading': 'Thought you loved Python? Wait until you meet Rust',
            'date': 'Apr. 14th, 2022',
            'headerimage': 'img_1_horizontal.jpg',
            'description': 'Lorem ipsum dolor sit amet '
                           'consectetur adipisicing elit. Unde, nobis ea quis '
                           'inventore vel voluptas.',
            'topic': 'Business'
         },
        {
            'heading': 'Thought you loved Python? Wait until you meet Rust',
            'date': 'Apr. 14th, 2022',
            'headerimage': 'img_2_horizontal.jpg',
            'description': 'Lorem ipsum dolor sit amet '
                           'consectetur adipisicing elit. Unde, nobis ea quis '
                           'inventore vel voluptas.',
            'topic': 'Business'
        },
        {
            'heading': 'Thought you loved Python? Wait until you meet Rust',
            'date': 'Apr. 14th, 2022',
            'headerimage': 'img_3_horizontal.jpg',
            'description': 'Lorem ipsum dolor sit amet '
                           'consectetur adipisicing elit. Unde, nobis ea quis '
                           'inventore vel voluptas.',
            'topic': 'Business'
        },
        {
            'heading': 'Thought you loved Python? Wait until you meet Rust',
            'date': 'Apr. 14th, 2022',
            'headerimage': 'img_4_horizontal.jpg',
            'description': 'Lorem ipsum dolor sit amet '
                           'consectetur adipisicing elit. Unde, nobis ea quis '
                           'inventore vel voluptas.',
            'topic': 'Business'
        },
{
            'heading': 'Thought you loved Python? Wait until you meet Rust',
            'date': 'Apr. 14th, 2022',
            'headerimage': 'img_5_horizontal.jpg',
            'description': 'Lorem ipsum dolor sit amet '
                           'consectetur adipisicing elit. Unde, nobis ea quis '
                           'inventore vel voluptas.',
            'topic': 'Business'
        },
{
            'heading': 'Thought you loved Python? Wait until you meet Rust',
            'date': 'Apr. 14th, 2022',
            'headerimage': 'img_7_horizontal.jpg',
            'description': 'Lorem ipsum dolor sit amet '
                           'consectetur adipisicing elit. Unde, nobis ea quis '
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
        'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. '
                       'Unde, nobis ea quis inventore vel voluptas.',
        'body': 'Quibusdam autem, quas molestias recusandae aperiam molestiae '
                'modi qui ipsam vel. Placeat tenetur veritatis tempore quos '
                'impedit dicta, error autem, quae sint inventore ipsa quidem. '
                'Quo voluptate quisquam reiciendis, minus, animi minima eum officia '
                'doloremque repellat eos, odio doloribus cum.\
                Temporibus quo dolore veritatis doloribus delectus dolores '
                'perspiciatis recusandae ducimus, nisi quod, incidunt ut '
                'quaerat, magnam cupiditate. Aut, laboriosam magnam, nobis dolore '
                'fugiat impedit necessitatibus nisi cupiditate, quas repellat itaque '
                'molestias sit libero voluptas eveniet omnis illo ullam dolorem minima.\
                Porro amet accusantium libero fugit totam, deserunt ipsa, dolorem, '
                'vero expedita illo similique saepe nisi deleniti. Cumque, laboriosam,'
                ' porro! Facilis voluptatem sequi nulla quidem, provident eius quos '
                'pariatur maxime sapiente illo nostrum quibusdam aliquid fugiat! '
                'Earum quod fuga id officia.\
                Illo magnam at dolore ad enim fugiat ut maxime facilis autem, nulla '
                'cumque quis commodi eos nisi unde soluta, ipsa eius aspernatur sint '
                'atque! Nihil, eveniet illo ea, mollitia fuga accusamus dolor dolorem '
                'perspiciatis rerum hic, consectetur error rem aspernatur!\
                Lorem ipsum dolor sit amet, consectetur adipisicing elit. Temporibus '
                'magni explicabo id molestiae, minima quas assumenda consectetur, '
                'nobis neque rem, incidunt quam tempore perferendis provident obcaecati '
                'sapiente, animi vel expedita omnis quae ipsa! Obcaecati eligendi sed '
                'odio labore vero reiciendis facere accusamus molestias eaque impedit, '
                'consequuntur quae fuga vitae fugit?',
        'topic': 'Business',
        'type': 'Premium'
            }
comment_list = [
        {
            'author': 'Jean Doe',
            'authorimage': 'person_1.jpg',
            'date': 'January 9, 2018',
            'time': '2:21pm',
            'text': 'Lorem ipsum dolor sit amet, consectetur '
                    'adipisicing elit. Pariatur quidem laborum necessitatibus, '
                    'ipsam impedit vitae autem, eum officia, fugiat saepe enim sapiente '
                    'iste iure! Quam voluptas earum impedit necessitatibus, nihil',
        },
        {
            'author': 'John Doe',
            'authorimage': 'person_2.jpg',
            'date': 'January 9, 2018',
            'time': '2:21pm',
            'text': 'Lorem ipsum dolor sit amet, consectetur '
                    'adipisicing elit. Pariatur quidem laborum necessitatibus, '
                    'ipsam impedit vitae autem, eum officia, fugiat saepe enim '
                    'sapiente iste iure! Quam voluptas earum impedit necessitatibus, nihil',
        },
        {
            'author': 'Jean Doe',
            'authorimage': 'person_5.jpg',
            'date': 'January 9, 2018',
            'time': '2:21pm',
            'text': 'Lorem ipsum dolor sit amet, consectetur '
                    'adipisicing elit. Pariatur quidem laborum necessitatibus, '
                    'ipsam impedit vitae autem, eum officia, fugiat saepe enim '
                    'sapiente iste iure! Quam voluptas earum impedit necessitatibus, nihil',
        }


    ]
author = {
        'name': 'Hannah Anderson',
        'fname': 'Hannah',
        'lname': 'Anderson',
        'image': 'person_5.jpg',
        'bio': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. '
               'Exercitationem facilis sunt repellendus excepturi beatae porro '
               'debitis voluptate nulla quo veniam fuga sit molestias minus.',
        'blog_count': '41',
        'likes': '8.9k',
        'followers': '976',
        'user_type': 'Premium User',
        'email': 'hannah.anderson@123.com',
    }


def blog_list_view(request):
    """
    blog_list_view
    """
    return render(request, "blogs/bloglist.html",
                  {"blog_list": blog_list, "list_heading": 'Subscriptions',
                   "current_user": author, 'featured_blog_list': blog_list[:3]})


def single_blog_view(request, blog_id):
    """
    single_blog_view
    """
    return render(request, "blogs/single.html",
                  {"blog": blog, "comment_list": comment_list,
                   'author': author, 'featured_blog_list': blog_list[:3], "current_user": author})


def user_profile_view(request, user_id):
    """
    user_profile_view
    """
    return render(request, "blogs/user_profile.html",
                  {"blog_list": blog_list[:6], 'user': author, "current_user": author})


def sub_form_view(request):
    """
    sub_form_view
    """
    return render(request, "blogs/subscribe_form.html", {"current_user": author})


def sub_plans_view(request):
    """
    sub_plans_view
    """
    return render(request, "blogs/subscription_plans.html",
                  {"premium_price": 'Rs. 1.5k', "ultra_price": 'Rs. 14k', "current_user": author})


def edit_draft_view(request, draft_id):
    """
    edit_draft_view
    """
    return render(request, "blogs/edit_draft.html", {"current_user": author, "blog": blog})


def list_drafts_and_published(request, list_type):
    """
    list_drafts_and_published
    """
    return render(request, "blogs/my_drafts_and_published_list.html",
                  {"current_user": author, "blog_list": blog_list, "list_heading": list_type.upper})
