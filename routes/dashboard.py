from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models.complaint import Complaint
from models.service_request import ServiceRequest


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    total_complaints = Complaint.query.count()

    pending_complaints = Complaint.query.filter_by(
        status="New"
    ).count()

    in_progress = Complaint.query.filter_by(
        status="In Progress"
    ).count()

    resolved = Complaint.query.filter_by(
        status="Resolved"
    ).count()

    closed = Complaint.query.filter_by(
        status="Closed"
    ).count()

    total_service_requests = ServiceRequest.query.count()

    return render_template(
        "dashboard.html",
        total_complaints=total_complaints,
        pending_complaints=pending_complaints,
        in_progress=in_progress,
        resolved=resolved,
        closed=closed,
        total_service_requests=total_service_requests
    )


# =========================
# ADMIN DASHBOARD
# =========================

@dashboard_bp.route("/admin-dashboard")
@login_required
def admin_dashboard():

    return render_template(
        "admin_dashboard.html"
    )


# =========================
# STAFF DASHBOARD
# =========================

@dashboard_bp.route("/staff-dashboard")
@login_required
def staff_dashboard():

    return render_template(
        "staff_dashboard.html"
    )


# =========================
# CUSTOMER DASHBOARD
# =========================

@dashboard_bp.route("/customer-dashboard")
@login_required
def customer_dashboard():

    return render_template(
        "customer_dashboard.html"
    )