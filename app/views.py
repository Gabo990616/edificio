from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def home(request):
    return render(request, "app/home.html")


def adicionar_edificio(request):
    data = {
        "form": EdificioForm(),
    }

    if request.method == "POST":
        formulario = EdificioForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Edificio agregado correctamente")
            return redirect(to="listar_edificios")
        else:
            data["form"] = formulario

    return render(request, "app/edificio/adicionar.html", data)


def listar_edificios(request):
    edificios = Edificio.objects.all()
    page = request.GET.get("page", 1)
    try:
        paginator = Paginator(edificios, 5)
        edificios = paginator.page(page)
    except:
        raise Http404

    data = {
        "entity": edificios,
        "paginator": paginator,
    }
    return render(request, "app/edificio/listar.html", data)


def modificar_edificio(request, id):
    edificio = get_object_or_404(Edificio, id=id)

    data = {"form": EdificioForm(instance=edificio)}

    if request.method == "POST":
        formulario = EdificioForm(data=request.POST, instance=edificio)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Edificio modificado correctamente")
            return redirect(to="listar_edificios")
        else:
            data["form"] = formulario

    return render(request, "app/edificio/modificar.html", data)


def eliminar_edificio(request, id):
    edificio = get_object_or_404(Edificio, id=id)
    edificio.delete()
    messages.success(request, "Edificio eliminado correctamente")
    return redirect(to="listar_edificios")


def apartamentos(request):
    return render(request, "app/apartamentos.html")


def adicionar_apartamento(request):
    data = {
        "form": ApartamentoForm(),
    }

    # Recuperar datos de sesión si existen (después de agregar propietario)
    if "apartamento_form_data" in request.session:
        data["form"] = ApartamentoForm(request.session["apartamento_form_data"])
        del request.session["apartamento_form_data"]

    if request.method == "POST":
        formulario = ApartamentoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Apartamento agregado correctamente")
            return redirect(to="listar_apartamentos")
        else:
            data["form"] = formulario
            messages.error(request, "Por favor, corrige los errores en el formulario")

    return render(request, "app/apartamento/adicionar.html", data)


# def adicionar_apartamento(request):
#     data = {
#         "form": ApartamentoForm(),
#     }

#     if request.method == "POST":
#         formulario = ApartamentoForm(data=request.POST)
#         if formulario.is_valid():
#             formulario.save()
#             messages.success(request, "Apartamento agregado correctamente")
#             return redirect(to="listar_apartamentos")
#         else:
#             data["form"] = formulario

#     return render(request, "app/apartamento/adicionar.html", data)


def listar_apartamentos(request):
    apartamentos = Apartamento.objects.all()
    page = request.GET.get("page", 1)
    try:
        paginator = Paginator(apartamentos, 5)
        apartamentos = paginator.page(page)
    except:
        raise Http404

    data = {
        "entity": apartamentos,
        "paginator": paginator,
    }
    return render(request, "app/apartamento/listar.html", data)


def modificar_apartamento(request, id):
    apartamento = get_object_or_404(Apartamento, id=id)

    data = {"form": ApartamentoForm(instance=apartamento)}

    if request.method == "POST":
        formulario = ApartamentoForm(data=request.POST, instance=apartamento)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Apartamento modificado correctamente")
            return redirect(to="listar_apartamentos")
        else:
            data["form"] = formulario

    return render(request, "app/apartamento/modificar.html", data)


def eliminar_apartamento(request, id):
    apartamento = get_object_or_404(Apartamento, id=id)
    apartamento.delete()
    messages.success(request, "Apartamento eliminado correctamente")
    return redirect(to="listar_apartamentos")


def propietarios(request):
    return render(request, "app/propietarios.html")


def adicionar_propietario(request):
    data = {
        "form": PropietarioForm(),
    }

    # Guardar la URL de retorno (desde donde se llamó al formulario)
    return_url = request.GET.get("return_url", reverse("listar_propietarios"))
    data["return_url"] = return_url

    if request.method == "POST":
        formulario = PropietarioForm(data=request.POST)
        if formulario.is_valid():
            propietario = formulario.save()

            # Si viene del formulario de apartamento, guardar datos y redirigir de vuelta
            if "apartamento" in return_url:
                # Guardar el ID del nuevo propietario para seleccionarlo automáticamente
                request.session["nuevo_propietario_id"] = propietario.dni

                messages.success(
                    request,
                    "Propietario agregado correctamente. Continue con el apartamento.",
                )
                return redirect(to="adicionar_apartamento")
            else:
                messages.success(request, "Propietario agregado correctamente")
                return redirect(to="listar_propietarios")
        else:
            data["form"] = formulario
            messages.error(request, "Por favor, corrige los errores en el formulario")

    return render(request, "app/propietario/adicionar.html", data)


# def adicionar_propietario(request):
#     data = {
#         "form": PropietarioForm(),
#     }

#     if request.method == "POST":
#         formulario = PropietarioForm(data=request.POST)
#         if formulario.is_valid():
#             formulario.save()
#             messages.success(request, "Propietario agregado correctamente")
#             return redirect(to="listar_propietarios")
#         else:
#             data["form"] = formulario

#     return render(request, "app/propietario/adicionar.html", data)


def listar_propietarios(request):
    propietarios = Propietario.objects.all()
    page = request.GET.get("page", 1)
    try:
        paginator = Paginator(propietarios, 5)
        propietarios = paginator.page(page)
    except:
        raise Http404

    data = {
        "entity": propietarios,
        "paginator": paginator,
    }
    return render(request, "app/propietario/listar.html", data)


def modificar_propietario(request, dni):
    propietario = get_object_or_404(Propietario, dni=dni)

    data = {"form": PropietarioForm(instance=propietario)}

    if request.method == "POST":
        formulario = PropietarioForm(data=request.POST, instance=propietario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Propietario modificado correctamente")
            return redirect(to="listar_propietarios")
        else:
            data["form"] = formulario

    return render(request, "app/propietario/modificar.html", data)


def eliminar_propietario(request, dni):
    propietario = get_object_or_404(Propietario, dni=dni)
    propietario.delete()
    messages.success(request, "Propietario eliminado correctamente")
    return redirect(to="listar_propietarios")


@csrf_exempt
@require_POST
def clear_session_propietario(request):
    if "nuevo_propietario_id" in request.session:
        del request.session["nuevo_propietario_id"]
    return JsonResponse({"status": "ok"})
