from django.contrib import admin

from .models import ImageFile


@admin.register(ImageFile)
class ImageFileAdmin(admin.ModelAdmin):

    list_display = ('id',
                    'inst_type',
                    'inst_id',
                    'file_path',
                    'is_deleted',
                    'create_time')

    list_editable = ('is_deleted',)

    list_per_page = 100