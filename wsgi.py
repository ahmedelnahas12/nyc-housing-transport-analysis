# WSGI entry point for Vercel
# This must be at project root for Vercel to find it
from website.app import server as application

# Vercel expects a WSGI callable named 'application' or 'app' at module level
# Dash's server is a Flask app (WSGI compliant)