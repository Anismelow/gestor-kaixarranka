from decimal import Decimal
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .forms import *
from .models import Horas, Adelanto


def inicio_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('panel') 
            else:
                return redirect('home')  
        else:
            error = "Nombre de usuario o contraseña incorrectos"
            return render(request, 'login.html', {'error': error})
    
    return render(request, 'login.html')


@login_required
def view_home(request):
    horas = Horas.objects.filter(usuario=request.user).order_by('fecha')
    adelanto = Adelanto.objects.filter(usuario=request.user).order_by('fecha_solicitud')
    
    total_horas = sum(h.horas_laboradas.total_seconds() for h in horas)
    total_adelanto = sum(a.monto for a in adelanto)
    total_adelanto = float(total_adelanto)
    total_euros_menos_adelanto = round(total_horas / 3600 * 8.125 - total_adelanto, 2)
    return render(request, 'index.html', {
        'horas': horas,
        'adelanto': adelanto,
        'total_horas': total_horas / 3600,  # Convertir segundos a horas
        'total_adelanto': total_adelanto,
        'euros': total_horas / 3600 * 8.125,
        'euros_menos_adelanto': total_euros_menos_adelanto
    })

@login_required
def horas_detail(request):
    if request.method == 'POST':
        form = HorasForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            hora_entrada = form.cleaned_data['hora_entrada']
            hora_salida = form.cleaned_data['hora_salida']

            horas = Horas(
                usuario=request.user,
                fecha=fecha,
                hora_entrada=hora_entrada,
                hora_salida=hora_salida
            )
            horas.save()
            return redirect('home')
    else:
        form = HorasForm()

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
            adelanto.save()  
            return redirect('home')  
    else:
        form = AdelantoForm()  
    return render(request, 'adelanto/adelanto_detail.html', {'form': form})



def cerrar_sesion(request):
    logout(request) 
    return redirect('login') 


# views.py
@login_required
def register(request):
    if request.method == 'POST':
        # Verifica si el usuario actual es miembro del staff
        if request.user.is_staff:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)  # Inicia sesión automáticamente con el nuevo usuario
                messages.success(request, 'Usuario registrado y conectado exitosamente.')
                return redirect('home')
        else:
            messages.error(request, 'No tienes permiso para registrar nuevos usuarios.')
            return redirect('home')  # Vuelve a la página principal
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})





@login_required
def admin_login(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

    trabajadores = User.objects.filter(is_staff=False)
    datos_trabajadores = []

    for trabajador in trabajadores:
        horas = Horas.objects.filter(usuario=trabajador).order_by('fecha')
        adelantos = Adelanto.objects.filter(usuario=trabajador)
        
        total_horas = sum(hora.horas_laboradas.total_seconds() for hora in horas) / 3600
        total_adelanto = sum(adelanto.monto for adelanto in adelantos)
    
        euros = total_horas * 8.125
        
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


def eliminar_horas(request, id):
    try:
        horas = Horas.objects.get(id=id)
        horas.delete()
        messages.success(request, 'Eliminado exitosamente.')
    except Horas.DoesNotExist:
        messages.error(request, 'El objeto no existe.')
    except Exception as e:
        messages.error(request, f'Ocurrió un error: {str(e)}')

    return redirect('home')

def eliminar_adelanto(request, id):
    try:
        adelanto = Adelanto.objects.get(id=id)
        adelanto.delete()
        messages.success(request, 'Eliminado exitosamente.')
    except Adelanto.DoesNotExist:
        messages.error(request, 'El objeto no existe.')
    except Exception as e:
        messages.error(request, f'Ocurrió un error: {str(e)}')

    return redirect('home')



def editar_horas(request, id):
    horas = get_object_or_404(Horas, id=id)

    if request.method == 'POST':
        form = HorasForm(request.POST, instance=horas)
        if form.is_valid():
            form.save()
            # Mensaje de éxito opcional
            messages.success(request, 'Actualizado exitosamente.')
            return redirect('home')
    else:
        form = HorasForm(instance=horas)

    return render(request, 'horas/edit_horas.html', {'form': form})