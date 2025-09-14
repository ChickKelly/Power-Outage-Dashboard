# Power Outage Alert Web Application

A comprehensive, real-time power outage monitoring and management system built with Django. This professional-grade application enables repair teams to efficiently track, acknowledge, and resolve power outages in remote communities with advanced analytics, real-time notifications, and interactive mapping capabilities.

## 🚀 Features

### Core Functionality
- **Advanced Analytics Dashboard**: Comprehensive statistics with interactive charts and performance metrics
- **Real-Time Monitoring**: Live power status monitoring of all communities with instant updates
- **WebSocket Notifications**: Immediate alerts when outages occur with auto-dismissing notifications
- **Interactive Location Map**: Visual representation of community locations with color-coded power status indicators
- **Complete Repair Workflow**: Full outage lifecycle management with acknowledgment and resolution tracking
- **Historical Analytics**: Detailed outage history with trend analysis and reporting capabilities
- **Role-Based Access Control**: Granular permissions for Admins and Repair Team members

### Advanced Dashboard Features
- **Statistics Cards**: Key metrics including Communities Monitored, Active Outages, Resolved Today, and Team Members
- **Outage Analytics Chart**: Interactive 6-month trend visualization using Chart.js
- **Performance Metrics**: System uptime tracking, average resolution time, and response rate indicators
- **Team Management**: Complete team member statistics with role distribution
- **Quick Actions Panel**: Direct access to History, Map, Admin Panel, and Report Generation

### Technical Features
- **Secure Authentication**: Django's built-in authentication with custom user roles and validation
- **Real-Time Communication**: WebSocket support via Django Channels with connection management
- **Modern Responsive Design**: Professional UI with light gradient backgrounds and card-based layout
- **Enhanced Admin Panel**: Comprehensive data management with custom admin interfaces
- **Location Tracking**: Interactive maps using Leaflet.js with accurate coordinate positioning
- **Data Visualization**: Professional charts and metrics with Chart.js integration
- **Advanced Form Validation**: Comprehensive client and server-side validation with real-time feedback
- **User-Friendly Dialog System**: Professional confirmation dialogs and error messaging
- **Interactive UI Components**: Loading states, animations, and responsive design elements

## 🛠️ Technology Stack

- **Backend**: Django 5.2.6, Python 3.13
- **Real-Time**: Django Channels, WebSockets
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **Mapping**: Leaflet.js with OpenStreetMap tiles
- **Database**: SQLite (development), PostgreSQL ready
- **Static Files**: WhiteNoise middleware
- **Validation**: Advanced client-side and server-side form validation with real-time feedback
- **UI Components**: Modern card-based design with responsive grid layouts
- **Dialog System**: Professional confirmation dialogs and animated message notifications

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd power-outage-alert
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### 6. Run the Development Server
```bash
python manage.py runserver
```

### 7. Access the Application
- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 📖 Usage Guide

### Getting Started
1. **Sign Up**: Create a new account at the main page with comprehensive form validation
2. **Choose Role**: Select either "Admin" or "Repair Team" during registration
3. **Login**: Access the dashboard with your credentials and receive welcome messages

### Advanced Dashboard Features
- **Statistics Overview**: Real-time metrics showing Communities Monitored, Active Outages, Resolved Today, and Team Members
- **Analytics Chart**: Interactive 6-month outage trend visualization with Chart.js
- **Performance Metrics**: System uptime indicators and average resolution time tracking
- **Active Outages Management**: Live outage list with acknowledge/resolve workflow buttons
- **Community Status Panel**: Real-time power status with coordinates and online/offline indicators
- **Quick Actions Grid**: Direct access to History, Map, Admin Panel, and Report Generation

### Outage Management Workflow
1. **Detection**: Outages automatically appear on dashboard with timestamps
2. **Acknowledge**: Repair team members acknowledge when starting work on an outage (with confirmation dialog)
3. **Resolve**: Mark outages as resolved when power is restored (with confirmation dialog)
4. **Track Progress**: Complete audit trail with user assignments and timestamps
5. **Analytics**: Historical data feeds into trend analysis and performance metrics
6. **User Feedback**: Success/error messages provide immediate feedback for all actions

### Enhanced Admin Panel
Comprehensive data management interface:
- **User Management**: Add/edit repair team members and administrators with role assignments
- **Community Configuration**: Manage community information with precise coordinates for mapping
- **Outage Records**: Complete outage database with search, filter, and export capabilities
- **System Statistics**: Overview of system performance and usage metrics

### Interactive Location Map
- **Accurate Positioning**: Communities positioned using real GPS coordinates
- **Color-Coded Status**: Green markers for powered communities, red for outages
- **Interactive Popups**: Click markers to view detailed community information and current status
- **Real-Time Updates**: Map updates automatically when power status changes

## 🧪 Testing Outages

To simulate power outages for testing:

```bash
python manage.py trigger_outage <community_id> off
```

To restore power:
```bash
python manage.py trigger_outage <community_id> on
```

Replace `<community_id>` with the ID of a community from the admin panel.

## 📁 Project Structure

```
power_outage_alert/
├── power_outage_alert/          # Main project settings
│   ├── settings.py              # Django configuration
│   ├── urls.py                  # Main URL routing
│   ├── asgi.py                  # ASGI configuration for WebSockets
│   └── wsgi.py                  # WSGI configuration
├── outages/                     # Main application
│   ├── models.py                # Database models
│   ├── views.py                 # View logic
│   ├── urls.py                  # URL patterns
│   ├── admin.py                 # Admin panel configuration
│   ├── forms.py                 # Form definitions
│   ├── consumers.py             # WebSocket consumers
│   ├── routing.py               # WebSocket routing
│   ├── templates/               # HTML templates
│   ├── static/                  # CSS, JS, images
│   └── management/              # Custom management commands
├── db.sqlite3                   # Database file
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🔧 Configuration

### Environment Variables
For production deployment, set these environment variables:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection string (if using PostgreSQL)

### WebSocket Configuration
The application uses Django Channels for real-time notifications. The WebSocket endpoint is available at:
```
ws://127.0.0.1:8000/ws/outages/
```

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Set up a production database (PostgreSQL recommended)
4. Configure static file serving
5. Set up SSL/HTTPS
6. Configure WebSocket support on your server

### Docker Deployment (Optional)
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 API Endpoints

### Authentication
- `GET /` - Login page
- `POST /signup/` - User registration
- `POST /logout/` - User logout

### Dashboard
- `GET /dashboard/` - Main dashboard
- `GET /history/` - Outage history
- `GET /map/` - Interactive map

### Outage Management
- `POST /outage/<id>/acknowledge/` - Acknowledge outage
- `POST /outage/<id>/resolve/` - Resolve outage

### WebSocket
- `ws://host/ws/outages/` - Real-time notifications

## 🔒 Security Features

- **CSRF Protection**: All forms include CSRF tokens
- **User Authentication**: Secure login/logout system with custom authentication forms
- **Role-Based Access**: Different permissions for admins and repair teams
- **Advanced Input Validation**: Comprehensive form validation and sanitization with real-time feedback
- **Session Management**: Secure session handling
- **Error Handling**: Graceful error recovery with user-friendly messages

## 📊 Database Schema

### User Model
- Custom user model extending Django's AbstractUser
- Additional `role` field for access control

### Community Model
- Name, latitude, longitude coordinates
- Power status (boolean)

### Outage Model
- Community reference
- Start/end timestamps
- Acknowledgment tracking
- Resolution tracking
- User assignments

## 🎨 UI/UX Features

- **Animated Gradient Background**: Dynamic color transitions with lightened purple/lavender theme
- **Floating Bubble Effects**: Subtle animations for visual appeal
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-Time Updates**: Live notifications without page refresh
- **Professional Styling**: Clean, modern interface design with card-based layout
- **Interactive Dialogs**: Professional confirmation dialogs with smooth animations
- **Message System**: Toast-style notifications with auto-dismiss and manual close options
- **Form Validation UI**: Real-time visual feedback with success/error states
- **Loading States**: Button loading animations during form submissions and actions
- **Hover Effects**: Interactive elements with smooth transitions and visual feedback

## 📞 Support

For support, feature requests, or bug reports, please create an issue in the GitHub repository.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django framework for the robust backend
- Leaflet.js for interactive mapping
- Django Channels for WebSocket support
- OpenStreetMap for map tiles

---

**Built with ❤️ for reliable power outage management**
