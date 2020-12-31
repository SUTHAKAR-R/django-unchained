from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.contrib.auth.models import User
from django.views.generic import (
	View,
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = "posts"     # default context_view_name for ListView is object_list 
	ordering = ['-date']			  # which is usually, but not necessarily a queryset
	paginate_by = 3


class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'  # app/model_viewtype.html 
	context_object_name = "posts"
	paginate_by = 3

	# queryset = A QuerySet that has all the objects of the model given in model = Post 
	# aka queryset = Post.objects.all()
	# get_queryset returns the objects in the queryset variable otherwise calls all() in Post model
	# to filter the objects override the get_queryset() method


	def get_queryset(self):

		# get_object_or_404(klass, *args, **kwargs)
		# ListView has a get() method
		# (self.request) positional = (self.args) name-based (self.kwargs)  self.request.user

		user = get_object_or_404(User, username=self.kwargs['username'])
		return Post.objects.filter(author=user).order_by('-date')


class PostDetailView(DetailView):
	# get_context_data()
	# default implementation adds the object being displayed to the template
	# so the template post_detail.html gets an object from Post model
	# default context_object_name = object 
	model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		# Call the base implementation or default implementation of UpdateView to get a context
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


def about(request):
    context = {
        'title' : 'About'
    }
    return render(request, 'blog/about.html', {'title' : 'About'})
