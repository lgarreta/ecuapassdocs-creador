# tables.py
import django_tables2 as tables
from django_tables2.utils import A
from .models import CustomUser

class UserTable(tables.Table):
	username = tables.LinkColumn ('actualizar', args=[A('pk')])  # Assuming 'actualizar' is your URL pattern name
	#email = tables.LinkColumn('user_email_detail', args=[A('pk')])

	# Columna adicional de "acciones" que se presenta al listar los usuarios
	columnaAcciones = tables.TemplateColumn(
		template_code='''
		(<a href="{{ record.get_link_actualizar }}">{{ record.get_link_actualizar_display }}</a>),
		(<a href="{{ record.get_link_eliminar }}">{{ record.get_link_eliminar_display }}</a>)
		''',
		verbose_name='Acciones'
	)
	class Meta:
		model = CustomUser
		template_name = "django_tables2/bootstrap4.html"
		fields = ("username", "email", "first_name", "last_name", "columnaAcciones")
		attrs = {'class': 'table table-striped table-bordered'}		

