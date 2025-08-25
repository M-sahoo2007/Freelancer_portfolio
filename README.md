 # Zola Becker - Creative Portfolio

A modern, responsive portfolio website built with HTML, CSS, JavaScript, and Python (Flask).

## Features

- Responsive design that works on all devices
- Interactive navigation with smooth scrolling
- Project showcase with hover effects
- Client work sections
- Services overview
- Contact form with email notifications
- Modern animations and transitions

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update with your email configuration:

```bash
cp .env.example .env
```

Edit `.env` with your email settings:
- `EMAIL_ADDRESS`: Your Gmail address
- `EMAIL_PASSWORD`: Your Gmail app password (not your regular password)
- `RECIPIENT_EMAIL`: Where you want to receive form submissions

### 3. Run the Development Server

```bash
python app.py
```

The website will be available at `http://localhost:5000`

### 4. Production Deployment

For production, use gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## File Structure

```
├── index.html              # Main HTML file
├── app.py                  # Python Flask backend
├── styles/
│   ├── main.css           # Main styles and utilities
│   ├── components.css     # Component-specific styles
│   └── responsive.css     # Responsive breakpoints
├── scripts/
│   └── main.js           # JavaScript functionality
├── submissions/          # Form submissions (auto-created)
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

## Email Configuration

To enable the contact form:

1. Enable 2-factor authentication on your Gmail account
2. Generate an app-specific password in Google Account settings
3. Use this app password in the `EMAIL_PASSWORD` environment variable

## Features

### Frontend
- Pure HTML/CSS/JavaScript (no frameworks)
- Responsive grid layouts
- Smooth scrolling navigation
- Interactive animations
- Form validation
- Mobile-friendly navigation

### Backend
- Flask web server
- Email notifications for form submissions
- Form data backup to JSON files
- CORS enabled for API calls
- Error handling and logging
- Health check endpoint

## Customization

### Colors and Styling
Edit the CSS custom properties in `styles/main.css`:

```css
:root {
    --primary: #030213;
    --background: #ffffff;
    --foreground: #1a1a1a;
    /* ... more variables */
}
```

### Content
Update the content directly in `index.html` or modify the JavaScript in `scripts/main.js` for dynamic content.

### Images
Replace the Unsplash URLs with your own images in `index.html`.

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## License

This project is open source and available under the MIT License.