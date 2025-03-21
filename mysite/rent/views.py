from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from .models import Group, Product, Status, Reservation
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import password_validation
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, ReservationCreateUpdateForm

@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    try:
                        password_validation.validate_password(password)
                    except password_validation.ValidationError as e:
                        for error in e:
                            messages.error(request, error)
                        return redirect('register')

                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        new_email = request.POST['email']
        if new_email == "":
            messages.error(request, f'El. paštas negali būti tuščias!')
            return redirect('profile')
        if request.user.email != new_email and User.objects.filter(email=new_email).exists():
            messages.error(request, f'Vartotojas su el. paštu {new_email} jau užregistruotas!')
            return redirect('profile')
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.info(request, f"Profilis atnaujintas")
            return redirect('profile')


    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, "profile.html", context=context)


def index(request):
    num_products = Product.objects.all().count()
    num_groups = Group.objects.all().count()
    num_status = Status.objects.all().count()
    num_users = User.objects.all().count()

    context = {
        'num_products': num_products,
        'num_status': num_status,
        'num_groups': num_groups,
        'num_users': num_users,
    }
    return render(request, 'base.html', context)

def products(request):
    all_products = Product.objects.all()

    lighting_products = all_products.filter(group__name="Apšvietimas")
    furniture_products = all_products.filter(group__name="Baldai")
    tent_products = all_products.filter(group__name="Palapinės")

    lighting_paginator = Paginator(lighting_products, 3)
    furniture_paginator = Paginator(furniture_products, 3)
    tent_paginator = Paginator(tent_products, 3)

    lighting_page_number = request.GET.get('lighting_page', 1)
    furniture_page_number = request.GET.get('furniture_page', 1)
    tent_page_number = request.GET.get('tent_page', 1)

    lighting_page = lighting_paginator.get_page(lighting_page_number)
    furniture_page = furniture_paginator.get_page(furniture_page_number)
    tent_page = tent_paginator.get_page(tent_page_number)

    context = {
        'lighting_page': lighting_page,
        'furniture_page': furniture_page,
        'tent_page': tent_page,
    }

    return render(request, 'products.html', context)


def product(request, product_id):
    # Iš anksto pasiruošiam „Status“ su susijusiomis rezervacijomis
    product = Product.objects.prefetch_related(
        'product_status__reservations_status'  # Susiję rezervacijų duomenys
    ).get(id=product_id)

    context = {
        "product": product,
    }
    return render(request, 'product.html', context)


def search(request):
    query = request.GET.get('query')
    product_search_result = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(group__name__icontains=query) | Q(product_status__uuid__icontains=query)
)
    context = {
        'query': query,
        'products': product_search_result,
    }
    return render(request, 'search.html', context)

class CustomerProductsListView(LoginRequiredMixin, generic.ListView):
    model = Status
    template_name = "my_products.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Status.objects.filter(customer=self.request.user)


class StatusListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
     model = Status
     template_name = "statuses.html"
     context_object_name = "statuses"

     def test_func(self):
         return self.request.user.profile.is_employee


class StatusDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Status
    template_name = "single_status.html"
    context_object_name = "single_status"

    def test_func(self):
         return self.request.user.profile.is_employee


class StatusCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Status
    template_name = "status_form.html"
    fields = ['product', 'customer', 'condition']
    success_url = "/rent/statuses/"

    def test_func(self):
        return self.request.user.profile.is_employee


class StatusUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Status
    template_name = "status_form.html"
    fields = ['product', 'customer', 'condition']
    # success_url = "/rent/statuses/"

    def form_valid(self, form):
        form.instance.status_id = self.kwargs['pk']
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.profile.is_employee

    def get_success_url(self):
        return reverse('single_status', kwargs={'pk': self.kwargs['pk']})


class StatusDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Status
    template_name = "status_confirm_delete.html"
    context_object_name = "single_status"

    def test_func(self):
        return self.request.user.profile.is_employee

    def get_success_url(self):
        return reverse('statuses')


class ReservationCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Reservation
    template_name = "reservation_form.html"
    form_class = ReservationCreateUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Gaukite susijusį `Status` objektą pagal perduotą `pk`
        status = Status.objects.get(pk=self.kwargs['pk'])

        # Pridėkite reikalingus duomenis į kontekstą
        context['status'] = status
        context['product_name'] = status.product.name if status.product else "Produkto pavadinimas nerastas"

        return context


    def form_valid(self, form):
        form.instance.status_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('single_status', kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        return self.request.user.profile.is_employee

class ReservationUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Reservation
    # fields = ['customer', 'start_date', 'end_date']
    template_name = "reservation_form.html"
    form_class = ReservationCreateUpdateForm

    def get_object(self, queryset=None):
        try:
            return Reservation.objects.get(pk=self.kwargs['pk'])
        except Reservation.DoesNotExist:
            raise Http404("Rezervacija nerasta")

    def form_valid(self, form):
        form.instance.status_id = self.kwargs['status_pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('single_status', kwargs={'pk': self.kwargs['status_pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservation = self.get_object() # Gauti rezervacijos objektą
        status = reservation.status # Gauti susijusį Status objektą per užsienio raktą
        # Įtraukti Status objektą ir produkto pavadinimą į kontekstą
        context['status'] = status
        context['product_name'] = status.product.name if status.product else "Produkto pavadinimas nerastas"
        return context

    def test_func(self):
        return self.request.user.profile.is_employee


class ReservationDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Reservation
    template_name = "reservation_delete.html"
    context_object_name = "reservation"

    def get_object(self, queryset=None):
        reservation = Reservation.objects.get(pk=self.kwargs['pk'])
        return reservation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservation = self.get_object()
        status = reservation.status

        # Įtraukti papildomą informaciją į kontekstą
        context['status'] = status
        context['product_name'] = status.product.name if status.product else "Produkto pavadinimas nerastas"
        context['reservation_pk'] = reservation.pk
        return context

    def get_success_url(self):
        return reverse('single_status', kwargs={'pk': self.object.status.pk})

    def test_func(self):
        # Tikrina, ar vartotojas yra darbuotojas, kaip ir kitose klasėse
        return self.request.user.profile.is_employee



