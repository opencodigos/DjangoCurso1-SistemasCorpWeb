from django.contrib import admin
from config.models import Logo, SEOHome, GoogleAnalytics

# Register your models here.
admin.site.register(Logo)
admin.site.register(SEOHome)
admin.site.register(GoogleAnalytics)