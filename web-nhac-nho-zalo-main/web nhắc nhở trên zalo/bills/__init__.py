from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from models import db, Bill, Notification
from utils.helpers import format_currency, parse_currency

bills = Blueprint('bills', __name__)

@bills.route('/bills')
@login_required
def index():
    user_bills = Bill.query.filter_by(user_id=current_user.id).order_by(Bill.due_date).all()
    return render_template('bills/index.html', bills=user_bills)

@bills.route('/bills/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        try:
            amount = parse_currency(request.form.get('amount'))
            due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%d')
            
            new_bill = Bill(
                title=request.form.get('title'),
                description=request.form.get('description'),
                amount=amount,
                due_date=due_date,
                user_id=current_user.id
            )
            
            db.session.add(new_bill)
            
            # Create notification for the bill
            notification = Notification(
                user_id=current_user.id,
                bill_id=new_bill.id,
                message=f"New bill '{new_bill.title}' due on {due_date.strftime('%Y-%m-%d')}",
                notification_date=due_date
            )
            db.session.add(notification)
            
            db.session.commit()
            flash('Bill created successfully!', 'success')
            return redirect(url_for('bills.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating bill: {str(e)}', 'error')
            
    return render_template('bills/create.html')

@bills.route('/bills/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    bill = Bill.query.get_or_404(id)
    
    if bill.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('bills.index'))
        
    if request.method == 'POST':
        try:
            bill.title = request.form.get('title')
            bill.description = request.form.get('description')
            bill.amount = parse_currency(request.form.get('amount'))
            bill.due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%d')
            
            db.session.commit()
            flash('Bill updated successfully!', 'success')
            return redirect(url_for('bills.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating bill: {str(e)}', 'error')
            
    return render_template('bills/edit.html', bill=bill)

@bills.route('/bills/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    bill = Bill.query.get_or_404(id)
    
    if bill.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('bills.index'))
        
    try:
        # Delete associated notifications first
        Notification.query.filter_by(bill_id=id).delete()
        
        db.session.delete(bill)
        db.session.commit()
        flash('Bill deleted successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting bill: {str(e)}', 'error')
        
    return redirect(url_for('bills.index'))

@bills.route('/bills/<int:id>/mark-paid', methods=['POST'])
@login_required
def mark_paid(id):
    bill = Bill.query.get_or_404(id)
    
    if bill.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('bills.index'))
        
    try:
        bill.is_paid = True
        bill.paid_date = datetime.now()
        db.session.commit()
        flash('Bill marked as paid!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating bill status: {str(e)}', 'error')
        
    return redirect(url_for('bills.index'))
