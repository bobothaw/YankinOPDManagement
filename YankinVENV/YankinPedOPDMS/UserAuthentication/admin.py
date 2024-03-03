from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile
from PharmacistApp.models import MedicineType
from DoctorApp.models import Ward, Diagnosis

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Ward)
admin.site.register(Diagnosis)
admin.site.register(MedicineType)







