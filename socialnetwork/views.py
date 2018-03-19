from __future__ import unicode_literals
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.utils import timezone
import time # for adding sleep calls to demonstrate concurrency issues
from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie
# Import all classes
from socialnetwork.models import *
# Import class: CreatePost EditPost
from socialnetwork.posts_decoration import CreatePost, EditPost
# import all forms
from socialnetwork.forms import *
import json
from django.conf import settings

@ensure_csrf_cookie
@login_required
def global_stream(request):
	context = {}
	return render(request, 'socialnetwork/global_stream.html', context)

@login_required
def follower_stream(request):
	context = {}
	return render(request, 'socialnetwork/follower_stream.html', context)

@login_required
def myProfile(request):
	context = {}
	# getFollowingList(object), here object is of Profile, not User
	# So use request.user.profile instead of request.user
	following_list   = getFollowingList(request.user.profile)
	followed_by_list = getFollowedByList(request.user.profile)
	context['following_list']   = following_list
	context['followed_by_list'] = followed_by_list
	context['form'] = ItemForm()
	context['items'] = Profile.objects.filter(user=request.user)
	return render(request, 'socialnetwork/myProfile.html', context)

@login_required
def edit_bio(request):
	context = {}
	current_username = request.user.username

	user_list = []
	for user in Profile.objects.all():
		user_list.append(user.user.username)

	if current_username not in user_list:
		message = "Sorry, this user doesn't exist."
		context['message'] = message
		return render(request, 'socialnetwork/someone_not_exist', context)

	current_user = request.user.profile
	if 'bio' not in request.POST or not request.POST['bio']:
		message = 'The Bio information is illegal.'
		context['message'] = message
		return render(request, 'socialnetwork/someone_not_exist', context)
		
	current_user.bio = request.POST['bio']
	current_user.save()
	# After the above 3 lines, the bio has been updated!
	# following_list = getFollowingList(request.user.profile)
	context['following_list'] = getFollowingList(request.user.profile)
	context['followed_by_list'] = getFollowedByList(request.user.profile)
	context['form'] = ItemForm()
	context['items'] = Profile.objects.filter(user=request.user)
	return render(request, 'socialnetwork/myProfile.html', context)

@login_required
# by clicking the username, one can visit the homepage of that user
def someone_profile(request):
	context = {}
	if not 'created_by' in request.GET:
		message = "Sorry, this user doesn't exist."
		context['message'] = message
		return render(request, 'socialnetwork/someone_not_exist.html', context)

	user_being_viewed = request.GET['created_by']
	# Here, we use request.user.username instead of request.user
	# Since the former is a string, the latter is an object
	if user_being_viewed == request.user.username:
		return myProfile(request)

	context['user_being_viewed'] = user_being_viewed
	this_user = Profile.objects.filter(user__username=user_being_viewed)
	if not this_user:
		context['message'] = 'Sorry, this user doesn\'t exist.'
		return render(request, 'socialnetwork/someone_not_exist.html', context)
	this_user = list(this_user)[0]
	# A is logged in, A is looking at B's profile
	# viewed_following_list:  For B
	# viewing_following_list: For A
	viewed_following_list  = getFollowingList(this_user)
	viewing_following_list = getFollowingList(request.user.profile)
	if user_being_viewed in viewing_following_list:
		# Already followed
		following_status = 'Y'
	else:
		following_status = 'N'
	context['following_status'] = following_status


	its_posts = Posts.objects.filter(created_by__username = this_user.user.username)
	context['user_being_viewed']  = this_user
	print(type(this_user))
	context['its_posts'] = its_posts.order_by("-creation_time")
	context['following_list']   = getFollowingList(this_user)
	context['followed_by_list'] = getFollowedByList(this_user)
	context['items'] = Profile.objects.filter(user=this_user.user)
	# print('some-pro')
	# print(type(context['items']))
	# print(context['items'])
	# print('###################')
	return render(request, 'socialnetwork/someone_profile.html', context)

@login_required
def follow(request):
	context = {}

	if not request.POST.get('user_being_viewed', False) or 'user_being_viewed' not in request.POST:
		message = "Sorry, this user doesn't exist."
		context['message'] = message
		return render(request, 'socialnetwork/someone_not_exist.html', context)

	user_being_viewed_name = request.POST.get('user_being_viewed', False)
	# print(user_being_viewed_name)
	user_being_viewed = Profile.objects.filter(user__username=user_being_viewed_name)
	this_user = user_being_viewed
	this_user = list(this_user)[0]
	current_user = request.user
	current_user.profile.following.add(list(user_being_viewed)[0])
	context['user_being_viewed'] = this_user
	print(type(list(user_being_viewed)[0]))
	context['following_status']  = 'Y'
	its_posts = Posts.objects.filter(created_by__username = user_being_viewed_name)
	context['its_posts'] = its_posts.order_by("-creation_time")
	user_being_viewed = list(user_being_viewed)[0]
	context['following_list']   = getFollowingList(user_being_viewed)
	context['followed_by_list'] = getFollowedByList(user_being_viewed)
	##########################################
	context['items'] = Profile.objects.filter(user=this_user.user)
	# print('follow')
	# print(type(context['items']))
	# print(context['items'])
	# print('###################')
	return render(request, 'socialnetwork/someone_profile.html', context)

# Unfollow is just like follow
@login_required
def unfollow(request):
	context = {}

	if not request.POST.get('user_being_viewed', False) or 'user_being_viewed' not in request.POST:
		message = "Sorry, this user doesn't exist."
		context['message'] = message
		return render(request, 'socialnetwork/someone_not_exist.html', context)

	user_being_viewed_name = request.POST.get('user_being_viewed', False)
	user_being_viewed = Profile.objects.filter(user__username=user_being_viewed_name)
	this_user = user_being_viewed
	this_user = list(this_user)[0]
	current_user = request.user
	current_user.profile.following.remove(list(user_being_viewed)[0])
	context['user_being_viewed'] = this_user
	context['following_status']  = 'N'
	its_posts = Posts.objects.filter(created_by__username = user_being_viewed_name)
	context['its_posts'] = its_posts.order_by("-creation_time")
	user_being_viewed = list(user_being_viewed)[0]
	context['following_list']   = getFollowingList(user_being_viewed)
	context['followed_by_list'] = getFollowedByList(user_being_viewed)
	context['items'] = Profile.objects.filter(user=this_user.user)
	return render(request, 'socialnetwork/someone_profile.html', context)

@login_required
# return a list of usernames
def getFollowingList(this_user):
	all_followings = this_user.following.all()
	following_list = []
	for following in all_followings:
		following_list.append(following.user.username)
	return following_list

@login_required
# return a list of usernames
def getFollowedByList(this_user):
	all_followed_bys = this_user.followed_by.all()
	followed_by_list = []
	for followed_by in all_followed_bys:
		followed_by_list.append(followed_by.user.username)
	return followed_by_list

def someone_not_exist(request):
	context = {}
	context['message'] = 'Sorry, some error occurs.'
	return render(request, 'socialnetwork/someone_not_exist.html', context)
	
def loginPage(request):
    return render(request, 'socialnetwork/login.html', {})

def register(request):
	context = {}

	# If it is a GET method, then just display the registration form.
	# Some doubt here.
	if request.method == 'GET':
		context['form'] = RegistrationForm()
		return render(request, 'socialnetwork/register.html', context)

	# Creates a bound form from the request POST parameters and makes the 
	# form available in the request context dictionary.
	form = RegistrationForm(request.POST)
	context['form'] = form
	# Validates the form.
	if not form.is_valid():
	    return render(request, 'socialnetwork/register.html', context)

	# At this point, the form data is valid.  Register and login the user.
	new_user = User.objects.create_user(username=form.cleaned_data['username'], 
	                                    password=form.cleaned_data['password1'],
	                                    email=form.cleaned_data['email'],
	                                    first_name=form.cleaned_data['first_name'],
	                                    last_name=form.cleaned_data['last_name'])
	new_user.save()

	# Logs in the new user and redirects to his/her todo list
	new_user = authenticate(username=form.cleaned_data['username'],
	                        password=form.cleaned_data['password1'])
	login(request, new_user)
	return redirect(reverse('home'))

@login_required
def add_photo(request):
	context = {}
	form = ItemForm(request.POST, request.FILES, instance=request.user.profile)
	if not form.is_valid():
	    context['form'] = form
	else:
		if hasattr(form.cleaned_data['picture'],'content_type'):
			request.user.profile.content_type = form.cleaned_data['picture'].content_type
		form.save()
		context['message'] = 'Item #{0} saved.'.format(request.user.id)
		context['form'] = ItemForm()

	context['items'] = Profile.objects.filter(user=request.user)
	return render(request, 'socialnetwork/myProfile.html', context)

@login_required
def get_photo(request, id):
    item = get_object_or_404(Profile, id=id)

    # Probably don't need this check as form validation requires a picture be uploaded.
    if not item.picture:
        raise Http404

    return HttpResponse(item.picture, content_type=item.content_type)

@login_required
@transaction.atomic
def add_comment(request):
	if request.method != 'POST':
	    raise Http404

	current_item_id = request.POST['current_post_id']
	if not request.POST['this_post'] or 'this_post' not in request.POST:
	    message = 'You must enter an item to add.'
	    json_error = '{ "error": "'+message+'" }'
	    return HttpResponse(json_error, content_type='application/json')

	current_post = Posts.objects.filter(id=current_item_id)[0]

	new_comment = Comments(
		content=request.POST['this_post'],
		created_by=request.user,
		creation_time=timezone.now(),
		post=current_post,
		created_by_username=request.user.username)
	new_comment.save()
	response_comments = serializers.serialize('json', Comments.objects.all())
	data = {'comments'  :   response_comments}
	return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
@transaction.atomic
def add_post(request):
	errors = []
	if 'post' not in request.POST or not request.POST['post']:
	    errors.append('You must enter something.')
	else:
	    new_post = Posts(content=request.POST['post'],
	                    created_by=request.user,
	                    creation_time=timezone.now(),
	                    created_by_username=request.user.username)
	    new_post.save()
	    new_post.created_by_identity = new_post.id
	    new_post.save()

	posts = Posts.objects.all().order_by("-creation_time")
	context = {'posts': posts, 'errors': errors}
	return render(request, 'socialnetwork/global_stream.html', context)

@login_required
def get_list_json(request):

	response_posts = serializers.serialize('json', Posts.objects.all())
	response_comments = serializers.serialize('json', Comments.objects.all())

	current_user = request.user.profile
	all_followings = current_user.following.all()
	following_list = []
	for following in all_followings:
		following_list.append(following.user.username)

	all_followings_streams  = Posts.objects.filter(created_by__username__in=following_list)
	all_followings_streams  = all_followings_streams.order_by('pk')

	all_followings_comments = Comments.objects.filter(post__created_by__username__in=following_list)
	all_followings_comments = all_followings_comments.order_by('pk')

	response_following_posts = serializers.serialize('json', all_followings_streams)
	response_following_comments = serializers.serialize('json', all_followings_comments)

	data = {'posts'     :   response_posts,
	        'comments'  :   response_comments,
	        'following_posts'   :	response_following_posts,
	        'following_comments':	response_following_comments,
	        }
	return HttpResponse(json.dumps(data), content_type='application/json')