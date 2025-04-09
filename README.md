# Product Management API

A RESTful API for managing products, categories, and tags built with Django and Django REST Framework.

## Features

- User authentication with token-based authentication
- CRUD operations for products, categories, and tags
- Filtering products by category and tags
- Search functionality for products
- API documentation with Swagger/OpenAPI
- Docker containerization for easy deployment
- Django admin interface for data management

## Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd product-app-api
```

2. Build and start the Docker containers:
```bash
docker-compose build
docker-compose up
```

The API will be available at http://localhost:8000

## Testing functionality of Backend

1. Go to the API documentation:
- Swagger UI: http://localhost:8000/api/docs/
- Create User with /api/user/create
- Create Token with /api/user/token
- Authorize with created token in Swagger for further use

2. Go to the Fronend(Django Template):
- Frontend : http://localhost:8000/api/product/frontend/
- Frontend does not have all the backend features and endpoints. (All the endpoints can be seen in Swagger UI)

## Creating a Django Admin User with Docker

To create a Django admin user for accessing the admin interface, follow these steps:

1. Create a superuser by running the following command:
```bash
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```

2. Follow the prompts to enter:
   - Email address
   - Password (and confirm it)

3. Access the Django admin interface at:
```
http://localhost:8000/admin/
```

4. Log in with the superuser credentials you created.
    - Create at least 5 categories, 10 tags, and 20 products.


## API Endpoints

### Authentication
- `POST /api/user/create/` - Create a new user
- `POST /api/user/token/` - Get authentication token
- `GET /api/user/me/` - Get current user details

### Products
- `GET /api/product/products/` - List all products
- `POST /api/product/products/` - Create a new product
- `GET /api/product/products/{id}/` - Get product details
- `PUT /api/product/products/{id}/` - Update product
- `PATCH /api/product/products/{id}/` - Partial update
- `DELETE /api/product/products/{id}/` - Delete product

### Categories
- `GET /api/product/categories/` - List all categories
- `PUT /api/product/categories/{id}/` - Update category
- `PATCH /api/product/categories/{id}/` - Partial update
- `DELETE /api/product/categories/{id}/` - Delete category

### Tags
- `GET /api/product/tags/` - List all tags
- `PUT /api/product/tags/{id}/` - Update tag
- `PATCH /api/product/tags/{id}/` - Partial update
- `DELETE /api/product/tags/{id}/` - Delete tag


## Testing

Run the tests using:
```bash
docker-compose run --rm app sh -c "python manage.py test"
```

## Project Structure

```
product-app-api/
├── app/                    # Main project directory
│   ├── core/              # Core app (models, etc.)
│   ├── product/           # Product app
│   ├── user/              # User app
│   └── app/               # Project settings
├── templates/             # HTML templates
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker Compose configuration
└── Dockerfile            # Docker configuration
```

## Optimization Techniques(Future Considerations)

### Asynchronous Views

The API can be optimized using Django 5's async support:

```python
from asgiref.sync import sync_to_async

class ProductViewSet(viewsets.ModelViewSet):
    async def get_queryset(self):
        return await sync_to_async(lambda: self.queryset.filter(user=self.request.user))()
```

### Related Queries

Optimize database queries with `select_related` and `prefetch_related`:

```python
def get_queryset(self):
    return self.queryset.select_related('category').prefetch_related('tags')
```

### Fix the Frontend

Frontend does not have all the features, and it has bugs that should be fixed.
Frontend was built very fast pace with AI, so it has problems.
