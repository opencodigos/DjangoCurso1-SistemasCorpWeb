from django.contrib import admin
from config.models import Logo, SEOHome

# Register your models here.
admin.site.register(Logo)
admin.site.register(SEOHome)
admin.site.register(GoogleAnalytics)