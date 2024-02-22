from django.shortcuts import render,redirect,get_object_or_404
from posts.models import Post,Comment,Tag
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.forms import PostCreateForm,CommentForm,TagCreateForm
from django.urls import reverse
from hitcount.views import HitCountDetailView,HitCountMixin
from hitcount.models import HitCount
from hitcount.utils import get_hitcount_model
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.http import HttpResponse

# Create your views here.

from datetime import datetime

# Example ISO 8601 formatted string
iso_string = "2022-01-15T15:30:00"

# Create a datetime object from the ISO 8601 formatted string
dt_object = datetime.fromisoformat(iso_string)


class PostView(View):
    model  = Post
    count_hit = False

    def get(self,request):
        post_list = Post.objects.filter(status=Post.Status.Verified).order_by('id')
        search_query = request.GET.get('q','')
        if search_query:
            post_list = post_list.filter(title__icontains=search_query)

        paginator = Paginator(post_list,2)
        page_num = request.GET.get('page',2)
        page_obj = paginator.get_page(page_num)

        context = {
            'page_obj':page_obj,
            'search_query':search_query,
    
        }
        return render(request,'posts/postList.html',context)

class PostDetail(HitCountDetailView,View):
    model = Post    
    count_hit = True
    template_name = 'posts/postDetail.html'

    def get(self,request,pk):
        post = get_object_or_404(Post,id=pk,status=Post.Status.Verified)
        comments = post.comments.filter(active=True)
        comment_form = CommentForm()
        if request.user != post.author:
            if request.user not in post.viewers.all():
                post.viewers.add(request.user)
                post.save()
                
        context = {
            'post':post,
            'comments':comments,
            'comment_form':comment_form
        }
        return render(request,'posts/postDetail.html',context)

    def post(self,request,pk): # Posting comments
        post = Post.objects.get(id=pk)
        comment_form = CommentForm(data=request.POST)
        comments = post.comments.filter(active=True)
        if comment_form.is_valid():
            Comment.objects.create(
               post = post,
               author = request.user,
               text = comment_form.cleaned_data['text']               
           )
            comment_form = CommentForm()

        else:
            comment_form = CommentForm(data=request.POST)

        context = {
            'post':post,
            'comments':comments,
            'comment_form':comment_form
        }    
        return render(request,'posts/postDetail.html',context)

class WeeklyPopularPosts(View):

    def get(self,request):
        
        posts_list = Post.objects.filter(status=Post.Status.Verified).order_by('id')
        if posts_list:
            start_time = (timezone.now() - timedelta(days=7))
            posts_list = Post.objects.filter(publish_time__gt=start_time,status=Post.Status.Verified).order_by('hit_count_generic')
            search_query = request.GET.get('q','')
            if search_query:
                posts_list = posts_list.filter(title__icontains=search_query)
            
            paginator = Paginator(posts_list,2)
            page_num = request.GET.get('page',1)
            page_obj = paginator.get_page(page_num)

            context = {
                'posts_lists':posts_list,
                'page_obj':page_obj,
                'search_query':search_query
            }

            return render(request,'posts/week.html',context)
        else:
            return HttpResponse("No posts found")   

class MonthlyPopularPosts(View):

    def get(self,request):
        post_list = Post.objects.filter(status=Post.Status.Verified).order_by('id')
        if post_list:   
            start_time = timezone.now() - timedelta(days=30)
            post_list = post_list.filter(publish_time__gt=start_time).order_by('hit_count_generic')
            search_query = request.GET.get('q','')
            if search_query:
                post_list = post_list.filter(title__icontains=search_query)
                
            paginator = Paginator(post_list,2)
            page_num = request.GET.get('page',1)
            page_obj = paginator.get_page(page_num)

            context = {
                'page_obj':page_obj,
                'search_query':search_query
                }
            return render(request,'posts/month.html',context)
        else:
            return HttpResponse("no posts found")
class RecommendedPostsView(View):
    
    def get(self,request):
        post_list = Post.objects.filter(status=Post.Status.Verified,recommendation=Post.Recommendation.Recommended).order_by('id')
        if post_list:
            search_query = request.GET.get('q','')
            if search_query:
                post_list = post_list.filter(title__icontains=search_query)
            
            paginator = Paginator(post_list,2)
            page_num = request.GET.get('page',1)
            page_obj = paginator.get_page(page_num)

            context = {
                'page_obj':page_obj,
                'search_query':search_query
            }

            return render(request,'posts/recommended.html',context)
        else:
            return HttpResponse("No posts found")
        
class PopularPostsView(View):

    def get(self,request):
        post_list = Post.objects.filter(status=Post.Status.Verified).order_by('-viewers')
        if post_list:
        # q
            search_query = request.GET.get('q','')
            if search_query:
                post_list = Post.objects.filter(title__icontains=search_query)  
            # paginator objects
            paginator = Paginator(post_list,2)
            page_num = request.GET.get('page',1)
            page_obj = paginator.get_page(page_num)
        else: 
            return HttpResponse("No post found")
        context = {
            'search_query':search_query,
            'page_obj':page_obj
        }
        return render(request,'posts/popular.html',context)
    

class CreatePostView(LoginRequiredMixin,View):

    def get(self,request):
        form = PostCreateForm()
        tag_form = TagCreateForm()
        context = {
            'form':form,
            'tag_form': tag_form
        }
        return render(request,'posts/postCreate.html',context)

    def post(self,request):
        form = PostCreateForm(data=request.POST,files=request.FILES)
        tag_form = TagCreateForm(data=request.POST)
        if tag_form.is_valid():
            Tag.objects.create(
                name = tag_form.cleaned_data['name']
            )
            tag_form = TagCreateForm()
        else: 
            tag_form = TagCreateForm(data=request.POST)
        if form.is_valid():
            new = Post.objects.create(
                author = request.user,
                title = form.cleaned_data['title'],
                picture = form.cleaned_data['picture'],
                text = form.cleaned_data['text']
            )
            new.tags.set(form.cleaned_data['tags'])
            return redirect('posts:post_list')
        else:
            form = PostCreateForm(data=request.POST,files=request.FILES)
        context = {
            'form': form,
            'tag_form': tag_form
        }
        return render(request,'posts/postCreate.html',context)
