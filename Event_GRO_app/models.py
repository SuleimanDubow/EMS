from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

class SittingFormat(models.Model):
    name = models.CharField(max_length=255)
    sitting_types = models.JSONField()  # This stores an array of sitting arrangements in JSON format

    def __str__(self):
        return self.name
    
    



class Event(models.Model):
    name_of_event = models.CharField(max_length=200)
    date_of_event = models.DateField()
    created_by = models.ForeignKey(User, related_name='events_created', on_delete=models.CASCADE)
    modified_by = models.ForeignKey(User, related_name='events_modified', on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    place_of_event = models.CharField(max_length=300)
    no_of_invitees = models.PositiveIntegerField()
    
    # Coordinates for field cards
    field_card_cordinate_x = models.FloatField()
    field_card_cordinate_y = models.FloatField()
    field_card_font_type = models.CharField(max_length=100)
    field_card_font_size = models.PositiveIntegerField()
    
    # Coordinates for luncheon cards
    luncheon_card_cordinate_x = models.FloatField()
    luncheon_card_cordinate_y = models.FloatField()
    luncheon_card_font_type = models.CharField(max_length=100)
    luncheon_card_font_size = models.PositiveIntegerField()

    # Coordinates for field envelope cards
    field_envelope_card_cordinate_x = models.FloatField()
    field_envelope_card_cordinate_y = models.FloatField()
    field_envelope_card_font_type = models.CharField(max_length=100)
    field_envelope_card_font_size = models.PositiveIntegerField()

    # Coordinates for luncheon envelope cards
    luncheon_envelope_card_cordinate_x = models.FloatField()
    luncheon_envelope_card_cordinate_y = models.FloatField()
    luncheon_envelope_card_font_type = models.CharField(max_length=100)
    luncheon_envelope_card_font_size = models.PositiveIntegerField()

    # Luncheon-specific details
    no_of_invitees_to_luncheon = models.PositiveIntegerField()
    field_event_manager = models.CharField(max_length=200)
    luncheon_event_manager = models.CharField(max_length=200)
    
    type_of_sitting_format = models.ForeignKey(SittingFormat, related_name='SittingFormat', on_delete=models.CASCADE, null=True, blank=True,)

    def __str__(self):
        return self.name_of_event + " OF " + self.place_of_event

class Invitee(models.Model):
    INVITE_LUNCHEON_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    name = models.CharField(max_length=255)
    title = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    sitting_position_field = models.CharField(max_length=100)
    invited_for_luncheon = models.CharField(max_length=3, choices=INVITE_LUNCHEON_CHOICES, default='no')
    sitting_position_luncheon = models.CharField(max_length=100, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    company_organization_department_ministry = models.CharField(max_length=255)
    in_care_of = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='invitees_created')
    date_created = models.DateTimeField(auto_now_add=True)

    # Field card printing details
    field_card_printed = models.BooleanField(default=False)
    field_card_printed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='field_card_printers')
    field_card_printed_date = models.DateTimeField(null=True, blank=True)

    # Luncheon card printing details
    luncheon_card_printed = models.BooleanField(default=False)
    luncheon_card_printed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='luncheon_card_printers')
    luncheon_card_printed_date = models.DateTimeField(null=True, blank=True)

    # Dispatch details
    dispatched = models.BooleanField(default=False)
    date_dispatched = models.DateTimeField(null=True, blank=True)
    dispatched_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='dispatchers')

    def __str__(self):
        return self.name +" " + self.event
    
    

    
    
    
    
    
    
    
    
    