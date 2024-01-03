from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, SelectDateWidget, HiddenInput, ModelForm, ImageField, forms, CharField, EmailField
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import CreateView

from accounts.models import Profile, UserImage


# Create your views here.

class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        # fields = '__all__'
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('index')
    template_name = 'signup.html'


class ProfileModelForm(ModelForm):
    first_name = CharField(label='Jméno', max_length=64)
    last_name = CharField(label='Příjmení', max_length=64)
    email = EmailField()
    user_image = ImageField(required=False)

    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'birth_date': SelectDateWidget(years=range(datetime.now().year, 1900, -1)),
            'user': HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileModelForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user


class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileModelForm
    template_name = 'profile_create.html'
    success_url = reverse_lazy('profile')

    user_image = ImageField(required=False)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.user.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        result = super().form_valid(form)

        user_image = self.request.FILES.get('user_image', None)
        if user_image:
            UserImage.objects.create(user=user.profile, image=user_image, description="Profilový obrázek")
        return result

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        user_profile = getattr(self.request.user, 'profile', None)
        if user_profile:
            obj = get_object_or_404(queryset, user=user_profile.user)
            return obj
        else:
            raise Http404("Profil neexistuje")


@login_required
def profile(request, pk):
    user_profile = Profile.objects.get(id=pk)
    images = UserImage.objects.filter(user=user_profile)
    context = {'profile': user_profile, 'images': images}
    return render(request, 'profile.html', context)


@login_required
def profile_edit(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileModelForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.save()
            image_path = form.cleaned_data.get('user_image')
            print(image_path)
            form.save()
            user.refresh_from_db()
            user_pk = user.pk
            return redirect(reverse('profile', kwargs={'pk': user_pk}))
        else:
            print('jsem tady')
    else:
        form = ProfileModelForm(instance=user.profile)

    context = {'form': form}
    return render(request, 'profile_edit.html', context)
