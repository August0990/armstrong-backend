import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, CompanyInfo, Product, BlogPost, Request, Review
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import json
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

app = FastAPI()
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Создаем папку uploads если не существует
os.makedirs("uploads", exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === IMAGE UPLOAD ===
@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"path": f"/uploads/{file.filename}"}

# === COMPANY INFO ===
@app.post("/company-info")
async def update_company_info(
    phone: str = Form(...),
    email: str = Form(...),
    address: str = Form(...),
    social_links: str = Form(...)  # JSON строка
):
    db = Session()
    try:
        # Удаляем существующую запись (если есть)
        db.query(CompanyInfo).delete()
        
        # Создаем новую запись
        company_info = CompanyInfo(
            phone=phone,
            email=email,
            address=address,
            social_links=json.loads(social_links)
        )
        db.add(company_info)
        db.commit()
        return {"status": "ok"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/company-info")
async def get_company_info():
    db = Session()
    try:
        company_info = db.query(CompanyInfo).first()
        if not company_info:
            raise HTTPException(status_code=404, detail="Company info not found")
        
        return {
            "phone": company_info.phone,
            "email": company_info.email,
            "address": company_info.address,
            "social_links": company_info.social_links
        }
    finally:
        db.close()

# === PRODUCTS ===
@app.post("/add-product")
async def add_product(
    title: str = Form(...),
    guarantee: str = Form(...),
    region: str = Form(...),
    price_retail: int = Form(...),
    price_wholesale: int = Form(...),
    price_bulk: int = Form(...),
    description: str = Form(...),
    attributes: str = Form(...),  # JSON строка
    images: str = Form(...)       # JSON строка
):
    db = Session()
    try:
        product = Product(
            title=title,
            guarantee=guarantee,
            region=region,
            price_retail=price_retail,
            price_wholesale=price_wholesale,
            price_bulk=price_bulk,
            description=description,
            attributes=json.loads(attributes),
            images=json.loads(images)
        )
        db.add(product)
        db.commit()
        return {"status": "ok", "product_id": product.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/products")
async def get_products():
    db = Session()
    try:
        products = db.query(Product).all()
        return [{
            "id": p.id,
            "title": p.title,
            "attributes": p.attributes,
            "guarantee": p.guarantee,
            "region": p.region,
            "price_retail": p.price_retail,
            "price_wholesale": p.price_wholesale,
            "price_bulk": p.price_bulk,
            "description": p.description,
            "images": p.images
        } for p in products]
    finally:
        db.close()

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    db = Session()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return {
            "id": product.id,
            "title": product.title,
            "attributes": product.attributes,
            "guarantee": product.guarantee,
            "region": product.region,
            "price_retail": product.price_retail,
            "price_wholesale": product.price_wholesale,
            "price_bulk": product.price_bulk,
            "description": product.description,
            "images": product.images
        }
    finally:
        db.close()

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    db = Session()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        db.delete(product)
        db.commit()
        return {"status": "ok"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# === BLOG POSTS ===
@app.post("/add-blog-post")
async def add_blog_post(
    title: str = Form(...),
    content: str = Form(...),
    images: str = Form(...)  # JSON строка
):
    db = Session()
    try:
        blog_post = BlogPost(
            title=title,
            content=content,
            images=json.loads(images)
        )
        db.add(blog_post)
        db.commit()
        return {"status": "ok", "blog_post_id": blog_post.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/blog-posts")
async def get_blog_posts():
    db = Session()
    try:
        posts = db.query(BlogPost).all()
        return [{
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "images": p.images
        } for p in posts]
    finally:
        db.close()

@app.get("/blog-posts/{post_id}")
async def get_blog_post(post_id: int):
    db = Session()
    try:
        post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Blog post not found")
        
        return {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "images": post.images
        }
    finally:
        db.close()

@app.delete("/blog-posts/{post_id}")
async def delete_blog_post(post_id: int):
    db = Session()
    try:
        post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Blog post not found")
        
        db.delete(post)
        db.commit()
        return {"status": "ok"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# === REQUESTS ===
@app.post("/add-request")
async def add_request(
    name: str = Form(...),
    phone: str = Form(...),
    comment: str = Form(...)
):
    db = Session()
    try:
        request = Request(
            name=name,
            phone=phone,
            comment=comment
        )
        db.add(request)
        db.commit()
        return {"status": "ok", "request_id": request.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/requests")
async def get_requests():
    db = Session()
    try:
        requests = db.query(Request).all()
        return [{
            "id": r.id,
            "name": r.name,
            "phone": r.phone,
            "comment": r.comment
        } for r in requests]
    finally:
        db.close()

@app.delete("/requests/{request_id}")
async def delete_request(request_id: int):
    db = Session()
    try:
        request = db.query(Request).filter(Request.id == request_id).first()
        if not request:
            raise HTTPException(status_code=404, detail="Request not found")
        
        db.delete(request)
        db.commit()
        return {"status": "ok"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# === REVIEWS ===
@app.post("/add-review")
async def add_review(
    name: str = Form(...),
    review: str = Form(...)
):
    db = Session()
    try:
        review_obj = Review(
            name=name,
            review=review
        )
        db.add(review_obj)
        db.commit()
        return {"status": "ok", "review_id": review_obj.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/reviews")
async def get_reviews():
    db = Session()
    try:
        reviews = db.query(Review).all()
        return [{
            "id": r.id,
            "name": r.name,
            "review": r.review,
            "created_at": r.created_at.isoformat()
        } for r in reviews]
    finally:
        db.close()

@app.delete("/reviews/{review_id}")
async def delete_review(review_id: int):
    db = Session()
    try:
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        db.delete(review)
        db.commit()
        return {"status": "ok"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# === HEALTH CHECK ===
@app.get("/")
async def root():
    return {"message": "API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8538)