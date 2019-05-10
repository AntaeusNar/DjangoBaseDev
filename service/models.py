from django.db import models

# Create your models here.


class Container(models.Model):
    # a location, truck, door, system, group, warehouse etc for relating one set of parts to another
    # or sub-locations nesting forever
    name = models.CharField(max_length=64)
    part = models.ManyToManyField('Part', through='PartQuantity', related_name='containers')
    subcontainer = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Part(models.Model):

    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class PartQuantity(models.Model):
    amount = models.IntegerField()
    part = models.ForeignKey('Part', related_name='part_quantity', on_delete=models.SET_NULL, null=True, blank=True)
    container = models.ForeignKey('Container', related_name='part_quantity', on_delete=models.SET_NULL, null=True)


class Event(models.Model):
    # this is the core of the service system
    # A description of [an action] performed on [Group of Parts at a location/place] at a [time]

    description = models.TextField()

    ACTION_CHOICES = (
        ('Add', 'Installed/Delivered'),
        ('Removed', 'Took out/Picked Up'),
        ('Repair', 'Repaired'),
        ('Insp.', 'Inspected'),
    )
    action = models.CharField(max_length=8, choices=ACTION_CHOICES)
    container = models.ForeignKey('Container', on_delete=models.CASCADE)
    event_date = models.DateField()
    rec_date = models.DateTimeField(auto_now_add=True)
    last_change_date = models.DateTimeField(auto_now=True)
    events = models.ManyToManyField('self')
