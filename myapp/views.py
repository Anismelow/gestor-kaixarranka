from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required,user_passes_test

from .forms import *
from .models import Horas, Adelanto


def inicio_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                return redirect('panel')  # Redirige al panel de administración si es staff
            else:
                login(request, user)
                return redirect('home')  # Redirige a la página de inicio u otra página
        else:
            error = "Nombre de usuario o contraseña incorrectos"
            return render(request, 'login.html', {'error': error})
    
    return render(request, 'login.html')
@login_required
def view_home(request):
    # Filtrar las instancias de Horas y Adelanto para el usuario autenticado
    horas = Horas.objects.filter(usuario=request.user)
    adelanto = Adelanto.objects.filter(usuario=request.user)
    
    # Calcular los totales
    total_horas = sum(h.horas_laboradas.total_seconds() for h in horas)
    total_adelanto = sum(a.monto for a in adelanto)


    return render(request, 'index.html', {
        'horas': horas,
        'adelanto': adelanto,
        'total_horas': total_horas / 3600,  # Convertir segundos a horas
        'total_adelanto': total_adelanto,
        'euros':total_horas / 3600 * 8.125
    })


@login_required
def horas_detail(request):
    if request.method == 'POST':
        form = HorasForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            hora_entrada = form.cleaned_data['hora_entrada']
            hora_salida = form.cleaned_data['hora_salida']

            # Crear una instancia del modelo Horas y guardarla
            horas = Horas(
                usuario=request.user,  # Asignar el usuario actual
                fecha=fecha,
                hora_entrada=hora_entrada,
                hora_salida=hora_salida
            )
            horas.save()  # Guardar la instancia en la base de datos

            return redirect('home')  # Redirigir a la vista 'home'

    else:
        form = HorasForm()  # Mostrar un formulario vacío si la solicitud no es POST

    return render(request, 'horas/horas_detail.html', {'form': form})

@login_required
def adelanto_detail(request):
    if request.method == 'POST':
        form = AdelantoForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data['fecha_solicitud']
            monto = form.cleaned_data['monto']
            # Crear una instancia del modelo Adelanto y guardarla
            adelanto = Adelanto(
                usuario=request.user,  # Asignar el usuario actual
                fecha_solicitud=fecha,
                monto=monto
            )
            adelanto.save()  # Guardar la instancia en la base de datos
            return redirect('home')  # Redirigir a la vista 'home'
    else:
        form = AdelantoForm()  # Mostrar un formulario vacío si la solicitud no es POST
    return render(request, 'adelanto/adelanto_detail.html', {'form': form})



def cerrar_sesion(request):
    logout(request)  # Cerrar la sesión del usuario
    return redirect('login')  # Redirigir a la vista de inicio de sesión


# views.py
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login the user after registration
            return redirect('home')  # Redirect to a success page
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


from dataclasses import dataclass


@dataclass
class TrabajadorData:
    username: str
    fecha: str
    hora_entrada: str
    hora_salida: str
    horas_laboradas: float
    horas_totales: float
    adelanto: float
    total_adelanto: float
    euros: float


def admin_login(request):
    trabajadores = User.objects.filter(is_staff=False)  # Obtener usuarios que no son staff
    
    datos_trabajadores = []

    for trabajador in trabajadores:
        horas = Horas.objects.filter(usuario=trabajador)
        adelantos = Adelanto.objects.filter(usuario=trabajador)
        
        total_horas = sum(hora.horas_laboradas.total_seconds() for hora in horas) / 3600
        total_adelanto = sum(adelanto.monto for adelanto in adelantos)
    
        euros = total_horas * 8.125  # Calcula el total de euros
        
        datos_trabajadores.append({
            'username': trabajador.username,
            'horas': horas,
            'total_horas': total_horas,
            'total_adelanto': total_adelanto,
            'euros': euros,
        })
    
    return render(request, 'panel.html', {
        'datos_trabajadores': datos_trabajadores,
    })