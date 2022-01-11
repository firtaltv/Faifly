from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import *
from .forms import MovieRatingForm, MovieReviewForm
from django.http import HttpResponseRedirect, HttpResponse


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
    profile = Profile.objects.filter(user=request.user).first()
    movie = get_object_or_404(Movie, url=url)
    similar = Movie.objects.filter(series=movie.series).all()
    comments = Review.objects.filter(movie=movie).all()
    have = Profile.objects.filter(user=request.user).filter(watch_later__name=movie.name).first()
    have1 = Profile.objects.filter(user=request.user).filter(viewed__name=movie.name).first()
    have2 = Profile.objects.filter(user=request.user).filter(abandoned__name=movie.name).first()

    # try:
    #     curr_rating = round(float(movie.rating / movie.voters), 2)
    # except ZeroDivisionError:
    #     curr_rating = 0

    form1 = MovieReviewForm()
    form2 = MovieRatingForm()
    if request.method == 'POST':
        if 'comm' in request.POST:
            form1 = MovieReviewForm(data=request.POST)
            set_comment(request, form1, movie)
            form1 = MovieReviewForm()
            movie.save()
        if 'vote' in request.POST:
            if Vote.objects.filter(user=request.user).filter(movie__name=movie.name).first():
                a = Vote.objects.filter(user=request.user).filter(movie__name=movie.name).first()
                movie.rating -= a.value
                movie.voters -= 1
                movie.save()
                Vote.objects.filter(user=request.user).filter(movie__name=movie.name).delete()
            form2 = MovieRatingForm(data=request.POST)
            try:
                set_vote(request, form2, movie)
                if form2.cleaned_data:
                    movie.rating += form2.cleaned_data['value']
                    movie.voters += 1
                    movie.avg_rate = round(float(movie.rating / movie.voters), 2)
                form2 = MovieRatingForm()
                movie.save()
            except IntegrityError as e:
                print(e)

    context = {
        'movie': movie,
        'similar': similar,
        # 'rate': curr_rating,
        'form1': form1,
        'form2': form2,
        'comments': comments,
        'profile': profile,
        'have': have,
        'have1': have1,
        'have2': have2
    }

    return render(request, 'movies/movie_detail.html', context=context)


@login_required(login_url='login')
def profile_view(request, pk):
    if User.objects.filter(id=pk).first() and not Profile.objects.filter(user__id=pk).first():
        us = User.objects.filter(id=pk).first()
        p = Profile(user=us)
        p.save()
        print(1)
    elif not User.objects.filter(id=pk).first():
        return HttpResponse("No such User")
    profile = Profile.objects.filter(user__id=pk).first()

    count1 = len(profile.watch_later.all())
    count2 = len(profile.viewed.all())
    count3 = len(profile.abandoned.all())

    context = {
        'profile': profile,
        'count1': count1,
        'count2': count2,
        'count3': count3,
    }
    return render(request, 'movies/profile.html', context=context)


@login_required(login_url='login')
def go_private(request, pk):
    profile = Profile.objects.get_or_create(user=request.user)
    profile = profile[0]
    profile.is_public = False
    profile.save()
    return redirect('profile', pk=pk)


@login_required(login_url='login')
def go_visible(request, pk):
    profile = Profile.objects.get_or_create(user=request.user)
    profile = profile[0]
    profile.is_public = True
    profile.save()
    return redirect('profile', pk=pk)


@login_required(login_url='login')
def watch_later(request, url):
    pk = request.user.id
    movie = Movie.objects.filter(url=url).first()
    profile = Profile.objects.get_or_create(user=request.user)
    profile = profile[0]
    if Profile.objects.filter(viewed__name=movie.name).first():
        profile.viewed.remove(movie)
    elif Profile.objects.filter(abandoned__name=movie.name).first():
        profile.abandoned.remove(movie)
    profile.watch_later.add(movie)
    profile.save()
    print(profile.watch_later.all())
    return redirect('profile', pk=pk)


@login_required(login_url='login')
def viewed(request, url):
    pk = request.user.id
    movie = Movie.objects.filter(url=url).first()
    profile = Profile.objects.get_or_create(user=request.user)
    profile = profile[0]
    if Profile.objects.filter(watch_later__name=movie.name).first():
        profile.watch_later.remove(movie)
    elif Profile.objects.filter(abandoned__name=movie.name).first():
        profile.abandoned.remove(movie)
    profile.viewed.add(movie)
    profile.save()
    print(profile.viewed.all())
    return redirect('profile', pk=pk)


@login_required(login_url='login')
def abandoned(request, url):
    pk = request.user.id
    movie = Movie.objects.filter(url=url).first()
    profile = Profile.objects.get_or_create(user=request.user)
    profile = profile[0]
    if Profile.objects.filter(watch_later__name=movie.name).first():
        profile.watch_later.remove(movie)
    elif Profile.objects.filter(viewed__name=movie.name).first():
        profile.viewed.remove(movie)
    profile.abandoned.add(movie)
    profile.save()
    print(profile.abandoned.all())
    return redirect('profile', pk=pk)


@login_required(login_url='login')
def delete_from_later(request, url):
    pk = request.user.id
    movie = Movie.objects.filter(url=url).first()
    profile = Profile.objects.get_or_create(user=request.user)
    profile = profile[0]
    profile.watch_later.remove(movie)
    profile.save()
    print(profile.abandoned.all())
    return redirect('watch_later_list', pk=pk)


@login_required(login_url='login')
def delete_from_viewed(request, url):
    pk = request.user.id
    movie = Movie.objects.filter(url=url).first()
    profile = Profile.objects.get_or_create(user=request.user)
    profile = profile[0]
    profile.viewed.remove(movie)
    profile.save()
    print(profile.abandoned.all())
    return redirect('viewed_list', pk=pk)


@login_required(login_url='login')
def delete_from_abandoned(request, url):
    pk = request.user.id
    movie = Movie.objects.filter(url=url).first()
    profile = Profile.objects.get_or_create(user=request.user)
    profile = profile[0]
    profile.abandoned.remove(movie)
    profile.save()
    print(profile.abandoned.all())
    return redirect('abandoned_list', pk=pk)


@login_required(login_url='login')
def watch_later_list_view(request, pk):
    if User.objects.filter(id=pk).first() and not Profile.objects.filter(user__id=pk).first():
        us = User.objects.filter(id=pk).first()
        p = Profile(user=us)
        p.save()
    else:
        HttpResponse("No such User")
    profile = Profile.objects.filter(user__id=pk).first()
    watch_later_list = profile.watch_later.all()
    context = {'watch_later': watch_later_list,
               'pk': pk,
               'profile': profile
               }
    return render(request, 'movies/watch_later.html', context=context)


@login_required(login_url='login')
def viewed_list_view(request, pk):
    if User.objects.filter(id=pk).first() and not Profile.objects.filter(user__id=pk).first():
        us = User.objects.filter(id=pk).first()
        p = Profile(user=us)
        p.save()
    else:
        HttpResponse("No such User")
    profile = Profile.objects.filter(user__id=pk).first()
    viewed_list = profile.viewed.all()
    context = {'viewed': viewed_list,
               'pk': pk,
               'profile': profile
               }
    return render(request, 'movies/viewed.html', context=context)


@login_required(login_url='login')
def abandoned_list_view(request, pk):
    if User.objects.filter(id=pk).first() and not Profile.objects.filter(user__id=pk).first():
        us = User.objects.filter(id=pk).first()
        p = Profile(user=us)
        p.save()
    else:
        HttpResponse("No such User")
    profile = Profile.objects.filter(user__id=pk).first()
    abandoned_list = profile.abandoned.all()
    context = {'abandoned_list': abandoned_list,
               'pk': pk,
               'profile': profile
               }
    return render(request, 'movies/abandoned.html', context=context)


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


def users_list(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'movies/users_list.html', context=context)
