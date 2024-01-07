from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User, Group


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=21)
    date_created = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=32, blank=True, null=True)
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )   

    def __str__(self):
        return self.name
    class Meta: 
        ordering = ['id']
    

class Nessues_Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=21, unique=True)
    users = models.ManyToManyField(User, through='Nessues_Group_User')
    description = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self): 
        return str(self.id)


class Nessues_Group_User(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Nessues_Group, on_delete=models.CASCADE)
    role = models.IntegerField(blank=False, default=None) # 1-Owner, 2-Admin, 3-Common

    def __str__(self):
        return self.group.name

    
class Table(models.Model):
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(
        Room,
        blank=True,   
        null=True, 
        default=None,  
        on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        Nessues_Group,
        blank=True,   
        null=True, 
        default=None,  
        on_delete=models.CASCADE
    )
    date_created = models.DateField(default=now)
    name = models.CharField(max_length=21)
    description = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return self.name 


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    table = models.ForeignKey(
        Table,      
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=120)
    date_created = models.DateField(default=now)
    created_by = models.IntegerField(blank=False)
    completed = models.BooleanField(default=False)
    completed_by = models.IntegerField(blank=False, null=True, default=None)

    def __str__(self):
        return self.text


class Invitation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Nessues_Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"From {self.group.name} to {self.user}"




