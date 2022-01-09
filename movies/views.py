from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import *
from .forms import MovieRatingForm, MovieReviewForm
from django.http import HttpResponseRedirect


def home_view(request):
    movies = Movie.objects.all()
    a = list(dict(request.GET).keys())
    if request.GET:
        print(a)
        movies = Movie.objects.filter(genre__name__in=a).all()
    context = {
        'movies': movies
    }
    return render(request, 'movies/homepage.html', context=context)


def movie_detail_view(request, url):
    profile = Profile.objects.filter(user__pk=request.user.pk).first()
    movie = get_object_or_404(Movie, url=url)
    similar = Movie.objects.filter(series=movie.series).all()
    comments = Review.objects.filter(movie=movie).all()
    votes = Vote.objects.filter(movie=movie).all()
    have = Profile.objects.filter(watch_later__name__contains=movie.name).first()

    print(votes)
    try:
        curr_rating = round(float(movie.rating/movie.voters), 2)
    except ZeroDivisionError:
        curr_rating = 0
    if request.method != 'POST':
        form1 = MovieReviewForm()
        form2 = MovieRatingForm()
    else:
        form1 = MovieReviewForm(data=request.POST)
        form2 = MovieRatingForm(data=request.POST)
        set_comment(request, form1, movie)
        try:
            set_vote(request, form2, movie)
            movie.rating += form2.cleaned_data['value']
            movie.voters += 1
            movie.save()
        except IntegrityError as e:
            print(e)

    context = {
        'movie': movie,
        'similar': similar,
        'rate': curr_rating,
        'form1': form1,
        'form2': form2,
        'comments': comments,
        'profile': profile,
        'have': have
    }

    return render(request, 'movies/movie_detail.html', context=context)


@login_required(login_url='login')
def profile_view(request):
    profile = Profile.objects.get_or_create(user=request.user)
    count1 = len(profile[0].watch_later.all())
    count2 = len(profile[0].viewed.all())
    count3 = len(profile[0].abandoned.all())

    context = {
        'profile': profile,
        'count1': count1,
        'count2': count2,
        'count3': count3,
    }
    return render(request, 'movies/profile.html', context=context)


@login_required(login_url='login')
def watch_later(request, url):
    movie = Movie.objects.filter(url=url).first()
    profile = Profile.objects.get_or_create(user=request.user)
    profile = profile[0]
    profile.watch_later.add(movie)
    profile.save()
    print(profile.watch_later.all())
    return redirect('profile')


@login_required(login_url='login')
def viewed(request, url):
    movie = Movie.objects.filter(url=url).first()
    profile = Profile.objects.get_or_create(user=request.user)
    profile = profile[0]
    profile.viewed.add(movie)
    profile.save()
    print(profile.viewed.all())
    return redirect('profile')


@login_required(login_url='login')
def abandoned(request, url):
    movie = Movie.objects.filter(url=url).first()
    profile = Profile.objects.get_or_create(user=request.user)
    profile = profile[0]
    profile.abandoned.add(movie)
    profile.save()
    print(profile.abandoned.all())
    return redirect('profile')


@login_required(login_url='login')
def watch_later_list_view(request):
    profile = Profile.objects.get_or_create(user=request.user)
    profile = profile[0]
    watch_later_list = profile.watch_later.all()
    return render(request, 'movies/watch_later.html', {'watch_later': watch_later_list})


@login_required(login_url='login')
def viewed_list_view(request):
    profile = Profile.objects.get_or_create(user=request.user)
    profile = profile[0]
    viewed_list = profile.viewed.all()
    return render(request, 'movies/viewed.html', {'viewed': viewed_list})


@login_required(login_url='login')
def abandoned_list_view(request):
    profile = Profile.objects.get_or_create(user=request.user)
    profile = profile[0]
    abandoned_list = profile.abandoned.all()
    return render(request, 'movies/abandoned.html', {'abandoned_list': abandoned_list})


@login_required(login_url='login')
def set_comment(request, form, movie):
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.author = request.user
        new_comment.movie = movie
        form.save()
        return HttpResponseRedirect('detail')


@login_required(login_url='login')
def set_vote(request, form, movie):
    if form.is_valid():
        vote = form.save(commit=False)
        vote.user = request.user
        vote.movie = movie
        form.save()
        return HttpResponseRedirect('detail')
