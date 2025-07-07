from sqlalchemy import Column, Integer, String, JSON, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class CompanyInfo(Base):
    __tablename__ = 'company_info'
    
    id = Column(Integer, primary_key=True)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String, nullable=False)
    social_links = Column(JSON)  # {"whatsapp": "...", "instagram": "...", "telegram": "..."}

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    attributes = Column(JSON)  # {"Освещение": "Лампы", "состав материала": "дерево", "материалы из": "Европа"}
    guarantee = Column(String)  # "12 мес"
    region = Column(String)     # "Кыргызстан"
    price_retail = Column(Integer)
    price_wholesale = Column(Integer)
    price_bulk = Column(Integer)
    description = Column(Text)
    images = Column(JSON)  # ["/uploads/img1.jpg", "/uploads/img2.jpg"]

class BlogPost(Base):
    __tablename__ = 'blog_posts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    images = Column(JSON)  # ["/uploads/blog1.jpg", "/uploads/blog2.jpg"]

class Request(Base):
    __tablename__ = 'requests'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    comment = Column(Text)

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    review = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
