import calendar
import json
import random
#from turtle import home
import pandas as pd
from datetime import datetime, time, timedelta
from django.shortcuts import render, redirect

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, GroupManager, User
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.http import HttpResponse
import pandas as pd
import xlwt
from clientes.models import Clientes
from ventas.models import Ventas
from orden_compra.models import OrdenCompra, DetalleOrdenCompra
from insumos.models import Insumos
from ventas.models import Detalle_orden_venta
from categorias.models import Categorias
from productos.models import Producto

from registration.models import Profile
@login_required
def change_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password and password == confirm_password:
            user = request.user
            user.set_password(password)
            user.save()
            messages.success(request, 'Contraseña cambiada con éxito')
            return redirect('admin_main')  # Cambia 'admin_main' por la URL a la que quieres redirigir después de cambiar la contraseña
        else:
            messages.error(request, 'Las contraseñas no coinciden')

    template_name = 'administrator/password_change_form.html'  # Cambia 'password_change_form.html' por el nombre de tu plantilla
    return render(request, template_name)
@login_required
def view_user(request, user_id):
    user_data = User.objects.get(pk=user_id)
    profile_data = Profile.objects.get(user_id=user_id)
    groups = Group.objects.get(pk=profile_data.group_id) 
    template_name = 'administrator/view_user.html'
    return render(request, template_name, {'user_data': user_data, 'profile_data': profile_data, 'groups': groups})

@login_required
def admin_main(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'administrator/admin_main.html'
    total_clientes = Clientes.total_clientes()
    total_ordenes_venta = Detalle_orden_venta.total_ordenes_venta()
    total_insumos = Insumos.total_insumos()
    total_ordenes_compra = OrdenCompra.total_ordenes_compra()
    return render(request, template_name, {'profiles': profiles, 'total_clientes': total_clientes, 'total_ordenes_venta': total_ordenes_venta, 'total_insumos': total_insumos, 'total_ordenes_compra': total_ordenes_compra})




@login_required
def dashbo(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'dashboard/dashboard.html'
    

    prod = Producto.objects.all()
    cate = Categorias.objects.all()
    ord=Detalle_orden_venta.objects.all()
    ins=Insumos.objects.all()
    orde=DetalleOrdenCompra.objects.all()


    for a in cate:
        a.cantidad=0
        for b in prod:
            cat__del_prod=b.categoria
            id_de_cat__del_prod=cat__del_prod.id
            idcate=a.id
            if id_de_cat__del_prod==idcate:

                a.cantidad+=1
                a.save()

    for c in prod:
        c.can_sol=0
        for d in ord:
            prod_de_orden=d.producto
            id_de_prod_de_orden=prod_de_orden.id
            idprod=c.id
            if id_de_prod_de_orden==idprod:
                ca=d.cantidad
                c.can_sol+=ca
                c.save()


    for e in ins:
        e.can_sol=0
        for f in orde:
            insumo_de_orden=f.insumo
            id_de_insumo_de_orden=insumo_de_orden.id
            idprod=e.id
            if id_de_insumo_de_orden==idprod:
                ca=f.cantidad
                e.can_sol+=ca
                e.save()

    
    return render(request, template_name, {'profiles': profiles, 'prod':prod, 'cat':cate, 'ord':ord, 'ins':ins})






@login_required
def users_main(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tiene permisos')
        return redirect('check_group_main')
    
    groups = Group.objects.all().order_by('id')
    user_count = User.objects.count() 
    
    template_name = 'administrator/users_main.html'
    return render(request, template_name, {'groups': groups, 'profiles': profiles, 'user_count': user_count})


@login_required
def users_main(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tiene permisos')
        return redirect('check_group_main')
    
    groups = Group.objects.all().order_by('id')
    user_count = User.objects.count() 
    
    template_name = 'administrator/users_main.html'
    return render(request, template_name, {'groups': groups, 'profiles': profiles, 'user_count': user_count})


from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator

@login_required
def new_user(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        grupo = request.POST.get('grupo')
        rut = request.POST.get('rut')
        first_name = request.POST.get('name')
        last_name = request.POST.get('last_name1')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')

        rut_exist = User.objects.filter(username=rut).count()
        mail_exist = User.objects.filter(email=email).count()
        
        if rut_exist == 0:
            if mail_exist == 0:
                user = User.objects.create_user(
                    username=rut,
                    email=email,
                    password=rut,
                    first_name=first_name,
                    last_name=last_name,
                )
                
                
                current_site = get_current_site(request)
                mail_subject = 'Confirmación de creación de cuenta'
                message = render_to_string('emails/confirmation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                send_mail(mail_subject, message, 'uautonomachatgpt@gmail.com', [email])
                
                profile_save = Profile(
                    user_id=user.id,
                    group_id=grupo,
                    first_session='No',
                    token_app_session='No',
                )
                profile_save.save()
                
                messages.add_message(request, messages.INFO, 'Usuario creado con éxito y correo enviado al usuario')
            else:
                messages.add_message(request, messages.INFO, 'El correo que está tratando de ingresar, ya existe en nuestros registros')
        else:
            messages.add_message(request, messages.INFO, 'El nombre de usuario que está tratando de ingresar, ya existe en nuestros registros')

    groups = Group.objects.all().order_by('id')
    template_name = 'administrator/new_user.html'
    return render(request, template_name, {'groups': groups})


@login_required
def list_main(request,group_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    group = Group.objects.get(pk=group_id)
    template_name = 'administrator/list_main.html'
    return render(request,template_name,{'group':group,'profiles':profiles})

@login_required
def edit_user(request,user_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        grupo = request.POST.get('grupo')
        user_id = request.POST.get('user_id')
        first_name = request.POST.get('name')
        last_name = request.POST.get('last_name1')
        email = request.POST.get('email')
        group = request.POST.get('group')
        user_data_count = User.objects.filter(pk=user_id).count()
        user_data = User.objects.get(pk=user_id)
        profile_data = Profile.objects.get(user_id=user_id)    
        if user_data_count == 1:
            if user_data.email != email:
                user_mail_count_all = User.objects.filter(email=email).count()
                if user_mail_count_all > 0:
                    messages.add_message(request, messages.INFO, 'El correo '+str(email)+' ya existe en nuestros registros asociado a otro usuario, por favor utilice otro ')                             
                    return redirect('list_user_active',grupo,page)
            User.objects.filter(pk = user_id).update(first_name = first_name)
            User.objects.filter(pk = user_id).update(last_name = last_name)  
            User.objects.filter(pk = user_id).update(email = email)  
            Profile.objects.filter(user_id = user_id).update(group_id = group)                
            messages.add_message(request, messages.INFO, 'Usuario '+user_data.first_name +' '+user_data.last_name+' editado con éxito')                             
            return redirect('list_user_active',grupo)
        else:
            messages.add_message(request, messages.INFO, 'Hubo un error al editar el Usuario '+user_data.first_name +' '+user_data.last_name)
            return redirect('list_user_active',profile_data.group_id)   
         
    user_data = User.objects.get(pk=user_id)
    profile_data = Profile.objects.get(user_id=user_id)
    groups = Group.objects.get(pk=profile_data.group_id) 
    profile_list = Group.objects.all().exclude(pk=0).order_by('name')    
    template_name = 'administrator/edit_user.html'
    return render(request,template_name,{'user_data':user_data,'profile_data':profile_data,'groups':groups,'profile_list':profile_list})

@login_required    
def list_user_active(request,group_id,page=None):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if page == None:
        page = request.GET.get('page')
    else:
        page = page
    if request.GET.get('page') == None:
        page = page
    else:
        page = request.GET.get('page')
    group = Group.objects.get(pk=group_id)
    user_all = []
    user_array = User.objects.filter(is_active='t').filter(profile__group_id=group_id).order_by('first_name')
    for us in user_array:
        profile_data = Profile.objects.get(user_id=us.id)
        name = us.first_name+' '+us.last_name
        user_all.append({'id':us.id,'user_name':us.username,'name':name,'mail':us.email})
    paginator = Paginator(user_all, 30)  
    user_list = paginator.get_page(page)
    template_name = 'administrator/list_user_active.html'
    return render(request,template_name,{'profiles':profiles,'group':group,'user_list':user_list,'paginator':paginator,'page':page})
@login_required    
def list_user_block(request,group_id,page=None):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if page == None:
        page = request.GET.get('page')
    else:
        page = page
    if request.GET.get('page') == None:
        page = page
    else:
        page = request.GET.get('page')
    group = Group.objects.get(pk=group_id)
    user_all = []
    user_array = User.objects.filter(is_active='f').filter(profile__group_id=group_id).order_by('first_name')
    for us in user_array:
        profile_data = Profile.objects.get(user_id=us.id)
        name = us.first_name+' '+us.last_name
        user_all.append({'id':us.id,'user_name':us.username,'name':name,'mail':us.email})
    paginator = Paginator(user_all, 30)  
    user_list = paginator.get_page(page)
    template_name = 'administrator/list_user_block.html'
    return render(request,template_name,{'profiles':profiles,'group':group,'user_list':user_list,'paginator':paginator,'page':page})
@login_required
def user_block(request,user_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    user_data_count = User.objects.filter(pk=user_id).count()
    user_data = User.objects.get(pk=user_id)
    profile_data = Profile.objects.get(user_id=user_id)       
    if user_data_count == 1:
        User.objects.filter(pk=user_id).update(is_active='f')
        messages.add_message(request, messages.INFO, 'Usuario '+user_data.first_name +' '+user_data.last_name+' bloqueado con éxito')
        return redirect('list_user_active',profile_data.group_id)        
    else:
        messages.add_message(request, messages.INFO, 'Hubo un error al bloquear el Usuario '+user_data.first_name +' '+user_data.last_name)
        return redirect('list_user_active',profile_data.group_id)        
@login_required
def user_activate(request,user_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    user_data_count = User.objects.filter(pk=user_id).count()
    user_data = User.objects.get(pk=user_id)
    profile_data = Profile.objects.get(user_id=user_id)       
    if user_data_count == 1:
        User.objects.filter(pk=user_id).update(is_active='t')
        messages.add_message(request, messages.INFO, 'Usuario '+user_data.first_name +' '+user_data.last_name+' activado con éxito')
        return redirect('list_user_block',profile_data.group_id)        
    else:
        messages.add_message(request, messages.INFO, 'Hubo un error al activar el Usuario '+user_data.first_name +' '+user_data.last_name)
        return redirect('list_user_block',profile_data.group_id)        

@login_required
def user_delete(request,user_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    user_data_count = User.objects.filter(pk=user_id).count()
    user_data = User.objects.get(pk=user_id)
    profile_data = Profile.objects.get(user_id=user_id)       
    if user_data_count == 1:
        #Profile.objects.filter(user_id=user_id).delete()
        Profile.objects.filter(user_id=user_id).delete()
        User.objects.filter(pk=user_id).delete()
        messages.add_message(request, messages.INFO, 'Usuario '+user_data.first_name +' '+user_data.last_name+' eliminado con éxito')
        return redirect('list_user_block',profile_data.group_id)        
    else:
        messages.add_message(request, messages.INFO, 'Hubo un error al eliminar el Usuario '+user_data.first_name +' '+user_data.last_name)
        return redirect('list_user_block',profile_data.group_id)     
#CARGA MASIVA
@login_required
def carga_masiva_users(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'administrator/carga_masiva_users.html'
    return render(request,template_name,{'profiles':profiles})


@login_required
def import_file_users(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="archivo_importacion.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('carga_masiva')
    row_num = 0
    columns = ['Nombre', 'Correo', 'Grupo']
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/MM/yyyy'
    for row in range(1):
        row_num += 1
        for col_num in range(3):
            if col_num == 0:
                ws.write(row_num, col_num, 'ej: Andres', font_style)
            elif col_num == 1:
                ws.write(row_num, col_num, 'Andres@gmail.com', font_style)
            elif col_num == 2:
                ws.write(row_num, col_num, 'Nombre del Grupo', font_style)
    wb.save(response)
    return response


@login_required
def carga_masiva_users_save(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        data = pd.read_excel(request.FILES['myfile'])
        df = pd.DataFrame(data)
        acc = 0
        for item in df.itertuples():
            nombre = str(item[1])
            correo = str(item[2])
            nombre_grupo = str(item[3])
            try:
                grupo = Group.objects.get(name=nombre_grupo)
            except Group.DoesNotExist:
                messages.add_message(request, messages.ERROR, f'El grupo "{nombre_grupo}" no existe')
                continue
            user = User.objects.create_user(
                username=nombre,
                email=correo,
            )
            profile = Profile.objects.create(user=user, group=grupo)
            acc += 1
        messages.add_message(request, messages.INFO, f'Carga masiva finalizada, se importaron {acc} registros')
        return redirect('carga_masiva_users')
