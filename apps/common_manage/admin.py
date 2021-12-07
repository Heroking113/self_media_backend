from django.contrib import admin

from .models import Configuration


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):

    list_display = ('id',
                    'key',
                    'opt_val_one',
                    'uni_val',
                    'instruction')

    list_editable = ('key',
                    'opt_val_one',
                    'uni_val',
                    'instruction')

    # readonly_fields = ('key',)

    list_per_page = 100