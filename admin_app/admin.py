from django import forms
from django.contrib import admin
from .models import CompanyInfo, Product, BlogPost, Request, Review
import os
import json
from django.conf import settings
from django.forms.widgets import Widget


class MultipleFileInput(forms.FileInput):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs.update({'multiple': True})
        super(forms.FileInput, self).__init__(attrs)  # Skip FileInput's __init__

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        # Обрабатываем список файлов
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


# Форма для информации о компании с отдельными полями для соцсетей
class CompanyInfoForm(forms.ModelForm):
    # Отдельные поля для социальных сетей
    whatsapp = forms.CharField(
        max_length=200, 
        required=False, 
        label="WhatsApp", 
        help_text="Ссылка на WhatsApp"
    )
    instagram = forms.CharField(
        max_length=200, 
        required=False, 
        label="Instagram", 
        help_text="Ссылка на Instagram"
    )
    telegram = forms.CharField(
        max_length=200, 
        required=False, 
        label="Telegram", 
        help_text="Ссылка на Telegram"
    )
    facebook = forms.CharField(
        max_length=200, 
        required=False, 
        label="Facebook", 
        help_text="Ссылка на Facebook"
    )
    youtube = forms.CharField(
        max_length=200, 
        required=False, 
        label="YouTube", 
        help_text="Ссылка на YouTube"
    )

    class Meta:
        model = CompanyInfo
        fields = ['phone', 'email', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Заполняем поля из JSON при редактировании
        if self.instance.pk and self.instance.social_links:
            # Обрабатываем случай, когда social_links может быть строкой JSON
            try:
                if isinstance(self.instance.social_links, str):
                    import json
                    social_links = json.loads(self.instance.social_links)
                else:
                    social_links = self.instance.social_links or {}
                    
                self.fields['whatsapp'].initial = social_links.get('whatsapp', '')
                self.fields['instagram'].initial = social_links.get('instagram', '')
                self.fields['telegram'].initial = social_links.get('telegram', '')
                self.fields['facebook'].initial = social_links.get('facebook', '')
                self.fields['youtube'].initial = social_links.get('youtube', '')
            except (json.JSONDecodeError, AttributeError):
                # Если не удается парсить, оставляем поля пустыми
                pass

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Собираем данные социальных сетей в JSON
        social_links = {}
        if self.cleaned_data.get('whatsapp'):
            social_links['whatsapp'] = self.cleaned_data['whatsapp']
        if self.cleaned_data.get('instagram'):
            social_links['instagram'] = self.cleaned_data['instagram']
        if self.cleaned_data.get('telegram'):
            social_links['telegram'] = self.cleaned_data['telegram']
        if self.cleaned_data.get('facebook'):
            social_links['facebook'] = self.cleaned_data['facebook']
        if self.cleaned_data.get('youtube'):
            social_links['youtube'] = self.cleaned_data['youtube']
        
        instance.social_links = social_links
        
        if commit:
            instance.save()
        return instance


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    form = CompanyInfoForm
    list_display = ['phone', 'email', 'address']
    fieldsets = (
        ('Контактная информация', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Социальные сети', {
            'fields': ('whatsapp', 'instagram', 'telegram', 'facebook', 'youtube'),
            'description': 'Укажите ссылки на социальные сети'
        }),
    )


# Форма для продукта с отдельными полями для атрибутов
class ProductForm(forms.ModelForm):
    upload_images = MultipleFileField(
        required=False,
        label="Загрузить изображения"
    )
    
    # Отдельные поля для атрибутов (добавьте нужные вам атрибуты)
    brand = forms.CharField(
        max_length=100, 
        required=False, 
        label="Бренд",
        help_text="Производитель товара"
    )
    model = forms.CharField(
        max_length=100, 
        required=False, 
        label="Модель",
        help_text="Модель товара"
    )
    color = forms.CharField(
        max_length=50, 
        required=False, 
        label="Цвет",
        help_text="Цвет товара"
    )
    size = forms.CharField(
        max_length=50, 
        required=False, 
        label="Размер",
        help_text="Размер товара"
    )
    weight = forms.CharField(
        max_length=50, 
        required=False, 
        label="Вес",
        help_text="Вес товара"
    )
    material = forms.CharField(
        max_length=100, 
        required=False, 
        label="Материал",
        help_text="Материал изготовления"
    )
    country = forms.CharField(
        max_length=100, 
        required=False, 
        label="Страна производства",
        help_text="Страна производства товара"
    )
    article = forms.CharField(
        max_length=100, 
        required=False, 
        label="Артикул",
        help_text="Артикул товара"
    )

    class Meta:
        model = Product
        fields = ['title', 'description', 'guarantee', 'region', 'price_retail', 'price_wholesale', 'price_bulk']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Заполняем поля из JSON при редактировании
        if self.instance.pk and self.instance.attributes:
            # Обрабатываем случай, когда attributes может быть строкой JSON
            try:
                if isinstance(self.instance.attributes, str):
                    import json
                    attributes = json.loads(self.instance.attributes)
                else:
                    attributes = self.instance.attributes or {}
                    
                self.fields['brand'].initial = attributes.get('brand', '')
                self.fields['model'].initial = attributes.get('model', '')
                self.fields['color'].initial = attributes.get('color', '')
                self.fields['size'].initial = attributes.get('size', '')
                self.fields['weight'].initial = attributes.get('weight', '')
                self.fields['material'].initial = attributes.get('material', '')
                self.fields['country'].initial = attributes.get('country', '')
                self.fields['article'].initial = attributes.get('article', '')
            except (json.JSONDecodeError, AttributeError):
                # Если не удается парсить, оставляем поля пустыми
                pass

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Собираем атрибуты в JSON
        attributes = {}
        if self.cleaned_data.get('brand'):
            attributes['brand'] = self.cleaned_data['brand']
        if self.cleaned_data.get('model'):
            attributes['model'] = self.cleaned_data['model']
        if self.cleaned_data.get('color'):
            attributes['color'] = self.cleaned_data['color']
        if self.cleaned_data.get('size'):
            attributes['size'] = self.cleaned_data['size']
        if self.cleaned_data.get('weight'):
            attributes['weight'] = self.cleaned_data['weight']
        if self.cleaned_data.get('material'):
            attributes['material'] = self.cleaned_data['material']
        if self.cleaned_data.get('country'):
            attributes['country'] = self.cleaned_data['country']
        if self.cleaned_data.get('article'):
            attributes['article'] = self.cleaned_data['article']
        
        instance.attributes = attributes

        # Сохраняем изображения
        image_paths = []
        if instance.images:
            # Безопасно обрабатываем существующие изображения
            try:
                if isinstance(instance.images, str):
                    import json
                    image_paths = json.loads(instance.images)
                else:
                    image_paths = instance.images or []
            except (json.JSONDecodeError, AttributeError):
                image_paths = []
        
        upload_images = self.cleaned_data.get('upload_images')
        
        if upload_images:
            # Обрабатываем список файлов
            files_to_process = upload_images if isinstance(upload_images, list) else [upload_images]
            
            for file in files_to_process:
                if file:  # Проверяем, что файл не пустой
                    filename = file.name
                    save_path = os.path.join(settings.MEDIA_ROOT, filename)
                    
                    # Создаем директорию если не существует
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    
                    with open(save_path, 'wb+') as dest:
                        for chunk in file.chunks():
                            dest.write(chunk)
                    image_paths.append(f"/uploads/{filename}")

            instance.images = image_paths

        if commit:
            instance.save()
        return instance


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm

    list_display = ['title', 'price_retail', 'price_wholesale', 'price_bulk', 'region', 'guarantee']
    list_filter = ['region', 'guarantee']
    search_fields = ['title', 'description']

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'upload_images', 'images')
        }),
        ('Атрибуты товара', {
            'fields': ('brand', 'model', 'color', 'size', 'weight', 'material', 'country', 'article'),
            'description': 'Характеристики товара'
        }),
        ('Цены', {
            'fields': ('price_retail', 'price_wholesale', 'price_bulk')
        }),
        ('Дополнительно', {
            'fields': ('guarantee', 'region')
        }),
    )

    readonly_fields = ['images']

    def get_fieldsets(self, request, obj=None):
        # Можно настроить отображение полей в зависимости от прав пользователя
        fieldsets = super().get_fieldsets(request, obj)
        return fieldsets


class BlogPostForm(forms.ModelForm):
    upload_images = MultipleFileField(
        required=False,
        label="Загрузить изображения"
    )

    class Meta:
        model = BlogPost
        fields = ['title', 'content']

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Безопасно обрабатываем существующие изображения
        image_paths = []
        if instance.images:
            try:
                if isinstance(instance.images, str):
                    import json
                    image_paths = json.loads(instance.images)
                else:
                    image_paths = instance.images or []
            except (json.JSONDecodeError, AttributeError):
                image_paths = []

        upload_images = self.cleaned_data.get('upload_images')
        
        if upload_images:
            # Обрабатываем список файлов
            files_to_process = upload_images if isinstance(upload_images, list) else [upload_images]
            
            for file in files_to_process:
                if file:  # Проверяем, что файл не пустой
                    filename = file.name
                    save_path = os.path.join(settings.MEDIA_ROOT, filename)
                    
                    # Создаем директорию если не существует
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    
                    with open(save_path, 'wb+') as dest:
                        for chunk in file.chunks():
                            dest.write(chunk)
                    image_paths.append(f"{settings.MEDIA_URL}{filename}")

            instance.images = image_paths

        if commit:
            instance.save()
        return instance


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostForm

    list_display = ['title', 'content_preview']
    search_fields = ['title', 'content']

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'content', 'upload_images', 'images')
        }),
    )

    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Превью контента'

    readonly_fields = ['images']


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'comment_preview']
    list_filter = ['name']
    search_fields = ['name', 'phone']
    readonly_fields = ['name', 'phone', 'comment']
    
    def comment_preview(self, obj):
        return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
    comment_preview.short_description = 'Комментарий'
    
    def has_add_permission(self, request):
        return False


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'review_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'review']
    readonly_fields = ['created_at']
    
    def review_preview(self, obj):
        return obj.review[:50] + '...' if len(obj.review) > 50 else obj.review
    review_preview.short_description = 'Отзыв'


# Настройка админки
admin.site.site_header = 'Админ панель Armstrong'
admin.site.site_title = 'Armstrong Admin'
admin.site.index_title = 'Добро пожаловать в админ панель'