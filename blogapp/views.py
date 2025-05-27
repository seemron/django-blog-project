from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import AccessRequest


def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'blogapp/blog_list.html', {'posts': posts})

def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    email = request.session.get('user_email')

    if post.is_private:
        if not email:
            return redirect('request_access')
        has_access = PrivatePostAccess.objects.filter(email=email, post=post).exists()
        if not has_access:
            messages.error(request, "You don't have access to this post.")
            return redirect('request_access')

    return render(request, 'blogapp/blog_detail.html', {'post': post})

# def request_access(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         request.session['user_email'] = email
#         messages.success(request, f"Email '{email}' saved. You can now request access.")
#         return redirect('blog_list')
#     return render(request, 'blogapp/request_access.html')

# def request_post_access(request, post_id):
#     if request.method == 'POST':
#         email = request.session.get('user_email')
#         post = get_object_or_404(BlogPost, id=post_id)
#         if not email:
#             return redirect('request_access')

#         PrivatePostAccess.objects.get_or_create(email=email, post=post)
#         messages.success(request, f"Requested access to: {post.title}")
#         return redirect('blog_detail', post_id=post.id)
@login_required
def request_access(request):
    if request.method == "POST":
        message = request.POST.get('message', '')
        AccessRequest.objects.create(user=request.user, message=message)
        messages.success(request, "Your request has been submitted.")
        return redirect('request_access')
    return render(request, 'blogapp/request_access.html')


def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    user_email = request.session.get('user_email')
    return render(request, 'blogapp/blog_list.html', {'posts': posts, 'user_email': user_email})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ApprovedEmail

def request_access(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if not email:
            messages.error(request, "Please enter an email address.")
            return redirect('signin')

        # Check if the email exists and is approved
        approved_email = ApprovedEmail.objects.filter(email=email).first()

        if approved_email and approved_email.approved:
            messages.success(request, "Access granted. Redirecting to login...")
            # Redirect to the private blog login view or dashboard
            return redirect('login')  # make sure this 'login' view exists
        else:
            # Save the email for admin to review if not already in DB
            ApprovedEmail.objects.get_or_create(email=email)
            messages.info(request, "Your request has been submitted. Please wait for approval.")
            return redirect('signin')

    return render(request, 'signin.html')
