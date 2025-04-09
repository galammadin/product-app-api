# Product Management API

A RESTful API for managing products, categories, and tags built with Django and Django REST Framework.

## Features

- User authentication with token-based authentication
- CRUD operations for products, categories, and tags
- Filtering products by category and tags
- Search functionality for products
- API documentation with Swagger/OpenAPI

## Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose
- PostgreSQL (if running locally)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd product-app-api
```

2. Create a `.env` file in the root directory with the following variables:
```env
DB_HOST=db
DB_NAME=app_db
DB_USER=app_user
DB_PASS=app_password
```

3. Build and start the Docker containers:
```bash
docker-compose build
docker-compose up
```

The API will be available at http://localhost:8000

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
- `POST /api/product/categories/` - Create a new category
- `GET /api/product/categories/{id}/` - Get category details
- `PUT /api/product/categories/{id}/` - Update category
- `PATCH /api/product/categories/{id}/` - Partial update
- `DELETE /api/product/categories/{id}/` - Delete category

### Tags
- `GET /api/product/tags/` - List all tags
- `POST /api/product/tags/` - Create a new tag
- `GET /api/product/tags/{id}/` - Get tag details
- `PUT /api/product/tags/{id}/` - Update tag
- `PATCH /api/product/tags/{id}/` - Partial update
- `DELETE /api/product/tags/{id}/` - Delete tag

## API Documentation

The API documentation is available at:
- Swagger UI: http://localhost:8000/api/docs/
- OpenAPI Schema: http://localhost:8000/api/schema/

## Testing

Run the tests using:
```bash
docker-compose run app python manage.py test
```

## Development

To run the project locally without Docker:

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the database:
```bash
python manage.py migrate
```

4. Run the development server:
```bash
python manage.py runserver
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

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.
