from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from models import User
from datetime import datetime

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('/profile')
@login_required
def profile():
    """User profile settings"""
    return render_template('settings/profile.html')

@settings_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update user profile"""
    try:
        data = request.get_json()
        
        # Update basic info
        if 'name' in data:
            current_user.name = data['name']
        
        if 'email' in data:
            # Check if email is already taken
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.id != current_user.id:
                return jsonify({'error': 'Email already exists'}), 400
            current_user.email = data['email']
        
        if 'phone' in data:
            current_user.phone = data['phone']
        
        if 'bio' in data:
            current_user.bio = data['bio']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'user': {
                'name': current_user.name,
                'email': current_user.email,
                'phone': current_user.phone,
                'bio': current_user.bio
            }
        })
        
    except Exception as e:
        print(f"❌ Profile update error: {e}")
        return jsonify({'error': 'Failed to update profile'}), 500

@settings_bp.route('/password', methods=['POST'])
@login_required
def update_password():
    """Update user password"""
    try:
        data = request.get_json()
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        
        # Verify current password
        if not current_user.check_password(current_password):
            return jsonify({'error': 'Current password is incorrect'}), 400
        
        # Validate new password
        if len(new_password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters long'}), 400
        
        if new_password != confirm_password:
            return jsonify({'error': 'Passwords do not match'}), 400
        
        # Update password
        current_user.set_password(new_password)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Password updated successfully'
        })
        
    except Exception as e:
        print(f"❌ Password update error: {e}")
        return jsonify({'error': 'Failed to update password'}), 500

@settings_bp.route('/preferences', methods=['POST'])
@login_required
def update_preferences():
    """Update user preferences"""
    try:
        data = request.get_json()
        
        # Update notification preferences
        if 'email_notifications' in data:
            current_user.email_notifications = data['email_notifications']
        
        if 'push_notifications' in data:
            current_user.push_notifications = data['push_notifications']
        
        if 'theme' in data:
            current_user.theme = data['theme']
        
        if 'language' in data:
            current_user.language = data['language']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Preferences updated successfully'
        })
        
    except Exception as e:
        print(f"❌ Preferences update error: {e}")
        return jsonify({'error': 'Failed to update preferences'}), 500

@settings_bp.route('/notifications')
@login_required
def notifications():
    """Notification settings page"""
    return render_template('settings/notifications.html')

@settings_bp.route('/security')
@login_required
def security():
    """Security settings page"""
    return render_template('settings/security.html')

@settings_bp.route('/account')
@login_required
def account():
    """Account settings page"""
    return render_template('settings/account.html')
