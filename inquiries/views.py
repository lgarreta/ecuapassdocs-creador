from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from inquiries.models import AcademicRequests,AdministrativeRequests

# Academic Requests views

class AcademicRequestsCreateView(CreateView):
	model = AcademicRequests
	fields = ['subject', 'body', 'receiver', 'reply']
	template_name = 'inquiries/academic_requests_details.html'
	
	def form_valid(self, form):
		# Attach the current request to the form instance before saving
		form.instance.sender = self.request.user
		return super().form_valid(form)
	
	# reverse returns the string url path 
	def get_success_url(self):
		return reverse_lazy('academicrequests-list')
	
	# Adds a table title to the context by calling the Parent's class get.context_data and extending it
	# Parent Class in this case is CreateView
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['table_title'] = 'Add New Academic Request'

		return context
	
	def get_form(self, form_class=None):
		form = super().get_form(form_class)

		# Check if the user is a student
		if self.request.user.es_externo():
			# Make the 'reply' field read-only for students so that the field can still be submitted
			form.fields['reply'].widget.attrs['readonly'] = True

		return form

class AcademicRequestsUpdateView(UpdateView):
	model = AcademicRequests
	fields = ['subject', 'body','receiver', 'reply']
	template_name = 'inquiries/academic_requests_details.html'
	def get_success_url(self):
		
		return reverse_lazy('academicrequests-list')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['table_title'] = 'Update Academic Request'

		return context
	
	def get_form(self, form_class=None):
		form = super().get_form(form_class)

		# Check if the user is a student
		if self.request.user.es_externo() or self.request.user.es_director():
			# Make the 'reply' field read-only for students and teamleads, so that the field can still be submitted
			form.fields['reply'].widget.attrs['readonly'] = True

		return form

class AcademicRequestsListView(LoginRequiredMixin,ListView):
	model = AcademicRequests
	
	# The context object name will be used in the templates to query the academic requests
	context_object_name = 'academic_requests'	 
	template_name = 'inquiries/academic_requests_list.html'
	paginate_by = 5
	
	def get_queryset(self):
		
	   # Get the currently logged-in user
		user = self.request.user

		# If the user is a student, filter academic requests sent by the student
		if user.es_externo():
			return AcademicRequests.objects.filter(sender=user)
		
		# If the user is a facilitator, filter academic requests where the receiver is the facilitator
		elif user.es_funcionario():
			return AcademicRequests.objects.filter(receiver=user)

		elif user.es_director:
			# If the user is a team lead, return all academic requests
			return AcademicRequests.objects.all()
		
	
class AcademicRequestsDeleteView(DeleteView):
	model = AcademicRequests
	template_name = 'inquiries/confirm_delete.html'

	def get_success_url(self):		
		return reverse_lazy('academicrequests-list')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Delete Academic Request'
		# Retrieves the subject of the academicrequest we want to delete
		academic_request_subject = AcademicRequests.objects.get(pk=self.kwargs.get('pk')).subject
		context['message'] = f'Are you sure you want to delete this academic request : "{academic_request_subject}"'
		# Display a cancel button on confirmation page and if pressed, return user to the academicrequests list
		context['cancel_url'] = 'academicrequests-list'
		return context 
	

#-------------------------------------------------------------------------------------------------------------------------------

# Administrative Requests Views 

class AdministrativeRequestsCreateView(CreateView):
	model = AdministrativeRequests
	fields = ['subject', 'body', 'receiver', 'reply']
	template_name = 'inquiries/admin_requests_details.html'
	
	def form_valid(self, form):
		# Attach the current request to the form instance before saving
		form.instance.sender = self.request.user
		return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy('administrativerequests-list')
	
	# Adds a table title to the context by calling the Parent's class get.context_data and extending it
	# Parent Class in this case is CreateView
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['table_title'] = 'Add New Administrative Request'
		return context
	
	def get_form(self, form_class=None):
		form = super().get_form(form_class)

		# Check if the user is a student
		if self.request.user.es_externo():
			# Make the 'reply' field read-only for students so that the field can still be submitted
			form.fields['reply'].widget.attrs['readonly'] = True

		return form

class AdministrativeRequestsUpdateView(UpdateView):
	model = AdministrativeRequests
	fields = ['subject', 'body', 'receiver', 'reply']
	template_name = 'inquiries/admin_requests_details.html'
	def get_success_url(self):
		
		return reverse_lazy('administrativerequests-list')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['table_title'] = 'Update Administrative Request'
		return context
	
	def get_form(self, form_class=None):
		form = super().get_form(form_class)

		# Check if the user is a student
		if self.request.user.es_externo():
			# Make the 'reply' field read-only for students so that the field can still be submitted
			form.fields['reply'].widget.attrs['readonly'] = True

		return form

class AdministrativeRequestsListView(LoginRequiredMixin,ListView):
	model = AdministrativeRequests
	
	# The context object name will be used in the templates to query the administrative requests
	context_object_name = "administrative_requests"    
	template_name = "inquiries/admin_requests_list.html"
	paginate_by = 5
	
	def get_queryset(self):
		
		
		# Get the currently logged-in user
		user = self.request.user
		print ("...get_queryset... :", user.es_funcionario())

		if user.es_director() or user.is_superuser:
			# If the user is a team lead, return all administrative requests
			return AdministrativeRequests.objects.all()
	
		# If the user is a facilitator, filter administrative requests sent by all students
		elif user.es_funcionario():
			return AdministrativeRequests.objects.filter(sender=user)

		# If the user is a student, filter administrative requests sent by the student
		elif user.es_externo():
			return AdministrativeRequests.objects.filter(sender=user)
		
class AdministrativeRequestsDeleteView(DeleteView):
	model = AdministrativeRequests
	template_name = 'inquiries/confirm_delete.html'

	def get_success_url(self):		
		return reverse_lazy('administrativerequests-list')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Delete Administrative Request'	 
			 
		# Retrieves the subject of the administrativerequest we want to delete
		administration_request_subject = AdministrativeRequests.objects.get(pk=self.kwargs.get('pk')).subject
		context['message'] = f'Are you sure you want to delete this Administrative Request : "{administration_request_subject}" ?'
		
		# Display a cancel button on confirmation page and if pressed, return user to the academicrequests list
		context['cancel_url'] = 'administrativerequests-list'
		return context 
	
#-------------------------------------------------------------------------------------------------------------------------------
