#!/usr/bin/env python3
"""
Main entry point for Railway deployment
Fallback for when Railway looks for main:app
"""
from wsgi import app

if __name__ == "__main__":
    app.run()
