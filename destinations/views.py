from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .models import Destination, Guide, Review
from .forms import ReviewForm


# ──────────────────────────────────────────
# Destination Views
# ──────────────────────────────────────────

class DestinationListView(ListView):
    model = Destination
    template_name = 'tours/home.html'
    context_object_name = 'destinations'


class DestinationDetailView(DetailView):
    model = Destination
    template_name = 'tours/destination_detail.html'


class DestinationCreateView(LoginRequiredMixin, CreateView):
    model = Destination
    fields = ['name', 'description', 'image_url', 'category', 'price']
    template_name = 'tours/destination_form.html'
    success_url = reverse_lazy('home')


class DestinationUpdateView(LoginRequiredMixin, UpdateView):
    model = Destination
    fields = ['name', 'description', 'image_url', 'category', 'price']
    template_name = 'tours/destination_form.html'
    success_url = reverse_lazy('home')


class DestinationDeleteView(LoginRequiredMixin, DeleteView):
    model = Destination
    template_name = 'tours/destination_confirm_delete.html'
    success_url = reverse_lazy('home')


# ──────────────────────────────────────────
# Destination Comment Views
# (using Review model with no guide, comment as text)
# ──────────────────────────────────────────

@login_required
def add_comment(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Review.objects.create(
                user_name=request.user.username,
                comment=content,
                rating=5,
            )
    return redirect('destination-detail', pk=pk)


@login_required
def comment_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    return redirect('home')


# ──────────────────────────────────────────
# Auth Views
# ──────────────────────────────────────────

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'user/register.html', {'form': form})


# ──────────────────────────────────────────
# Guide Views
# ──────────────────────────────────────────

class GuideListView(ListView):
    model = Guide
    template_name = 'tours/guide_list.html'
    context_object_name = 'guides'


class GuideDetailView(DetailView):
    model = Guide
    template_name = 'tours/guide_detail.html'


class GuideCreateView(LoginRequiredMixin, CreateView):
    model = Guide
    fields = ['name', 'specialty', 'bio', 'avatar_url', 'category']
    template_name = 'tours/guide_form.html'
    success_url = reverse_lazy('guide-list')


class GuideUpdateView(LoginRequiredMixin, UpdateView):
    model = Guide
    fields = ['name', 'specialty', 'bio', 'avatar_url', 'category']
    template_name = 'tours/guide_form.html'
    success_url = reverse_lazy('guide-list')


class GuideDeleteView(LoginRequiredMixin, DeleteView):
    model = Guide
    template_name = 'tours/guide_confirm_delete.html'
    success_url = reverse_lazy('guide-list')


# ──────────────────────────────────────────
# Guide Review Views
# ──────────────────────────────────────────

@login_required
def add_or_update_guide_review(request, pk):
    guide = get_object_or_404(Guide, pk=pk)
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '').strip()
        Review.objects.update_or_create(
            guide=guide,
            user_name=request.user.username,
            defaults={'rating': rating, 'comment': comment},
        )
    return redirect('guide-detail', pk=pk)


@login_required
def delete_guide_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    guide_pk = review.guide.pk if review.guide else None
    review.delete()
    if guide_pk:
        return redirect('guide-detail', pk=guide_pk)
    return redirect('guide-list')


# ──────────────────────────────────────────
# Guide Comment Views (reusing Review model)
# ──────────────────────────────────────────

@login_required
def add_guide_comment(request, pk):
    guide = get_object_or_404(Guide, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Review.objects.create(
                guide=guide,
                user_name=request.user.username,
                comment=content,
                rating=0,
            )
    return redirect('guide-detail', pk=pk)


@login_required
def edit_guide_comment(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            review.comment = content
            review.save()
    guide_pk = review.guide.pk if review.guide else None
    if guide_pk:
        return redirect('guide-detail', pk=guide_pk)
    return redirect('guide-list')


@login_required
def delete_guide_comment(request, pk):
    review = get_object_or_404(Review, pk=pk)
    guide_pk = review.guide.pk if review.guide else None
    review.delete()
    if guide_pk:
        return redirect('guide-detail', pk=guide_pk)
    return redirect('guide-list')


# ──────────────────────────────────────────
# Guide Image Views (placeholder – no GuideImage model yet)
# ──────────────────────────────────────────

@login_required
def add_guide_image(request, pk):
    messages.info(request, 'Image upload is not yet implemented.')
    return redirect('guide-detail', pk=pk)


@login_required
def delete_guide_image(request, pk):
    messages.info(request, 'Image deletion is not yet implemented.')
    return redirect('guide-list')


# ──────────────────────────────────────────
# Public Reviews View
# ──────────────────────────────────────────

class ReviewListView(ListView):
    model = Review
    template_name = 'tours/reviews.html'
    context_object_name = 'reviews'
    
    def get_queryset(self):
        queryset = Review.objects.filter(is_visible=True, guide__isnull=False).select_related('guide').order_by('-created_at')
        guide_id = self.request.GET.get('guide')
        if guide_id:
            queryset = queryset.filter(guide_id=guide_id)
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['guides'] = Guide.objects.all()
        guide_id = self.request.GET.get('guide')
        context['selected_guide_id'] = int(guide_id) if guide_id and guide_id.isdigit() else None
        return context

def leave_review(request):
    guides_exist = Guide.objects.exists()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.is_visible = False  # Keep unvisible for moderation
            review.save()
            messages.success(request, "Thank you! Your review has been submitted and will appear after approval.")
            return redirect('leave_review')
    else:
        form = ReviewForm()
        
    return render(request, 'tours/leave_review.html', {
        'form': form,
        'guides_exist': guides_exist
    })
