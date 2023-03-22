from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Driver, Car, Manufacturer


@login_required
def index(request):
    """View function for the home page of the site."""

    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits + 1,
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    paginate_by = 5


class ManufacturerCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.CreateView
):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")
    template_name = "taxi/manufacturer_form.html"
    success_message = "%(name)s has been successfully created"


class ManufacturerUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView
):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")
    success_message = "%(name)s has been successfully updated"
    template_name = "taxi/manufacturer_form.html"


class ManufacturerDeleteView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.DeleteView
):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")
    success_message = "Manufacturer has been deleted!"
    template_name = "taxi/manufacturer_confirm_delete.html"


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.all().select_related("manufacturer")


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class CarCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.CreateView
):
    model = Car
    fields = "__all__"
    success_url = reverse_lazy("taxi:car-list")
    template_name = "taxi/car_form.html"
    success_message = "%(model)s has been successfully created"


class CarUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView
):
    model = Car
    fields = "__all__"
    success_url = reverse_lazy("taxi:car-list")
    success_message = "%(model)s has been successfully updated"
    template_name = "taxi/car_form.html"


class CarDeleteView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.DeleteView
):
    model = Car
    fields = "__all__"
    success_url = reverse_lazy("taxi:car-list")
    success_message = "Car has been deleted!"
    template_name = "taxi/car_confirm_delete.html"


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")
