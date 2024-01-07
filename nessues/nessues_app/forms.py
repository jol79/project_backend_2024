from django import forms
from django.forms import (
    CharField, HiddenInput, BooleanField, IntegerField)
from .models import (
    Room, Table, Task, Nessues_Group, 
    Nessues_Group_User, Invitation)


"""
 rooms
"""
class CreateRoomForm(forms.ModelForm):
    name = CharField(max_length=21)
    description = CharField(max_length=32)

    class Meta:
        model = Room
        fields = ['name', 'description', 'owner']
        widgets = {'owner': forms.HiddenInput()}

class DeleteRoomForm(forms.ModelForm):
    id = IntegerField()

    class Meta: 
        model = Room
        fields = ['id']

"""
 groups
"""
class CreateGroupForm(forms.ModelForm):
    name = CharField(max_length=21)
    description = CharField(max_length=32)

    class Meta:
        model = Nessues_Group
        fields = ['name', 'description']
# TO FIX, doesn't work properly
class CloseGroupForm(forms.ModelForm):
    id = IntegerField()

    class Meta: 
        model = Nessues_Group_User
        fields = ['id']

"""
 tablets
"""
class CreateTableForm(forms.ModelForm):
    name = CharField(max_length=21)
    description = CharField(max_length=60)

    class Meta:
        model = Table
        fields = ['name', 'description', 'room', 'group']
        widgets = {'room': forms.HiddenInput(), 'group': forms.HiddenInput()}

"""
 tasks
"""
class CreateTaskForm(forms.ModelForm): 
    text = CharField(max_length=120)

    class Meta:
        model = Task
        fields = ['text', 'completed', 'created_by', 'table']
        widgets = {'completed': forms.HiddenInput(), 'created_by': forms.HiddenInput(), 'table': forms.HiddenInput()}

class UpdateTaskForm(forms.ModelForm):
    text = CharField(max_length=120)

    class Meta: 
        model = Task
        fields = ['id', 'text', 'completed', 'table']
        widgets = {'id': forms.HiddenInput(), 'completed': forms.HiddenInput(), 'table': forms.HiddenInput()}

class CompleteTaskForm(forms.ModelForm):
    id = IntegerField()

    class Meta:
        model = Task
        fields = ['id', 'table', 'completed', 'created_by']
        widgets = {'table': forms.HiddenInput(), 'completed': forms.HiddenInput(), 'created_by': forms.HiddenInput()}

"""
 invitations
"""
class SendInvitationForm(forms.ModelForm):

    class Meta:
        model = Invitation
        fields = ['group', 'user']
        widgets = {'group': forms.HiddenInput()}

class AcceptInvitationForm(forms.ModelForm):
    id = IntegerField()

    class Meta:
        model = Invitation
        fields = ['id']

class RejectInvitationForm(forms.ModelForm):
    id = IntegerField()

    class Meta:
        model = Invitation
        fields = ['id']