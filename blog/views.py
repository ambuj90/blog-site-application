from django.shortcuts import render
from .models import BlogPost
from django.http import JsonResponse

def home(request):
    posts = BlogPost.objects.all()
    return render(request, "home.html", {"posts": posts})

def post_detail(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    return render(request, "post_detail.html", {"post": post})

def testing(request):
    posts = BlogPost.objects.all()
    return render(request, "testing.html", {"posts": posts})

def test_detail(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    return render(request, "test_detail.html", {"post": post})


def domain_analysis_view(request):
    return JsonResponse({"message": "Domain analysis API is working."})



# def count_up_to(n):
#     count = 1
#     while count <= n:
#         yield count  # Returns a value but pauses execution
#         count += 1

# gen = count_up_to(3)
# print(next(gen))  # Output: 1
# print(next(gen))  # Output: 2
# print(next(gen))  # Output: 3


