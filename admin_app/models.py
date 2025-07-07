# admin_app/models.py
from django.db import models
from django.db.models import JSONField
import json

class SafeJSONField(JSONField):
    """Безопасное JSON поле, которое обрабатывает разные типы данных"""
    
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        
        # Если уже является словарем или списком, возвращаем как есть
        if isinstance(value, (dict, list)):
            return value
            
        # Если строка, пытаемся парсить как JSON
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
                
        return value
    
    def to_python(self, value):
        if value is None:
            return value
            
        if isinstance(value, (dict, list)):
            return value
            
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
                
        return value

class CompanyInfo(models.Model):
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    social_links = SafeJSONField(default=dict, verbose_name='Социальные сети')

    class Meta:
        db_table = 'company_info'
        verbose_name = 'Информация о компании'
        verbose_name_plural = 'Информация о компании'
        managed = False  # Django не будет управлять этой таблицей

    def __str__(self):
        return f'Контакты компании'

class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    attributes = SafeJSONField(default=dict, verbose_name='Атрибуты')
    guarantee = models.CharField(max_length=50, verbose_name='Гарантия')
    region = models.CharField(max_length=100, verbose_name='Регион')
    price_retail = models.IntegerField(verbose_name='Розничная цена')
    price_wholesale = models.IntegerField(verbose_name='Оптовая цена')
    price_bulk = models.IntegerField(verbose_name='Цена за крупный опт')
    description = models.TextField(verbose_name='Описание')
    images = SafeJSONField(default=list, verbose_name='Изображения')

    class Meta:
        db_table = 'products'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        managed = False

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    images = SafeJSONField(default=list, verbose_name='Изображения')

    class Meta:
        db_table = 'blog_posts'
        verbose_name = 'Пост блога'
        verbose_name_plural = 'Посты блога'
        managed = False

    def __str__(self):
        return self.title

class Request(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    comment = models.TextField(verbose_name='Комментарий')

    class Meta:
        db_table = 'requests'
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        managed = False

    def __str__(self):
        return f'{self.name} - {self.phone}'

class Review(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    review = models.TextField(verbose_name='Отзыв')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        db_table = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        managed = False

    def __str__(self):
        return f'{self.name} - {self.created_at.strftime("%d.%m.%Y")}'