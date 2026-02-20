from datetime import datetime
from django.http import Http404, HttpResponseRedirect, JsonResponse, HttpResponse
from datetime import datetime
from django.http import Http404, HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from django.db.models import Case, When, Value, BooleanField
import pandas as pd
from django.db.models import Case, When, Value, BooleanField

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
        paginator = Paginator(edificios, 10)
        edificios = paginator.page(page)
    except:
        raise Http404

    data = {
        "entity": edificios,
        "paginator": paginator,
    }
    return render(request, "app/edificio/listar.html", data)


def detalle_edificio(request, edificio_id):
    """Vista principal del edificio - dashboard"""
    edificio = get_object_or_404(Edificio, id=edificio_id)

    # Estadísticas del edificio
    total_apartamentos = edificio.apartamento_set.count()
    total_propietarios = (
        Propietario.objects.filter(apartamentos__edificio=edificio).distinct().count()
    )

    context = {
        "edificio": edificio,
        "total_apartamentos": total_apartamentos,
        "total_propietarios": total_propietarios,
    }
    return render(request, "app/edificio/detalle.html", context)


def detalle_edificio(request, edificio_id):
    """Vista principal del edificio - dashboard"""
    edificio = get_object_or_404(Edificio, id=edificio_id)

    # Estadísticas del edificio
    total_apartamentos = edificio.apartamento_set.count()
    total_propietarios = (
        Propietario.objects.filter(apartamentos__edificio=edificio).distinct().count()
    )

    context = {
        "edificio": edificio,
        "total_apartamentos": total_apartamentos,
        "total_propietarios": total_propietarios,
    }
    return render(request, "app/edificio/detalle.html", context)


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


def adicionar_apartamento(request, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)

def adicionar_apartamento(request, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)

    data = {
        "form": ApartamentoForm(),
        "edificio": edificio,
        "edificio": edificio,
    }

    propietario_id = request.GET.get("propietario")
    if propietario_id:
        try:
            propietario = Propietario.objects.get(dni=propietario_id)
            data["form"].initial["propietario"] = propietario
        except Propietario.DoesNotExist:
            pass

    propietario_id = request.GET.get("propietario")
    if propietario_id:
        try:
            propietario = Propietario.objects.get(dni=propietario_id)
            data["form"].initial["propietario"] = propietario
        except Propietario.DoesNotExist:
            pass

    # Recuperar datos de sesión si existen (después de agregar propietario)
    if "apartamento_form_data" in request.session:
        data["form"] = ApartamentoForm(request.session["apartamento_form_data"])
        del request.session["apartamento_form_data"]

    if request.method == "POST":
        formulario = ApartamentoForm(data=request.POST)
        if formulario.is_valid():
            apartamento = formulario.save(commit=False)
            apartamento.edificio = edificio
            apartamento.save()
            apartamento = formulario.save(commit=False)
            apartamento.edificio = edificio
            apartamento.save()
            messages.success(request, "Apartamento agregado correctamente")
            return redirect(to="listar_apartamentos_edificio", edificio_id=edificio.id)
            return redirect(to="listar_apartamentos_edificio", edificio_id=edificio.id)
        else:
            print("Errores del formulario:", formulario.errors)  # Debug
            print("Datos del POST:", request.POST)  # Debug
            print("Errores del formulario:", formulario.errors)  # Debug
            print("Datos del POST:", request.POST)  # Debug
            data["form"] = formulario
            messages.error(request, "Por favor, corrige los errores en el formulario")

    return render(request, "app/apartamento/adicionar.html", data)


def listar_apartamentos_edificio(request, edificio_id):
    """Lista apartamentos de un edificio específico"""
    edificio = get_object_or_404(Edificio, id=edificio_id)
    apartamentos = edificio.apartamento_set.all().order_by("bloque", "piso", "nombre")
    page = request.GET.get("page", 1)
    try:
        paginator = Paginator(apartamentos, 10)
        apartamentos = paginator.page(page)
    except:
        raise Http404

    data = {
        "entity": apartamentos,
        "paginator": paginator,
        "edificio": edificio,
        "edificio": edificio,
    }
    return render(
        request,
        "app/apartamento/listar.html",
        data,
    )
    return render(
        request,
        "app/apartamento/listar.html",
        data,
    )


def detalle_apartamento(request, edificio_id, id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
    apartamento = get_object_or_404(Apartamento, id=id, edificio=edificio)

    # Obtener información relacionada
    propietario = apartamento.propietario
    movimientos = (
        propietario.movimientos.all().order_by("-fecha")[:5] if propietario else []
    )

    context = {
        "apartamento": apartamento,
        "edificio": edificio,
        "propietario": propietario,
        "movimientos": movimientos,
    }

    return render(request, "app/apartamento/detalle.html", context)


def modificar_apartamento(request, id, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
    apartamento = get_object_or_404(Apartamento, id=id)

    data = {
        "form": ApartamentoForm(instance=apartamento),
        "edificio": edificio,
        "apartamento": apartamento,
    }
    data = {
        "form": ApartamentoForm(instance=apartamento),
        "edificio": edificio,
        "apartamento": apartamento,
    }

    if request.method == "POST":
        formulario = ApartamentoForm(data=request.POST, instance=apartamento)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Apartamento modificado correctamente")
            return redirect(to="listar_apartamentos_edificio", edificio_id=edificio.id)
            return redirect(to="listar_apartamentos_edificio", edificio_id=edificio.id)
        else:
            data["form"] = formulario

    return render(request, "app/apartamento/modificar.html", data)


def eliminar_apartamento(request, id):
    apartamento = get_object_or_404(Apartamento, id=id)
    edificio_id = apartamento.edificio.id
    edificio_id = apartamento.edificio.id
    apartamento.delete()
    messages.success(request, "Apartamento eliminado correctamente")
    return redirect(to="listar_apartamentos_edificio", edificio_id=edificio_id)
    return redirect(to="listar_apartamentos_edificio", edificio_id=edificio_id)


def adicionar_propietario(request, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
def adicionar_propietario(request, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
    data = {
        "form": PropietarioForm(),
        "edificio": edificio,
        "edificio": edificio,
    }

    # Guardar la URL de retorno (desde donde se llamó al formulario)
    return_url = request.GET.get(
        "return_url", reverse("listar_propietarios_edificio", args=[edificio_id])
    )
    return_url = request.GET.get(
        "return_url", reverse("listar_propietarios_edificio", args=[edificio_id])
    )
    data["return_url"] = return_url

    if request.method == "POST":
        formulario = PropietarioForm(data=request.POST)
        if formulario.is_valid():
            propietario = formulario.save(commit=False)
            propietario.edificio = edificio
            propietario.save()
            propietario = formulario.save(commit=False)
            propietario.edificio = edificio
            propietario.save()

            # Si viene del formulario de apartamento, guardar datos y redirigir de vuelta
            if "apartamento" in return_url:
                # Guardar el ID del nuevo propietario para seleccionarlo automáticamente
                request.session["nuevo_propietario_id"] = propietario.dni

                messages.success(
                    request,
                    "Propietario agregado correctamente. Continue con el apartamento.",
                )
                return redirect(to="adicionar_apartamento", edificio_id=edificio_id)
                return redirect(to="adicionar_apartamento", edificio_id=edificio_id)
            else:
                messages.success(request, "Propietario agregado correctamente")
                return redirect(
                    to="listar_propietarios_edificio", edificio_id=edificio_id
                )
                return redirect(
                    to="listar_propietarios_edificio", edificio_id=edificio_id
                )
        else:
            data["form"] = formulario
            messages.error(request, "Por favor, corrige los errores en el formulario")

    return render(request, "app/propietario/adicionar.html", data)


def listar_propietarios_edificio(request, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
    propietarios = Propietario.objects.all()
    page = request.GET.get("page", 1)
    try:
        paginator = Paginator(propietarios, 10)
        propietarios = paginator.page(page)
    except:
        raise Http404

    data = {
        "entity": propietarios,
        "paginator": paginator,
        "edificio": edificio,
        "edificio": edificio,
    }
    return render(request, "app/propietario/listar.html", data)


def modificar_propietario(request, dni, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
def modificar_propietario(request, dni, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
    propietario = get_object_or_404(Propietario, dni=dni)

    data = {
        "form": PropietarioForm(instance=propietario),
        "edificio": edificio,
        "propietario": propietario,
    }
    data = {
        "form": PropietarioForm(instance=propietario),
        "edificio": edificio,
        "propietario": propietario,
    }

    if request.method == "POST":
        formulario = PropietarioForm(data=request.POST, instance=propietario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Propietario modificado correctamente")
            return redirect(to="listar_propietarios_edificio", edificio_id=edificio.id)
            return redirect(to="listar_propietarios_edificio", edificio_id=edificio.id)
        else:
            data["form"] = formulario
    print(data["form"].fields.keys())
    print(data["form"].fields.keys())
    return render(request, "app/propietario/modificar.html", data)


def detalle_propietario(request, dni, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
def detalle_propietario(request, dni, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
    propietario = get_object_or_404(Propietario, dni=dni)
    movimientos = MovimientoPropietario.objects.filter(
        propietario=propietario
    ).order_by("-fecha")
    apartamentos = propietario.apartamentos.all()
    apartamentos = propietario.apartamentos.all()
    total_movimientos = movimientos.count()
    total_entradas = movimientos.filter(tipo="entrada").count()
    total_salidas = movimientos.filter(tipo="salida").count()
    esta_en_propiedad = propietario.esta_en_propiedad
    tiene_movimientos = propietario.tiene_movimientos
    tiene_movimientos = propietario.tiene_movimientos
    ultimo_movimiento = movimientos.first() if total_movimientos > 0 else None
    deudas = 0.0
    for apt in apartamentos:
        if apt.adeudo:
            deudas += apt.cant_adeudo
        if apt.adeudo:
            deudas += apt.cant_adeudo

    data = {
        "edificio": edificio,
        "edificio": edificio,
        "propietario": propietario,
        "movimientos": movimientos,
        "total_movimientos": total_movimientos,
        "total_entradas": total_entradas,
        "total_salidas": total_salidas,
        "esta_en_propiedad": esta_en_propiedad,
        "tiene_movimientos": tiene_movimientos,
        "tiene_movimientos": tiene_movimientos,
        "ultimo_movimiento": ultimo_movimiento,
        "deudas": deudas,
        "apartamentos": apartamentos,
    }

    return render(request, "app/propietario/detalle.html", data)


def exportar_propietarios_excel(request):
    # Obtener todos los propietarios con sus relaciones
    propietarios = Propietario.objects.select_related("edificio").all()

    # Preparar los datos para el DataFrame
    data = []
    for prop in propietarios:
        data.append(
            {
                "DNI": prop.dni,
                "Nombre": prop.nombre,
                "Apellidos": prop.apellidos,
                "Nacionalidad": prop.nacionalidad,
                "Residente Inmobiliario": "Sí" if prop.residente_inmobiliario else "No",
                "Tiene Visa": "Sí" if prop.visa else "No",
                "Tipo de Visa": (
                    prop.get_tipo_visa_display() if prop.tipo_visa else "N/A"
                ),
                "Teléfono": prop.telefono,
                "Correo": prop.correo,
                "Edificio": prop.edificio.nombre if prop.edificio else "N/A",
                "Observaciones": prop.observaciones,
                "Es Representante": "Sí" if prop.representante else "No",
                "Representante Nombre": prop.rep_nombre or "N/A",
                "Representante Apellidos": prop.rep_apellidos or "N/A",
                "Representante DNI": prop.rep_dni or "N/A",
                "Representante Nacionalidad": prop.rep_nacionalidad or "N/A",
                "Representante Email": prop.rep_email or "N/A",
                "Representante Teléfono": prop.rep_telefono or "N/A",
            }
        )

    # Crear DataFrame
    df = pd.DataFrame(data)

    # Crear respuesta HTTP
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="propietarios.xlsx"'

    # Exportar a Excel
    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Propietarios", index=False)

        # Autoajustar el ancho de las columnas
        worksheet = writer.sheets["Propietarios"]
        for idx, col in enumerate(df.columns):
            max_length = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.column_dimensions[chr(65 + idx)].width = max_length

    return response


def exportar_propietarios_excel(request):
    # Obtener todos los propietarios con sus relaciones
    propietarios = Propietario.objects.select_related("edificio").all()

    # Preparar los datos para el DataFrame
    data = []
    for prop in propietarios:
        data.append(
            {
                "DNI": prop.dni,
                "Nombre": prop.nombre,
                "Apellidos": prop.apellidos,
                "Nacionalidad": prop.nacionalidad,
                "Residente Inmobiliario": "Sí" if prop.residente_inmobiliario else "No",
                "Tiene Visa": "Sí" if prop.visa else "No",
                "Tipo de Visa": (
                    prop.get_tipo_visa_display() if prop.tipo_visa else "N/A"
                ),
                "Teléfono": prop.telefono,
                "Correo": prop.correo,
                "Edificio": prop.edificio.nombre if prop.edificio else "N/A",
                "Observaciones": prop.observaciones,
                "Es Representante": "Sí" if prop.representante else "No",
                "Representante Nombre": prop.rep_nombre or "N/A",
                "Representante Apellidos": prop.rep_apellidos or "N/A",
                "Representante DNI": prop.rep_dni or "N/A",
                "Representante Nacionalidad": prop.rep_nacionalidad or "N/A",
                "Representante Email": prop.rep_email or "N/A",
                "Representante Teléfono": prop.rep_telefono or "N/A",
            }
        )

    # Crear DataFrame
    df = pd.DataFrame(data)

    # Crear respuesta HTTP
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="propietarios.xlsx"'

    # Exportar a Excel
    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Propietarios", index=False)

        # Autoajustar el ancho de las columnas
        worksheet = writer.sheets["Propietarios"]
        for idx, col in enumerate(df.columns):
            max_length = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.column_dimensions[chr(65 + idx)].width = max_length

    return response


def eliminar_propietario(request, dni):
    propietario = get_object_or_404(Propietario, dni=dni)
    edificio = propietario.edificio
    edificio = propietario.edificio
    propietario.delete()
    messages.success(request, "Propietario eliminado correctamente")
    return redirect(to="listar_propietarios_edificio", edificio_id=edificio.id)
    return redirect(to="listar_propietarios_edificio", edificio_id=edificio.id)


@csrf_exempt
@require_POST
def clear_session_propietario(request):
    if "nuevo_propietario_id" in request.session:
        del request.session["nuevo_propietario_id"]
    return JsonResponse({"status": "ok"})


def registrar_movimiento_propietario(request, dni, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
def registrar_movimiento_propietario(request, dni, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
    propietario = get_object_or_404(Propietario, dni=dni)

    if request.method == "POST":
        form = MovimientoPropietarioForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.propietario = propietario
            movimiento.save()

            messages.success(
                request,
                f"Movimiento registrado correctamente para {propietario.nombre}",
            )
            return redirect(to="listar_propietarios_edificio", edificio_id=edificio.id)
            return redirect(to="listar_propietarios_edificio", edificio_id=edificio.id)
    else:
        form = MovimientoPropietarioForm(initial={"fecha": timezone.now()})

    data = {
        "form": form,
        "entity": propietario,
        "titulo": "Registrar Movimiento",
        "edificio": edificio,
    }
    return render(request, "app/movimientos/agregar.html", data)


# arrendatarios


def adicionar_arrendatario(request, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
    data = {
        "form": ArrendatarioForm(),
        "edificio": edificio,
    }

    # Guardar la URL de retorno (desde donde se llamó al formulario)
    return_url = request.GET.get(
        "return_url", reverse("listar_arrendatarios_edificio", args=[edificio_id])
    )
    data["return_url"] = return_url

    if request.method == "POST":
        formulario = ArrendatarioForm(data=request.POST)
        if formulario.is_valid():
            arrendatario = formulario.save(commit=False)
            arrendatario.edificio = edificio
            arrendatario.save()

            # Si viene del formulario de apartamento, guardar datos y redirigir de vuelta
            if "apartamento" in return_url:
                # Guardar el ID del nuevo arrendatario para seleccionarlo automáticamente
                request.session["nuevo_arrendatario_id"] = arrendatario.dni

                messages.success(
                    request,
                    "Arrendatario agregado correctamente. Continue con el apartamento.",
                )
                return redirect(to="adicionar_apartamento", edificio_id=edificio_id)
            else:
                messages.success(request, "Arrendatario agregado correctamente")
                return redirect(
                    to="listar_arrendatarios_edificio", edificio_id=edificio_id
                )
        else:
            data["form"] = formulario
            messages.error(request, "Por favor, corrige los errores en el formulario")

    return render(request, "app/arrendatario/adicionar.html", data)


def listar_arrendatarios_edificio(request, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
    arrendatarios = Arrendatario.objects.all()
    page = request.GET.get("page", 1)
    try:
        paginator = Paginator(arrendatarios, 5)
        arrendatarios = paginator.page(page)
    except:
        raise Http404

    data = {
        "entity": arrendatarios,
        "paginator": paginator,
        "edificio": edificio,
    }
    return render(request, "app/arrendatario/listar.html", data)


def modificar_arrendatario(request, dni, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
    arrendatario = get_object_or_404(Arrendatario, dni=dni)

    data = {
        "form": ArrendatarioForm(instance=arrendatario),
        "edificio": edificio,
        "arrendatario": arrendatario,
    }

    if request.method == "POST":
        formulario = ArrendatarioForm(data=request.POST, instance=arrendatario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Arrendatario modificado correctamente")
            return redirect(to="listar_arrendatarios_edificio", edificio_id=edificio.id)
        else:
            data["form"] = formulario

    return render(request, "app/arrendatario/modificar.html", data)


def detalle_arrendatario(request, dni, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
    arrendatario = get_object_or_404(Arrendatario, dni=dni)
    movimientos = MovimientoArrendatario.objects.filter(
        arrendatario=arrendatario
    ).order_by("-fecha")
    apartamento = arrendatario.apartamento
    total_movimientos = movimientos.count()
    total_entradas = movimientos.filter(tipo="entrada").count()
    total_salidas = movimientos.filter(tipo="salida").count()
    esta_en_propiedad = arrendatario.esta_en_propiedad
    tiene_movimientos = arrendatario.tiene_movimientos
    ultimo_movimiento = movimientos.first() if total_movimientos > 0 else None

    data = {
        "edificio": edificio,
        "arrendatario": arrendatario,
        "movimientos": movimientos,
        "total_movimientos": total_movimientos,
        "total_entradas": total_entradas,
        "total_salidas": total_salidas,
        "esta_en_propiedad": esta_en_propiedad,
        "tiene_movimientos": tiene_movimientos,
        "ultimo_movimiento": ultimo_movimiento,
        "apartamento": apartamento,
    }

    return render(request, "app/arrendatario/detalle.html", data)


def eliminar_arrendatario(request, dni):
    arrendatario = get_object_or_404(Arrendatario, dni=dni)
    edificio = arrendatario.edificio
    arrendatario.delete()
    messages.success(request, "Arrendatario eliminado correctamente")
    return redirect(to="listar_arrendatarios_edificio", edificio_id=edificio.id)


@csrf_exempt
@require_POST
def clear_session_arrendatario(request):
    if "nuevo_arrendatario_id" in request.session:
        del request.session["nuevo_arrendatario_id"]
    return JsonResponse({"status": "ok"})


def registrar_movimiento_arrendatario(request, dni, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
    arrendatario = get_object_or_404(Arrendatario, dni=dni)

    if request.method == "POST":
        form = MovimientoArrendatarioForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.arrendatario = arrendatario
            movimiento.save()

            messages.success(
                request,
                f"Movimiento registrado correctamente para {arrendatario.nombre}",
            )
            return redirect(to="listar_arrendatarios_edificio", edificio_id=edificio.id)
    else:
        form = MovimientoArrendatarioForm(initial={"fecha": timezone.now()})

    data = {
        "form": form,
        "entity": arrendatario,
        "titulo": "Registrar Movimiento",
        "edificio": edificio,
    }
    return render(request, "app/movimientos/agregar.html", data)


# convivientes


def adicionar_conviviente(request, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
    data = {
        "form": ConvivienteForm(),
        "edificio": edificio,
    }

    # Guardar la URL de retorno (desde donde se llamó al formulario)
    return_url = request.GET.get(
        "return_url", reverse("listar_convivientes_edificio", args=[edificio_id])
    )
    data["return_url"] = return_url

    if request.method == "POST":
        formulario = ConvivienteForm(data=request.POST)
        if formulario.is_valid():
            conviviente = formulario.save(commit=False)
            conviviente.edificio = edificio
            conviviente.save()

            # Si viene del formulario de apartamento, guardar datos y redirigir de vuelta
            if "apartamento" in return_url:
                # Guardar el ID del nuevo conviviente para seleccionarlo automáticamente
                request.session["nuevo_conviviente_id"] = conviviente.dni

                messages.success(
                    request,
                    "Conviviente agregado correctamente. Continue con el apartamento.",
                )
                return redirect(to="adicionar_apartamento", edificio_id=edificio_id)
            else:
                messages.success(request, "Conviviente agregado correctamente")
                return redirect(
                    to="listar_convivientes_edificio", edificio_id=edificio_id
                )
        else:
            data["form"] = formulario
            messages.error(request, "Por favor, corrige los errores en el formulario")

    return render(request, "app/conviviente/adicionar.html", data)


def listar_convivientes_edificio(request, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
    convivientes = Conviviente.objects.all()
    page = request.GET.get("page", 1)
    try:
        paginator = Paginator(convivientes, 5)
        convivientes = paginator.page(page)
    except:
        raise Http404

    data = {
        "entity": convivientes,
        "paginator": paginator,
        "edificio": edificio,
    }
    return render(request, "app/conviviente/listar.html", data)


def modificar_conviviente(request, dni, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
    conviviente = get_object_or_404(Conviviente, dni=dni)

    data = {
        "form": ConvivienteForm(instance=conviviente),
        "edificio": edificio,
        "conviviente": conviviente,
    }

    if request.method == "POST":
        formulario = ConvivienteForm(data=request.POST, instance=conviviente)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Conviviente modificado correctamente")
            return redirect(to="listar_convivientes_edificio", edificio_id=edificio.id)
        else:
            data["form"] = formulario

    return render(request, "app/conviviente/modificar.html", data)


def detalle_conviviente(request, dni, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
    conviviente = get_object_or_404(Conviviente, dni=dni)
    movimientos = MovimientoConviviente.objects.filter(
        conviviente=conviviente
    ).order_by("-fecha")
    apartamento = conviviente.apartamento
    total_movimientos = movimientos.count()
    total_entradas = movimientos.filter(tipo="entrada").count()
    total_salidas = movimientos.filter(tipo="salida").count()
    esta_en_propiedad = conviviente.esta_en_propiedad
    tiene_movimientos = conviviente.tiene_movimientos
    ultimo_movimiento = movimientos.first() if total_movimientos > 0 else None

    data = {
        "edificio": edificio,
        "conviviente": conviviente,
        "movimientos": movimientos,
        "total_movimientos": total_movimientos,
        "total_entradas": total_entradas,
        "total_salidas": total_salidas,
        "esta_en_propiedad": esta_en_propiedad,
        "tiene_movimientos": tiene_movimientos,
        "ultimo_movimiento": ultimo_movimiento,
        "apartamento": apartamento,
    }

    return render(request, "app/conviviente/detalle.html", data)


def eliminar_conviviente(request, dni):
    conviviente = get_object_or_404(Conviviente, dni=dni)
    edificio = conviviente.edificio
    conviviente.delete()
    messages.success(request, "Conviviente eliminado correctamente")
    return redirect(to="listar_convivientes_edificio", edificio_id=edificio.id)


@csrf_exempt
@require_POST
def clear_session_conviviente(request):
    if "nuevo_conviviente_id" in request.session:
        del request.session["nuevo_conviviente_id"]
    return JsonResponse({"status": "ok"})


def registrar_movimiento_conviviente(request, dni, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
    conviviente = get_object_or_404(Conviviente, dni=dni)

    if request.method == "POST":
        form = MovimientoConvivienteForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.conviviente = conviviente
            movimiento.save()

            messages.success(
                request,
                f"Movimiento registrado correctamente para {conviviente.nombre}",
            )
            return redirect(to="listar_convivientes_edificio", edificio_id=edificio.id)
    else:
        form = MovimientoConvivienteForm(initial={"fecha": timezone.now()})

    data = {
        "form": form,
        "entity": conviviente,
        "titulo": "Registrar Movimiento",
        "edificio": edificio,
    }
    return render(request, "app/movimientos/agregar.html", data)


def panel_exportaciones(request, edificio_id):
    edificio = get_object_or_404(Edificio, id=edificio_id)
    data = {
        "edificio": edificio,
    }
    """Vista principal con los botones de exportación"""
    return render(request, "app/exportaciones/panel.html", data)


def exportar_estado_ocupacion_excel(request):
    # Obtener todos los propietarios con sus relaciones
    apartamentos = Apartamento.objects.select_related("edificio").all()

    # Preparar los datos para el DataFrame
    data = []
    for apto in apartamentos:
        propietario = apto.propietario
        convivientes = apto.convivientes.all()
        arrendatarios = apto.arrendatarios.all()
        if convivientes.exists() or arrendatarios.exists():
            for conv in convivientes:
                data.append(
                    {
                        "No. Apto": apto.nombre,
                        "Propietario": propietario.nombre + " " + propietario.apellidos,
                        "Ocupantes": conv.nombre + " " + conv.apellidos,
                        "No. Identidad": conv.dni,
                        "País": conv.nacionalidad.name,
                        "Tipo de Visado": (
                            conv.get_tipo_visa_display() if conv.tipo_visa else "N/A"
                        ),
                        "Permanencia": (
                            (
                                "Permanente"
                                if conv.esta_en_propiedad
                                else "Fuera del país"
                            )
                            if conv.tiene_movimientos
                            else "Desconocido"
                        ),
                        "Parentesco": "Conviviente",
                        "Observaciones": conv.observaciones,
                        # "Es Representante": "Sí" if prop.representante else "No",
                        # "Representante Nombre": prop.rep_nombre or "N/A",
                        # "Representante Apellidos": prop.rep_apellidos or "N/A",
                        # "Representante DNI": prop.rep_dni or "N/A",
                        # "Representante Nacionalidad": prop.rep_nacionalidad or "N/A",
                        # "Representante Email": prop.rep_email or "N/A",
                        # "Representante Teléfono": prop.rep_telefono or "N/A",
                    }
                )
            for arr in arrendatarios:
                data.append(
                    {
                        "No. Apto": apto.nombre,
                        "Propietario": propietario.nombre + " " + propietario.apellidos,
                        "Ocupantes": arr.nombre + " " + arr.apellidos,
                        "No. Identidad": arr.dni,
                        "País": arr.nacionalidad.name,
                        "Tipo de Visado": (
                            arr.get_tipo_visa_display() if arr.tipo_visa else "N/A"
                        ),
                        "Permanencia": (
                            (
                                "Permanente"
                                if arr.esta_en_propiedad
                                else "Fuera del país"
                            )
                            if arr.tiene_movimientos
                            else "Desconocido"
                        ),
                        "Parentesco": "Arrendatario",
                        "Observaciones": arr.observaciones,
                        # "Es Representante": "Sí" if prop.representante else "No",
                        # "Representante Nombre": prop.rep_nombre or "N/A",
                        # "Representante Apellidos": prop.rep_apellidos or "N/A",
                        # "Representante DNI": prop.rep_dni or "N/A",
                        # "Representante Nacionalidad": prop.rep_nacionalidad or "N/A",
                        # "Representante Email": prop.rep_email or "N/A",
                        # "Representante Teléfono": prop.rep_telefono or "N/A",
                    }
                )
        else:
            data.append(
                {
                    "No. Apto": apto.nombre,
                    "Propietario": propietario.nombre + " " + propietario.apellidos,
                    "Ocupantes": "N/A",
                    "No. Identidad": propietario.dni,
                    "País": propietario.nacionalidad.name,
                    "Tipo de Visado": (
                        propietario.get_tipo_visa_display()
                        if propietario.tipo_visa
                        else "N/A"
                    ),
                    "Permanencia": (
                        (
                            "Permanente"
                            if propietario.esta_en_propiedad
                            else "Fuera del país"
                        )
                        if propietario.tiene_movimientos
                        else "Desconocido"
                    ),
                    "Parentesco": "Propietario",
                    "Observaciones": propietario.observaciones,
                    # "Es Representante": "Sí" if prop.representante else "No",
                    # "Representante Nombre": prop.rep_nombre or "N/A",
                    # "Representante Apellidos": prop.rep_apellidos or "N/A",
                    # "Representante DNI": prop.rep_dni or "N/A",
                    # "Representante Nacionalidad": prop.rep_nacionalidad or "N/A",
                    # "Representante Email": prop.rep_email or "N/A",
                    # "Representante Teléfono": prop.rep_telefono or "N/A",
                }
            )

    # Crear DataFrame
    df = pd.DataFrame(data)

    # Crear respuesta HTTP
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    actual_date = datetime.now().strftime("%d/%m/%Y")
    filename = f"Estado de Ocupacion {actual_date}.xlsx"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    # Exportar a Excel
    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Ocupacion", index=False)

        # Autoajustar el ancho de las columnas
        worksheet = writer.sheets["Ocupacion"]
        for idx, col in enumerate(df.columns):
            max_length = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.column_dimensions[chr(65 + idx)].width = max_length

    return response


def exportar_propietarios_excel(request):
    propietarios = Propietario.objects.select_related("edificio").all()

    # Preparar los datos para el DataFrame
    data = []
    for prop in propietarios:
        apartamentos = prop.apartamentos.all()
        aptos = ", ".join([apto.nombre for apto in apartamentos])
        data.append(
            {
                "Nombre": prop.nombre,
                "Apellidos": prop.apellidos,
                "DNI": prop.dni,
                "Teléfono": prop.telefono,
                "Apartamentos": aptos,
                "Tiene Representante": "Sí" if prop.representante else "No",
                "Representante Nombre": prop.rep_nombre + " " + prop.rep_apellidos
                or "N/A",
                "Representante DNI": prop.rep_dni or "N/A",
                "Representante Teléfono": prop.rep_telefono or "N/A",
                "Representante Email": prop.rep_email or "N/A",
            }
        )

    # Crear DataFrame
    df = pd.DataFrame(data)

    # Crear respuesta HTTP
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        'attachment; filename="Listado de Propietarios.xlsx"'
    )

    # Exportar a Excel
    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Propietarios", index=False)

        # Autoajustar el ancho de las columnas
        worksheet = writer.sheets["Propietarios"]
        for idx, col in enumerate(df.columns):
            max_length = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.column_dimensions[chr(65 + idx)].width = max_length

    return response


def exportar_deuda_aptos_excel(request):
    apartamentos = Apartamento.objects.select_related("edificio").all()
    apartamentos = apartamentos.filter(adeudo=True)
    total_deudas = 0.0
    # Preparar los datos para el DataFrame
    data = []
    for apto in apartamentos:
        total_deudas += apto.cant_adeudo
        data.append(
            {
                "Apartamento": apto.nombre,
                "Propietario": apto.propietario.nombre
                + " "
                + apto.propietario.apellidos,
                "Deuda": apto.cant_adeudo,
                "Fecha Adeudo": apto.fecha_adeudo.strftime("%d/%m/%Y"),
            }
        )
    data.append(
        {
            "Apartamento": "Total deudas",
            "Propietario": "",
            "Deuda": total_deudas,
            "Fecha Adeudo": "",
        }
    )
    # Crear DataFrame
    df = pd.DataFrame(data)

    # Crear respuesta HTTP
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        'attachment; filename="Deudas por Apartamentos.xlsx"'
    )

    # Exportar a Excel
    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Deudas", index=False)

        # Autoajustar el ancho de las columnas
        worksheet = writer.sheets["Deudas"]
        for idx, col in enumerate(df.columns):
            max_length = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.column_dimensions[chr(65 + idx)].width = max_length

    return response


def exportar_deuda_propietarios_excel(request):
    propietarios = Propietario.objects.select_related("edificio").all()
    propietarios = propietarios.filter(apartamentos__adeudo=True).distinct()
    total_deudas = 0.0
    # Preparar los datos para el DataFrame
    data = []
    for prop in propietarios:
        apartamentos = prop.apartamentos.all().filter(adeudo=True)
        aptos = ", ".join([apto.nombre for apto in apartamentos])
        deuda = sum([apto.cant_adeudo for apto in apartamentos])
        total_deudas += deuda

        data.append(
            {
                "Propietario": prop.nombre + " " + prop.apellidos,
                "Apartamentos": aptos,
                "Total Deuda": deuda,
            }
        )
    data.append(
        {
            "Propietario": "Total deudas",
            "Apartamentos": "",
            "Total Deuda": total_deudas,
        }
    )
    # Crear DataFrame
    df = pd.DataFrame(data)

    # Crear respuesta HTTP
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        'attachment; filename="Deuda por Propietario.xlsx"'
    )

    # Exportar a Excel
    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Deudas", index=False)

        # Autoajustar el ancho de las columnas
        worksheet = writer.sheets["Deudas"]
        for idx, col in enumerate(df.columns):
            max_length = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.column_dimensions[chr(65 + idx)].width = max_length

    return response
