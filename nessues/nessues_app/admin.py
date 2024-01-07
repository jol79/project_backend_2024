from django.contrib import admin
from nessues_app.models import Room, Task, Table, Nessues_Group, Nessues_Group_User, Invitation


admin.site.register(Room)
admin.site.register(Task)
admin.site.register(Table)
admin.site.register(Nessues_Group)
admin.site.register(Nessues_Group_User)
admin.site.register(Invitation)
