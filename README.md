# Lagrange Interpolation Animator

A comprehensive web application for Lagrange polynomial interpolation with animation capabilities and Odoo integration.

## Features

### Core Functionality
- **Interactive Point Input**: Add interpolation points through a modern web interface
- **Real-time Visualization**: Dynamic plotting using Plotly.js
- **Lagrange Interpolation**: Mathematical implementation with polynomial coefficient calculation
- **Animation Support**: Step-by-step visualization of interpolation process
- **REST API**: Complete API for programmatic access

### Odoo Integration
- **Docker-based Odoo**: Seamless integration with Odoo using Docker Desktop
- **Custom Odoo Module**: Purpose-built module for interpolation data management
- **Data Synchronization**: Automatic transfer of interpolation results to Odoo
- **Business Intelligence**: Advanced reporting and analysis in Odoo

## Architecture

### Backend (Django)
- **Django REST Framework**: RESTful API endpoints
- **PostgreSQL Database**: Robust data persistence
- **Environment Configuration**: Secure configuration management
- **CORS Support**: Frontend-backend communication

### Frontend (HTML/JavaScript)
- **Modern UI**: Beautiful, responsive design
- **Interactive Plotting**: Plotly.js for mathematical visualization
- **Real-time Updates**: Dynamic content updates
- **Animation Controls**: Play/pause/step animation features

### Odoo Integration
- **Custom Module**: `lagrange_integration` addon
- **Data Models**: Structured interpolation data storage
- **Views & Reports**: Comprehensive data analysis
- **Docker Deployment**: Easy setup and scaling

## Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL
- Docker Desktop
- Node.js (for frontend dependencies)

### Installation

1. **Clone and Setup**
   ```bash
   cd lagrange_animator
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Start Services**
   ```bash
   # Start Django
   source lagrange_env/bin/activate
   python manage.py runserver
   
   # Start Odoo (in another terminal)
   docker-compose up -d
   ```

3. **Access Applications**
   - **Main App**: http://localhost:8000
   - **Odoo**: http://localhost:8069
   - **API Documentation**: http://localhost:8000/api/

## Usage

### Web Interface

1. **Add Points**: Input X,Y coordinates using the form
2. **Visualize**: See points plotted in real-time
3. **Interpolate**: Generate Lagrange polynomial
4. **Animate**: Watch step-by-step interpolation process
5. **Export**: Send results to Odoo for analysis

### API Endpoints

#### Direct Interpolation
```bash
POST /api/interpolate/
Content-Type: application/json

{
  "points": [[1, 2], [2, 4], [3, 8]],
  "x_values": [1.5, 2.5, 3.5]
}
```

#### Managed Sets
```bash
# Create interpolation set
POST /api/sets/
{
  "name": "Test Set",
  "description": "Sample interpolation"
}

# Add points to set
POST /api/sets/{id}/add_point/
{
  "x": 1.5,
  "y": 2.25
}

# Perform interpolation
POST /api/sets/{id}/interpolate/
```

#### Odoo Integration
```bash
# Send data to Odoo
POST /api/odoo/send/
{
  "interpolation_data": {
    "original_points": [[1,2], [2,4]],
    "coefficients": [0.5, 1.5],
    "evaluation_points": [1.5, 2.5],
    "evaluation_results": [2.25, 4.75]
  }
}

# Check Odoo status
GET /api/odoo/send/
```

## Configuration

### Environment Variables (.env)

```env
# Django Configuration
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=lagrange_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Odoo Configuration
ODOO_HOST=localhost
ODOO_PORT=8069
ODOO_DB=odoo_db
ODOO_USER=admin
ODOO_PASSWORD=admin

# API Configuration
API_BASE_URL=http://localhost:8000/api
FRONTEND_URL=http://localhost:3000
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## Mathematical Background

### Lagrange Interpolation

Given n+1 data points (x₀,y₀), (x₁,y₁), ..., (xₙ,yₙ), the Lagrange interpolating polynomial is:

```
P(x) = Σ(i=0 to n) yᵢ * Lᵢ(x)
```

Where Lᵢ(x) is the i-th Lagrange basis polynomial:

```
Lᵢ(x) = Π(j=0 to n, j≠i) (x - xⱼ)/(xᵢ - xⱼ)
```

### Features
- **Exact Interpolation**: Polynomial passes through all given points
- **Unique Solution**: For n+1 points, there's exactly one polynomial of degree ≤ n
- **Numerical Stability**: Optimized implementation for accuracy

## Development

### Project Structure
```
lagrange_animator/
├── lagrange_project/          # Django project settings
├── interpolation_app/         # Main Django app
│   ├── models.py             # Data models
│   ├── views.py              # API endpoints
│   ├── serializers.py        # API serialization
│   ├── lagrange.py           # Mathematical implementation
│   └── templates/            # Frontend templates
├── addons/                   # Odoo custom modules
│   └── lagrange_integration/ # Interpolation Odoo module
├── config/                   # Configuration files
├── docker-compose.yml        # Odoo deployment
└── requirements.txt          # Python dependencies
```

### API Testing

Use the Django REST Framework browsable API at `/api/` or tools like curl:

```bash
# Test interpolation
curl -X POST http://localhost:8000/api/interpolate/ \
  -H "Content-Type: application/json" \
  -d '{"points": [[0,0], [1,1], [2,4]]}'

# Test Odoo integration
curl -X GET http://localhost:8000/api/odoo/send/
```

## Deployment

### Production Setup

1. **Environment Configuration**
   - Set `DEBUG=False`
   - Configure secure `SECRET_KEY`
   - Set up production database

2. **Docker Deployment**
   ```bash
   # Production docker-compose
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

### Security Considerations
- Environment variables for sensitive data
- CORS configuration for frontend access
- Database security and backups
- Odoo security configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the API documentation
- Review the mathematical implementation

---

**Keywords**: Lagrange interpolation, polynomial interpolation, Django, Odoo, mathematical visualization, REST API, animation, Docker