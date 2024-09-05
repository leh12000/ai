from django.contrib import admin
from .models import Level
# Register your models here.
class LevelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("name",)}

admin.site.register(Level,LevelAdmin)