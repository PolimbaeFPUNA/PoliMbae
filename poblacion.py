import os

def poblacion():
	add_usuario('dana','Dana','dana@gmail.com','cabrera','123456','aregua','575757','funcionario','5002345')
	add_usuario('luis','Luis','luis@gmail.com','romero','123456','asuncion','585858',2,'4440004')
	add_usuario('teresa','Teresa','tere@gmail.com','cabrera','123456','aregua','121212',1,'5454454')
	add_usuario('fatima','Fatima','faty@gmail.com','cabrera','123456','aregua','575757','Adjunto','5043433')

	add_rol('admin2')
	add_rol_recursos('administrador de recursos')
	add_rol_usuario_autenticado('usuario')

	add_rol_usuario('dana','admin2')
	add_rol_usuario('luis','administrador de recursos')
	add_rol_usuario('fatima','usuario')
	
def add_usuario(username,first_name,email,last_name,password,direccion,telefono,categoria,cedula):
	try:
		user=User.objects.get(username=username)
	except User.DoesNotExist:
		user=User.objects.create_user(username=username,first_name=first_name,email=email,last_name=last_name,password=password)
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

	p=Permission.objects.get(codename='add_listareservaespecifica')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p=Permission.objects.get(codename='change_listareservaespecifica')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p=Permission.objects.get(codename='delete_listareservaespecifica')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)

	p=Permission.objects.get(codename='add_listareservageneral')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p=Permission.objects.get(codename='change_listareservageneral')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p=Permission.objects.get(codename='delete_listareservageneral')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)

	p=Permission.objects.get(codename='delete_reservaespecifica')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p=Permission.objects.get(codename='delete_reservaespecifica')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p=Permission.objects.get(codename='delete_reservaespecifica')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)

	p=Permission.objects.get(codename='delete_reservageneral')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p=Permission.objects.get(codename='delete_reservageneral')
	d,grupo=Group.objects.get_or_create(name=nombre)
	d.permissions.add(p)
	p=Permission.objects.get(codename='delete_reservageneral')
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

if __name__=='__main__':
	print "poblando"
	os.environ.setdefault('DJANGO_SETTINGS_MODULE','PoliMbae.settings')
	import django
	django.setup()
	from app.usuario.models import Profile
	from django.contrib.auth.models import User,Group,Permission

	poblacion()

