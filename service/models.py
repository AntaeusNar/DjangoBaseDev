from django.db import models

# Create your models here.


class Container(models.Model):
    # a location, truck, door, system, group, warehouse etc for relating one set of parts to another
    # or sub-locations nesting forever
    name = models.CharField(max_length=64)
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
    event = models.ForeignKey('Event', related_name='part_quantity', on_delete=models.SET_NULL, null=True)


class Event(models.Model):
    # this is the core of the service system, each event is the what, when, where and how of the system
    title = models.CharField(max_length=64)
    description = models.TextField()

    CATEGORY_CHOICES = (
        ("Install", 'Initial Installation'),
        ("Service", 'Service Work'),
        ("Warranty", 'Warranty Service'),
        ("Insp.", 'Inspection'),
        ('Audit', 'Audit'),
        ('Est.', 'Estimate/Quote/Proposal')
    )
    category = models.CharField(max_length=8, choices=CATEGORY_CHOICES)
    parts = models.ManyToManyField('Part', through='PartQuantity', related_name='events')
    events = models.ManyToManyField('self')

    def __str__(self):
        return self.title
