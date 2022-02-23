from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post, Comment
from dj1.forms import CreateForm, CommentForm, SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from django.contrib.auth.decorators import login_required 

from django.contrib.auth import login, authenticate

# Create your views here.
# Update it here
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user) 
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            #img_obj = p_form.instance
            return redirect('dj1:profile') # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'registration/profile.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        #print(form)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dj1:all')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


class PostListView(ListView):
      model = Post
      template_name = 'dj1/post_list.html'
      def get(self, request):
          #posts = Post.objects.all()
          post_list = Post.objects.all().order_by('-updated_on')[:10]
          for obj in post_list:
            obj.natural_updated = naturaltime(obj.updated_on)
          ctx = {'post_list': post_list}
          return render(request, self.template_name, ctx)
class PostCreateView(CreateView):
      template_name = "dj1/post_form.html"
      success_url = reverse_lazy('dj1:all')
      def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

      def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        # Add owner to the model before saving
        ad = form.save(commit=False) # In Inset/create vieww
        ad.owner = self.request.user
        ad.save()
        form.save_m2m()
        return redirect(self.success_url)
        
class PostDetailView(DetailView):
      model = Post
      template_name = 'dj1/post_detail.html'
      def get(self, request, pk):
          post = Post.objects.get(id = pk)
          comments = Comment.objects.filter(post = post).order_by('-updated_on')
          comment_form = CommentForm()
          ctx = {'post':post, 'comments':comments, 'comment_form':comment_form}
          return render(request, self.template_name, ctx)
      
class PostUpdateView(UpdateView):
      template_name = 'dj1/post_form.html'
      success_url = reverse_lazy('dj1:all')
      
      def get(self, request, pk):
          post = get_object_or_404(Post, id = pk, owner = self.request.user)
          form = CreateForm(instance = post)
          ctx = {'form':form}
          return render(request, self.template_name, ctx)
          
      def post(self, request, pk = None):
          post = get_object_or_404(Post, id = pk, owner = self.request.user)
          form = CreateForm(request.POST, request.FILES or None, instance = post)
          if not form.is_valid():
             ctx = {'form':form}
             return render(request, self.template_name, ctx)
          post = form.save(commit=False)
          post.owner = self.request.user
          post.save()
          form.save_m2m()
          
          return redirect(self.success_url)
class PostDeleteView(DeleteView):
      #template_name = 'dj1/post_delete.html'
      model = Post
class CommentCreateView(LoginRequiredMixin, View):
      def post(self, request, pk) :
        f = get_object_or_404(Post, id=pk)
        comment = Comment(body=request.POST['comment'], owner=request.user, post=f)
        comment.save()
        return redirect(reverse('dj1:post_detail', args=[pk]))
          
class CommentDeleteView(DeleteView):
      model = Comment
      template_name = 'dj1/comment_post_delete.html'
      def get_success_url(self):
          post = self.object.post
          return reverse('dj1:post_detail', args = [post.id])                


