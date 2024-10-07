from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.utils.safestring import mark_safe
from django.db.models import Q
from .models import *
from .forms import *
import markdown2
# Create your views here.
from datetime import date
import os

def index(request):
    profile_pic = None
    latest_posts = Post.objects.all().order_by("-date")[:2]
    if not request.user.is_authenticated:
        return render(request, "blog_site/index.html", {
        "posts": latest_posts,
        "profile_pic": profile_pic
    })
    try:
        profile_pic = UserProfileModel.objects.get(user = request.user)
    except UserProfileModel.DoesNotExist:
        profile_pic = None  
    return render(request, "blog_site/index.html", {
        "posts": latest_posts,
        "profile_pic": profile_pic
    })

@login_required(login_url="auth:index")
def get_date(post):
    return post['date']

@login_required(login_url="auth:index")
def posts(request):
    all_posts = Post.objects.all().order_by("-date")
    return render(request, "blog_site/all-posts.html", {
        "posts":all_posts, 
    })

class DetailPostView(LoginRequiredMixin,View):
    login_url = reverse_lazy("auth:login")
    def get(self, request, slug):
        detail_blog = Post.objects.get(slug = slug)
        blog_markdown = markdown2.markdown(detail_blog.content)
        blog_markdown = mark_safe(blog_markdown)
        return render(request, "blog_site/post-detail.html", {
            "detail_blog": detail_blog,
            "tags": detail_blog.tags.all(),
            "content": blog_markdown, 
        })

class UserProfileView(LoginRequiredMixin,View):
    login_url = reverse_lazy("auth:login")
    def get(self, request, username):
        user = User.objects.get(username = username)
        posts = user.posts.all()
        try:
            user_profile = UserProfileModel.objects.get(user = user)
            print(user_profile)
        except UserProfileModel.DoesNotExist:
            return render(request, "blog_site/userProfile.html", 
                          {
                              "posts": posts, 
                              "user": user,
                              "cantidad": len(posts)
                          })    
        return render(request, "blog_site/userProfile.html", {
            "posts": posts,
            "user_profile": user_profile, 
            "cantidad": len(posts)
        })

class MyProfileView(View):
    def get(self, request):
        user = User.objects.get(username = request.user)
        posts = user.posts.all()
        read_later = Post.objects.filter(id__in = request.session.get("save", []))
        try:
            userProfile = UserProfileModel.objects.get(user = request.user)
        except UserProfileModel.DoesNotExist:
            return render(request, "blog_site/miPerfil.html", {
            "userProfile": None,
            "guardados": len(request.session.get("save", [])),
            "posts": posts, 
            "read_later": read_later
        })
        return render(request, "blog_site/miPerfil.html", {
            "userProfile": userProfile,
            "guardados": len(request.session.get("save", [])),
            "posts": posts, 
            "read_later": read_later
        })
class ReadLaterView(LoginRequiredMixin,View):
    login_url = reverse_lazy("auth:login")
    def post(self, request, id, slug):
        #add to session
        if "save" not in request.session:
            request.session["save"] = []
        #borrar del leer mas tarde 
        if "save" in request.POST:
            if id in request.session["save"]:
                request.session["save"].remove(id)
        elif "not_save" in request.POST:
            if id not in request.session["save"]:
                request.session["save"].append(id)
        request.session.modified = True
        return redirect(reverse("blog_site:detail_post", kwargs={"slug": slug}))
        # if "save" not in request.session:
        #     request.session['save']

class PerfilView(LoginRequiredMixin, View):
    login_url = reverse_lazy("auth:login")
    def get(self, request):
        form = ProfileForm()
        try:
            perfil = UserProfileModel.objects.get(user = request.user)
        except UserProfileModel.DoesNotExist:
            return render(request, "blog_site/perfil.html", {
            "form": form
        })    
        return render(request, "blog_site/perfil.html", {
            "form": form,
            "perfil": perfil
        })
    
    def post(self, request):
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            #create new model instance
            #change both bio and profile pic
            if len(form.cleaned_data['biografia']) > 0 and form.cleaned_data['profile_pic'] is not None:
                profile = UserProfileModel(user = request.user, biografia = form.cleaned_data['biografia'], profile_pic = form.cleaned_data['profile_pic'])
                try:
                    profile.save()
                #unique constraint failling
                except IntegrityError:
                    user = request.user
                    userProfile = UserProfileModel.objects.get(user = user)
                    if userProfile.profile_pic:
                        userProfile.profile_pic.delete(save=False)
                        userProfile.save()
                    userProfile.profile_pic = form.cleaned_data['profile_pic']
                    userProfile.biografia = form.cleaned_data['biografia']
                    userProfile.save()
                return redirect(reverse("blog_site:perfil"))
            #just change bio
            elif len(form.cleaned_data['biografia']) > 0 and form.cleaned_data['profile_pic'] is None:
                print("b")
                try:
                    profile = UserProfileModel.objects.get(user = request.user)
                    profile.biografia = form.cleaned_data['biografia']
                    profile.save()
                except UserProfileModel.DoesNotExist:
                    profile = UserProfileModel(user = request.user, biografia = form.cleaned_data['biografia'])
                    profile.save()
                return redirect(reverse("blog_site:perfil"))
            #just change profile pic
            elif len(form.cleaned_data['biografia']) == 0 and form.cleaned_data['profile_pic'] is not None:
                print("c")
                profile = UserProfileModel.objects.get(user = request.user)
                try:
                    if profile.profile_pic:
                        profile.profile_pic.delete(save=False)
                        profile.save()
                    profile.profile_pic = form.cleaned_data['profile_pic']
                    profile.save()
                except UserProfileModel.DoesNotExist:
                    profile = UserProfileModel(user = request.user, profile = form.cleaned_data['profile_pic'])
                    profile.save()
                return redirect(reverse("blog_site:perfil"))
            return redirect(reverse("blog_site:perfil"))
        else:
            return render(request, "blog_site/perfil.html", {
            "form": form })

class CreateView(LoginRequiredMixin,View):
    login_url = reverse_lazy("auth:login")
    def get(self, request):
        form = PostForm()
        return render(request, "blog_site/create.html", {
            "form": form
        })
    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            print(form.cleaned_data['title'])
            try:
                new_post.save()
                for tag in form.cleaned_data['tags']:
                    new_post.tags.add(tag)
            except IntegrityError:
                return render(request, "blog_site/create.html", {
                "form":form,
                "message": 'No pueden existir dos blogs con el mismo nombre'
            })
            #despues va a renderizar al post detallado
            return redirect(reverse("blog_site:index"))
        else:
            return render(request, "blog_site/create.html", {
                "form":form
            })
    
class BorrarView(View):
    def post(self, request, slug):
        blog = Post.objects.get(slug = slug)
        blog.delete()
        return redirect(reverse("blog_site:index"))
    
class SearchView(View):
    def post(self, request):
        search = request.POST['post']
        busqueda = Post.objects.filter(Q(title__contains = search) | Q(author__username__contains = search ) | Q(tags__caption__contains = search )).distinct()
        print(busqueda)
        return render(request, "blog_site/search.html", {
            "search":search,
            "busquedas": busqueda,
            "cantidad": len(busqueda)
        })