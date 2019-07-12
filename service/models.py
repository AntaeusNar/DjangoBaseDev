from django.db import models

# Create your models here.


class Address(models.Model):
    house_number = models.CharField(max_length=32)
    road = models.CharField(max_length=32)
    unit = models.CharField(max_length=32, null=True, blank=True)
    level = models.CharField(max_length=32, null=True, blank=True)
    staircase = models.CharField(max_length=32, null=True, blank=True)
    entrance = models.CharField(max_length=32, null=True, blank=True)
    po_box = models.CharField(max_length=32, null=True, blank=True)
    postcode = models.CharField(max_length=32)
    suburb = models.CharField(max_length=32, null=True, blank=True)
    city_district = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=32)
    county = models.CharField(max_length=32, null=True, blank=True)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=32)

    def save(self, *args, **kwargs):
        us_state_abbrev = {
            'Alabama': 'AL',
            'Alaska': 'AK',
            'Arizona': 'AZ',
            'Arkansas': 'AR',
            'California': 'CA',
            'Colorado': 'CO',
            'Connecticut': 'CT',
            'Delaware': 'DE',
            'Florida': 'FL',
            'Georgia': 'GA',
            'Hawaii': 'HI',
            'Idaho': 'ID',
            'Illinois': 'IL',
            'Indiana': 'IN',
            'Iowa': 'IA',
            'Kansas': 'KS',
            'Kentucky': 'KY',
            'Louisiana': 'LA',
            'Maine': 'ME',
            'Maryland': 'MD',
            'Massachusetts': 'MA',
            'Michigan': 'MI',
            'Minnesota': 'MN',
            'Mississippi': 'MS',
            'Missouri': 'MO',
            'Montana': 'MT',
            'Nebraska': 'NE',
            'Nevada': 'NV',
            'New Hampshire': 'NH',
            'New Jersey': 'NJ',
            'New Mexico': 'NM',
            'New York': 'NY',
            'North Carolina': 'NC',
            'North Dakota': 'ND',
            'Ohio': 'OH',
            'Oklahoma': 'OK',
            'Oregon': 'OR',
            'Pennsylvania': 'PA',
            'Rhode Island': 'RI',
            'South Carolina': 'SC',
            'South Dakota': 'SD',
            'Tennessee': 'TN',
            'Texas': 'TX',
            'Utah': 'UT',
            'Vermont': 'VT',
            'Virginia': 'VA',
            'Washington': 'WA',
            'West Virginia': 'WV',
            'Wisconsin': 'WI',
            'Wyoming': 'WY',
        }
        for field_name in ['house_number', 'road', 'unit', 'suburb', 'city_district', 'state', 'city', 'county']:
            val = getattr(self, field_name, False)
            if val and field_name != 'state':
                setattr(self, field_name, val.title())
            if val and field_name == 'state': # and val.title in us_state_abbrev:
                setattr(self, field_name, us_state_abbrev.get(val.title, "NV"))
        super().save(*args, **kwargs)

    def __str__(self):
        if self.unit is not None:
            full_address = '%s %s, %s, %s, %s %s' % (
                self.house_number, self.road, self.unit, self.city, self.state, self.postcode
            )
        elif self.po_box is not None:
            full_address = 'PO Box %s, %s, %s %s' % (
                self.po_box, self.city, self.state, self.postcode
            )
        else:
            full_address = '%s %s, %s, %s %s' % (
                self.house_number, self.road, self.city, self.state, self.postcode
            )
        return full_address


class Container(models.Model):
    # a location, truck, door, system, group, warehouse etc for relating one set of parts to another
    # or sub-locations nesting forever
    name = models.CharField(max_length=64)
    part = models.ManyToManyField('Part')
    # Todo: Adjust so that each container can have only one address, but make sure we can have multible containers at one address
    address = models.ManyToManyField('Address')
    subcontainer = models.ManyToManyField('Container')

    def __str__(self):
        return self.name


class MasterPart(models.Model):
    name = models.CharField(max_length=16)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.CASCADE)
    man_part_num = models.CharField(max_length=32, null=True)
    supplier = models.ManyToManyField('Supplier', through='SupplierPart', related_name='master_part')

    def __str__(self):
        return self.name

# Todo: how do we want to id unique parts? without requiring a serial number?
class Part(models.Model):

    master_part = models.ForeignKey('MasterPart', on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    subpart = models.ManyToManyField('Part')

    def __str__(self):
        return self.name


class SupplierPart(models.Model):
    supplier_part_number = models.CharField(max_length=32)
    master_part = models.ForeignKey('MasterPart', related_name='supplier_part_number', on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey('Supplier', related_name='supplier_part_Number', on_delete=models.SET_NULL, null=True)


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

    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('On Hold', 'On Hold'),
        ('Initial', 'Initial'),
        ('In Work', 'In Work'),
        ('Completed', 'Completed'),
    )
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='Initial')
    container = models.ForeignKey('Container', on_delete=models.CASCADE)
    event_date = models.DateField()
    rec_date = models.DateTimeField(auto_now_add=True)
    last_change_date = models.DateTimeField(auto_now=True)
    events = models.ManyToManyField('self')

# Todo: add addresses, contact info etc
class Manufacturer(models.Model):
    name = models.CharField(max_length=16)
    address = models.ManyToManyField('Address')

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=32)
    address = models.ManyToManyField('Address')

    def __str__(self):
        return self.name



