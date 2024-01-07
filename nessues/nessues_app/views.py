from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import (
    Room, Table, Task, Nessues_Group, 
    Nessues_Group_User, Invitation)
from .forms import (
    CreateRoomForm, CreateTableForm, CreateTaskForm, UpdateTaskForm, 
    CompleteTaskForm, DeleteRoomForm, CreateGroupForm, CloseGroupForm,
    AcceptInvitationForm, RejectInvitationForm, SendInvitationForm)


def home_view(request):
    title = "home"
    return render(request, 'nessues_app/home.html', {'title': title})


"""
 data that need to be rendered on the page: 
    1) title
    2) available_groups
    3) forms
        new group
"""
class GroupsView(TemplateView):
    template_name = 'nessues_app/groups.html'
    title = 'group'
    create_group_class = CreateGroupForm

    def get(self, request, *args, **kwargs):
        available_groups = Nessues_Group_User.objects.filter(user=self.request.user.id)
        create = self.create_group_class()
        return render(request, self.template_name, {'available_groups': available_groups, 'create': create})

    def post(self, request, *args, **kwargs):
        create = self.create_group_class(request.POST)

        if create.is_valid():
            create.save()
            current_group = Nessues_Group.objects.get(name=create.cleaned_data['name'])
            current_group.users.add(self.request.user.id, through_defaults={'role': 1})
            current_group.save()
            messages.success(request, "Group added")
            return HttpResponseRedirect('/groups')
        else:
            messages.warning(request, "Group with the same name already exists")
            return HttpResponseRedirect('/groups')
        return render(request, self.template_name, {'create': create})


"""
 data that need to be rendered on the page: 
    1) title
    2) available_rooms
    3) forms
        new room
"""
class RoomsView(TemplateView):
    template_name = 'nessues_app/mono_rooms.html'
    title = 'rooms'
    create_room_class = CreateRoomForm

    def get(self, request, *args, **kwargs):
        available_rooms = Room.objects.filter(owner=self.request.user.id)
        create = self.create_room_class(initial={'owner': self.request.user.id})

        return render(request, self.template_name, {'title': self.title, 'available_rooms': available_rooms, 'create': create})

    def post(self, request, *args, **kwargs):
        create = self.create_room_class(request.POST)

        if create.is_valid():
            create.save()
            return HttpResponseRedirect('/rooms')
        else: 
            messages.warning(request, "Something went wrong while creating room")
            return HttpResponseRedirect('/rooms')

        return render(request, self.template_name, {'create': create})


class TablesView(TemplateView):
    template_name = 'nessues_app/tables.html'
    title = 'tables'
    create_table_class = CreateTableForm
    delete_room_class = DeleteRoomForm
    close_group_class = CloseGroupForm
    invite_user_class = SendInvitationForm

    def get(self, request, *args, **kwargs):
        if self.kwargs['redirected_from'] == 'group':
            try:
                current = Nessues_Group.objects.get(id=self.kwargs['key_id'])
                user_role = Nessues_Group_User.objects.get(group=self.kwargs['key_id'], user=self.request.user.id).role
                try:
                    available_tables = Table.objects.filter(group=current.id)
                except:
                    available_tables = None
                create = self.create_table_class(initial={'group': current.id})
                delete = self.close_group_class(initial={'group': current.id})
                invite = self.invite_user_class(initial={'group': current.id})
            except:
                pass
        
        if self.kwargs['redirected_from'] == 'room':
            try:
                current = Room.objects.get(id=self.kwargs['key_id'])
                try:
                    available_tables = Table.objects.filter(room=current.id)
                except:
                    available_tables = None
                create = self.create_table_class(initial={'room': self.kwargs['key_id']})
                delete = self.delete_room_class(initial={'room': self.kwargs['key_id']})
            except:
                pass
        
        try:
            return render(request, self.template_name, {'title': self.title, 'current_type': self.kwargs['redirected_from'], 'current': current.id, 'current_name': current.name, 'available_tables': available_tables, 'create': create, 'delete': delete, 'invite': invite, 'user_role': user_role})
        except:
            return render(request, self.template_name, {'title': self.title, 'current_type': self.kwargs['redirected_from'], 'current': current.id, 'current_name': current.name, 'available_tables': available_tables, 'create': create, 'delete': delete})
        

    def post(self, request, *args, **kwargs):
        create = self.create_table_class(request.POST)
        invite = self.invite_user_class(request.POST)
        delete = self.delete_room_class(request.POST)

        if create.is_valid():
            create.save()
            return HttpResponseRedirect(f"/tables/{self.kwargs['redirected_from']}/{self.kwargs['key_id']}")

        if invite.is_valid():
            user_to_invite = invite.cleaned_data['user']
            group_send_invitation_from = invite.cleaned_data['group']
            print(f"CLEANED DATA: {invite.cleaned_data}")
            
            try:
                user_exists = User.objects.get(username=user_to_invite)
                try:
                    if not Invitation.objects.filter(group=group_send_invitation_from, user=user_to_invite.id):
                        try:
                            if not Nessues_Group_User.objects.filter(group=group_send_invitation_from, user=user_to_invite.id):
                                messages.success(request, "Invitation was sent")
                                invite.save()
                        except:
                            messages.warning(request, "User already participate in the current group")
                except:
                    messages.warning(request, "You cannot send invitation twice to the same user")
            except:
                messages.warning(request, "No user with this name")

            return HttpResponseRedirect(f"/tables/{self.kwargs['redirected_from']}/{self.kwargs['key_id']}")
        else:
            # messages.message("Something went wrong, please check provided username")
            print("INVALID INVITATION FORM", invite)
        
        if delete.is_valid():
            id_to_delete = delete.cleaned_data['id']
            if self.kwargs['redirected_from'] == 'room': 
                current_to_delete = Room.objects.get(id=self.kwargs['key_id']).id
            elif self.kwargs['redirected_from'] == 'group':
                current_to_delete = Nessues_Group.objects.get(id=self.kwargs['key_id']).id

            if current_to_delete != id_to_delete:
                messages.warning(request, f"You were restricted to delete other {{ self.kwargs['redirected_from'] }}s")
                return HttpResponseRedirect(f"/tables/{self.kwargs['redirected_from']}/{self.kwargs['key_id']}")
            try:    
                if self.kwargs['redirected_from'] == 'room':
                    to_delete = Room.objects.get(id=id_to_delete) 
                elif self.kwargs['redirected_from'] == 'group':
                    to_delete = Nessues_Group.objects.get(id=id_to_delete) 
                to_delete.delete()
                messages.success(request, f"{{ self.kwargs['redirected_from'] }} deleted successfully")
                return HttpResponseRedirect("/account")
            except Exception:
                messages.warning(request, 'Wrong id provided, try again')
                return HttpResponseRedirect(f"/tables/{self.kwargs['redirected_from']}/{self.kwargs['key_id']}")

        return render(request, self.template_name, {'create': create, 'delete': delete})


"""
 Forms to handle:  
    1) CreateTaskForm
    2) UpdateTaskForm
    3) CompleteTaskForm
"""
class TasksView(TemplateView):
    template_name = 'nessues_app/tasks.html'
    create_task_class = CreateTaskForm
    update_task_class = UpdateTaskForm
    complete_task_class = CompleteTaskForm

    def get(self, request, *args, **kwargs): 
        available_tasks = Task.objects.filter(table=self.kwargs['key_id'])
        create = self.create_task_class(initial={'table': self.kwargs['key_id'], 'created_by': self.request.user.id})
        update = self.update_task_class(initial={'table': self.kwargs['key_id'], 'created_by': self.request.user.id})
        complete = self.complete_task_class(initial={'table': self.kwargs['key_id'], 'created_by': self.request.user.id})

        return render(request, self.template_name, {'url_arguments': {'key_id': self.kwargs['key_id'], 'current_user': self.request.user.id}, 'available_tasks': available_tasks, 'create': create, 'update': update, 'complete': complete})

    def post(self, request, *args, **kwargs):
        create = self.create_task_class(request.POST)
        update = self.update_task_class(request.POST)
        complete = self.complete_task_class(request.POST)

        if create.is_valid():
            create.save()
            # messages.success(request, 'Task Successfully added')
            return HttpResponseRedirect(f'/tasks/{self.kwargs["key_id"]}')

        if update.is_valid():
            update.save()
            messages.success(request, 'Task successfully updated')
            return HttpResponseRedirect(f'/tasks/{self.kwargs["key_id"]}')

        if complete.is_valid():
            id_to_close = complete.cleaned_data['id']
            try:    
                task_to_complete = Task.objects.get(id=id_to_close) 
                task_to_complete.delete()
            except Exception:
                messages.warning(request, 'Wrong id provided, try again')
                return HttpResponseRedirect(f'/tasks/{self.kwargs["key_id"]}')

            messages.success(request, 'Task successfully completed')
            return HttpResponseRedirect(f'/tasks/{self.kwargs["key_id"]}')
        
        return render(request, self.template_name, {'create': create, 'update': update, 'complete': complete})


"""
 Forms to handle:
    1) accept invitation;
    2) refuse invitation.
"""
class InvitationsView(TemplateView): 
    template_name = 'nessues_app/invitations.html'
    accept_invitation_class = AcceptInvitationForm
    reject_invitation_class = RejectInvitationForm

    def get(self, request, *args, **kwargs):
        available_invitation = Invitation.objects.filter(user=self.request.user.id)
        accept = self.accept_invitation_class()
        reject = self.reject_invitation_class()

        return render(request, self.template_name, {'available_invitations': available_invitation, 'accept': accept, 'reject': reject})

    def post(self, request, *args, **kwargs):
        accept = self.accept_invitation_class(request.POST)
        reject = self.reject_invitation_class(request.POST)

        # create new relation between user and nessues_group, role = 3 (common user). At the end, if success - delete the invitation
        if accept.is_valid():
            try:
                current_user = User.objects.get(id=self.request.user.id)
                invitation_to_accept = Invitation.objects.get(id=accept.cleaned_data['id'])
                group_where_to_add = Nessues_Group.objects.get(id=invitation_to_accept.group.id)
                group_where_to_add.users.add(self.request.user.id, through_defaults={'role': 3}) # bug here
                group_where_to_add.save()
                invitation_to_accept.delete()
                message.success(request, "You successfully accepted the request to join the group")
                return HttpResponseRedirect('/invitations')
            except:
                messages.warning(request, "Something went wrong, please try again")

        # delete row from the invitations table
        if reject.is_valid():
            try:
                invitation_to_reject = Invitation.objects.get(id=accept.cleaned_data['id'])
                invitation_to_reject.delete()
                messages.success(request, "Request successfully rejected")
                return HttpResponseRedirect('/invitations')
            except: 
                pass

        return render(request, self.template_name, {'accept': accept, 'reject': reject})

def about_view(request):
    content = {  }

    title = "about"
    return render(request, 'nessues_app/about.html', {'title': title, 'content': content})