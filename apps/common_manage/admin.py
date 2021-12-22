from django.contrib import admin

from .models import Configuration, SchSwiper


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


@admin.register(SchSwiper)
class SchSwiperAdmin(admin.ModelAdmin):
    list_display = ('id', 'school', 'swiper_type', 'img_path', 'mp_id', 'tweets_url')
    list_editable = ('school', 'swiper_type', 'img_path', 'mp_id', 'tweets_url')
    list_per_page = 100