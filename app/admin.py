from django.contrib import admin
from django.utils.html import format_html
from app.models import Type,Category, Product ,Color,Gift
# names

admin.site.site_header = "AURORA CADENCE"
admin.site.site_title = "AURORA CADENCE Admin Portal"
admin.site.index_title = "Welcome to AURORA CADENCE Admin"

# Register your models here.
class StockLevelFilter(admin.SimpleListFilter):
    title = 'Stock Level'
    parameter_name = 'stock_level'

    def lookups(self, request, model_admin):
        return (
            ('lt5', 'Less than 5'),
            ('lt10', 'Less than 10'),
            ('lt10', 'Less than 20'),
            ('gt50','Greater than 50'),
            ('gt100','Greater than 100'),
        )

    def queryset(self, request, queryset):
        if self.value()=='lt5':
            return queryset.filter(stock__lt=5)
        if self.value()=='lt10':
            return queryset.filter(stock__lt=10)
        if self.value()=='lt10':
            return queryset.filter(stock__lt=20)
        if self.value()=='gt50':
            return queryset.filter(stock__gt=50)
        if self.value()=="gt100":
            return queryset.filter(stock__gt=100)
        return queryset
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:80px;"/>', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'

    list_display = (
        'image_tag', 'name', 'type_obj' ,'category_obj', 'discount_price', 'stock', 'is_available', 'created_at'
    )
    list_filter = ('category_obj','type_obj', 'gift_obj','wear', 'is_available', 'created_at',StockLevelFilter)
    search_fields = ('name', 'description', 'gift_obj','category_obj__name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name','type_obj' , 'category_obj', 'Color_obj','gift_obj','wear', 'is_available', 'description')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'discount_price', 'stock')
        }),
        ('Images', {
            'fields': ('image', 'image2', 'image3', 'image4', 'image5')
        }),
        ('Auto Update Date & Time', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display=('name',)
    search_fields=('name',)

@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)