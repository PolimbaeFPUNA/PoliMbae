import os

def poblacion():
	add_usuario('admin','admin','admin@gmail.com','admin','adminadmin','san lorenzo','575757',1,'4503400')
	add_usuario('luis','Luis','luis@gmail.com','romero','123456','asuncion','585858',2,'4440004')
	add_usuario('teresa','Teresa','tere@gmail.com','cabrera','123456','aregua','121212',1,'5454454')
	add_usuario('fatima','Fatima','faty@gmail.com','cabrera','123456','aregua','575757',1,'5043433')

	add_usuario_pendiente('guido', 'guido', 'guiv07@gmail.com', 'franco', '123456', 'aregua', '4099999', 1, '4940564')

	add_rol('administrador general')
	add_rol_recursos('administrador de recursos')
	add_rol_usuario_autenticado('usuario')

	add_rol_usuario('admin','administrador general')
	add_rol_usuario('luis','administrador de recursos')
	add_rol_usuario('fatima','usuario')

	add_tipo_recurso('notebook',True)
	add_tipo_recurso('proyector',True)
	add_tipo_recurso('impresora', True)
	add_tipo_recurso('aula', True)

	add_recurso('notebook','nb1')
	add_recurso('notebook','nb2')
	add_recurso('proyector','pr1')
	add_recurso('proyector','pr2')
	add_recurso('proyector','pr3')
	add_recurso('impresora', 'impresora n1')
	add_recurso('impresora', 'impresora n2')
	add_recurso('aula', 'aula A55')
	add_recurso('aula', 'aula F36')
	add_recurso('aula', 'aula C11')
	add_recurso('aula', 'aula A58')
	add_recurso('aula', 'aula A50')

	add_mantenimiento('pr1','proyector','2017-07-02','2017-07-04','10:00','11:00','preventivo')
	add_mantenimiento('pr3', 'proyector', '2017-07-05', '2017-07-06', '12:00', '16:00', 'preventivo')
	add_mantenimiento('nb2', 'notebook', '2017-07-02', '2017-07-04', '10:00', '11:00', 'correctivo')
	add_mantenimiento('nb1', 'notebook', '2017-07-02', '2017-07-04', '10:00', '11:00', 'preventivo')
	add_mantenimiento('aula A55', 'aula', '2017-07-12', '2017-07-14', '08:00', '11:00', 'preventivo')

	add_solicitud('pr1','2017-06-06', '10:00', '11:15','admin')
	add_solicitud('aula A55', '2017-06-05', '8:00', '9:15', 'luis')
	add_solicitud('nb2', '2017-06-04', '15:00', '18:45', 'fatima')
	add_solicitud('nb2', '2017-06-07', '15:00', '18:45', 'fatima')

	add_reserva('2017-06-03', '22:00', '22:45', 'fatima','aula A55')
	add_reserva('2017-06-03', '10:00', '12:35', 'admin', 'pr1')
	add_reserva('2017-06-03', '09:15', '11:45', 'luis', 'aula A55')
	add_reserva('2017-06-03', '10:00', '12:35', 'fatima', 'nb2')
	
def add_usuario(username,first_name,email,last_name,password,direccion,telefono,categoria,cedula):
	try:
		user=User.objects.get(username=username)
	except User.DoesNotExist:
		user=User.objects.create_user(username=username,first_name=first_name,email=email,last_name=last_name,password=password)
		user.save()
		pro=Profile.objects.create(user=user,direccion=direccion,telefono=telefono,categoria=categoria,cedula=cedula)
		pro.save()
	return user

def add_usuario_pendiente(username,first_name,email,last_name,password,direccion,telefono,categoria,cedula):
	try:
		user=User.objects.get(username=username)
	except User.DoesNotExist:
		user=User.objects.create_user(username=username,first_name=first_name,email=email,last_name=last_name,password=password,is_active=False)
		user.save()
		pro=Profile.objects.create(user=user,direccion=direccion,telefono=telefono,categoria=categoria,cedula=cedula)
		pro.save()
	return user

def add_rol_recursos(nombre):
	
	p=Permission.objects.get(codename='add_recurso1')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p=Permission.objects.get(codename='change_recurso1')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p=Permission.objects.get(codename='delete_recurso1')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p=Permission.objects.get(codename='add_tiporecurso1')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p=Permission.objects.get(codename='change_tiporecurso1')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p=Permission.objects.get(codename='delete_tiporecurso1')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p=Permission.objects.get(codename='add_caracteristica')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p=Permission.objects.get(codename='change_caracteristica')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p=Permission.objects.get(codename='delete_caracteristica')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p=Permission.objects.get(codename='add_descripcarac')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p=Permission.objects.get(codename='change_descripcarac')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p=Permission.objects.get(codename='delete_descripcarac')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p = Permission.objects.get(codename='add_mantenimiento')
	d, grupo = Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p = Permission.objects.get(codename='change_mantenimiento')
	d, grupo = Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p = Permission.objects.get(codename='delete_mantenimiento')
	d, grupo = Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)

	d.save()
	return grupo

def add_rol_usuario_autenticado(nombre):
	
	p=Permission.objects.get(codename='add_profile')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p=Permission.objects.get(codename='change_profile')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)

	p=Permission.objects.get(codename='add_user')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p=Permission.objects.get(codename='change_user')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)

	p=Permission.objects.get(codename='add_solicitud')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)

	p=Permission.objects.get(codename='add_reserva')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	d.save()
	return grupo


def add_rol(nombre):
	p=Permission.objects.all()
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.set(p)
	d.save()
	return grupo

def add_rol_usuario(user,rol):
	user=User.objects.get(username=user)
	grupo=Group.objects.get(name=rol)
	grupo.user_set.add(user)
	return grupo

def add_tipo_recurso(nombre,reservable):
	try:
		tipo = TipoRecurso1.objects.get(nombre_recurso=nombre)
	except TipoRecurso1.DoesNotExist:
		tipo = TipoRecurso1.objects.create(nombre_recurso=nombre, reservable=reservable)
		tipo.save()
	return tipo

def add_recurso(tipo,descripcion):
	try:
		recurso=Recurso1.objects.get(descripcion=descripcion)
	except Recurso1.DoesNotExist:
		t=TipoRecurso1.objects.get(nombre_recurso=tipo)
		recurso=Recurso1.objects.create(tipo_id=t,descripcion=descripcion)
		recurso.save()
	return recurso

def add_mantenimiento(recurso,tipo,fechae,fechaf,horae,horaf,tipom):
	try:
		rec=Recurso1.objects.get(descripcion=recurso)
		mant=Mantenimiento.objects.get(recurso=rec.recurso_id)
	except Mantenimiento.DoesNotExist:
		rec=Recurso1.objects.get(descripcion=recurso)
		t=TipoRecurso1.objects.get(nombre_recurso=tipo)
		mant=Mantenimiento.objects.create(recurso=rec,tipo_recurso=t, fecha_entrega=fechae,
									 fecha_fin=fechaf, hora_entrega=horae,
									 hora_fin=horaf,tipo=tipom)
		mant.save()
	return mant

def add_solicitud(recurso,fecha,hora_inicio,hora_fin,usuario):
	rec = Recurso1.objects.get(descripcion=recurso)
	usu = Profile.objects.get(user__username=usuario)
	sol = Solicitud.objects.create(recurso=rec, usuario=usu,fecha_reserva=fecha,
									   hora_inicio=hora_inicio, hora_fin=hora_fin)
	sol.save()
	return sol

def add_reserva(fecha,horai,horaf,usuario,recurso):
	rec = Recurso1.objects.get(descripcion=recurso)
	usu = Profile.objects.get(user__username=usuario)
	reserva=Reserva.objects.create(fecha_reserva=fecha, hora_inicio=horai, hora_fin=horaf,
						   usuario=usu, recurso_reservado=rec, estado_reserva='CONFIRMADA')
	reserva.save()
	return reserva

if __name__=='__main__':
	print "poblando"
	os.environ.setdefault('DJANGO_SETTINGS_MODULE','PoliMbae.settings')
	import django
	django.setup()
	from app.usuario.models import Profile
	from django.contrib.auth.models import User,Group,Permission
	from app.recurso_pr.models import Recurso1,TipoRecurso1,Caracteristica
	from app.mantenimiento.models import Mantenimiento
	from app.reserva_new.models import Solicitud, Reserva

	poblacion()

