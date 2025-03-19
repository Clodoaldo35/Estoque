import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Brand, Category, Product


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'is_active', 'description', 'created_at', 'updated_at'
    ]
    search_fields = ['name']
    list_filter = ['is_active']

    def created_at(self, obj):
        return obj.created_at.strftime('%d-%m-%Y %H:%M')
    created_at.admin_order_field = 'created_at'
    created_at.short_description = 'Criado em'

    def updated_at(self, obj):
        return obj.updated_at.strftime('%d-%m-%Y %H:%M')
    updated_at.admin_order_field = 'updated_at'
    updated_at.short_description = 'Atualizado em'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'is_active', 'description', 'created_at', 'updated_at'
    ]
    search_fields = ['name']
    list_filter = ['is_active']

    def created_at(self, obj):
        return obj.created_at.strftime('%d-%m-%Y %H:%M')
    created_at.admin_order_field = 'created_at'
    created_at.short_description = 'Criado em'

    def updated_at(self, obj):
        return obj.updated_at.strftime('%d-%m-%Y %H:%M')
    updated_at.admin_order_field = 'updated_at'
    updated_at.short_description = 'Atualizado em'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'brand', 'category', 'price', 'stock',
        'is_active', 'description', 'created_at', 'updated_at'
    ]
    search_fields = ['title', 'brand__name', 'category__name']
    list_filter = ['is_active', 'brand', 'category']
    list_editable = ('stock',)
    actions = ['export_to_csv']

    def created_at(self, obj):
        return obj.created_at.strftime('%d-%m-%Y %H:%M')
    created_at.admin_order_field = 'created_at'
    created_at.short_description = 'Criado em'

    def updated_at(self, obj):
        return obj.updated_at.strftime('%d-%m-%Y %H:%M')
    updated_at.admin_order_field = 'updated_at'
    updated_at.short_description = 'Atualizado em'

    def get_fields(self, request, obj=None):
        fields = list(
            super().get_fields(request, obj)
        )  # Convertendo para lista
        if not obj:  # Adiciona 'stock' apenas no formulário de criação
            fields.append('stock')  # Usando append para adicionar à lista
        return fields

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Titulo', 'Marca', 'Categoria', 'Preço', 'Estoque', 'Ativo',
            'Descrição', 'Criado em', 'Atualizado em'
        ])
        for product in queryset:
            writer.writerow([
                product.title,
                product.brand.name,
                product.category.name,
                product.price,
                product.stock,
                product.is_active,
                product.description,
                product.created_at.strftime('%d-%m-%Y %H:%M'),
                product.updated_at.strftime('%d-%m-%Y %H:%M')
            ])
        return response
    export_to_csv.short_description = 'Exportar para CSV'
