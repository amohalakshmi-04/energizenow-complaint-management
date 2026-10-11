from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user

from models import db
from models.complaint import Complaint
from models.user import User
from models.category import Category
from utils.validators import role_required


complaints_bp = Blueprint("complaints", __name__)


# =========================================================
# CUSTOMER - ADD COMPLAINT
# =========================================================

@complaints_bp.route("/customer/complaints/add", methods=["GET", "POST"])
@role_required("customer")
def customer_add_complaint():

    categories = Category.query.order_by(Category.name).all()

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "Medium")
        category_id = request.form.get("category_id")

        if not title or not description:
            flash("Title and description are required.", "danger")

            return render_template(
                "complaints/add.html",
                categories=categories
            )

        complaint = Complaint(
            title=title,
            description=description,
            priority=priority,
            status="New",
            customer_id=current_user.id,
            category_id=int(category_id) if category_id else None
        )

        db.session.add(complaint)
        db.session.commit()

        flash("Complaint submitted successfully!", "success")

        return redirect(
            url_for("complaints.customer_complaints")
        )

    return render_template(
        "complaints/add.html",
        categories=categories
    )


# =========================================================
# CUSTOMER - VIEW ALL OWN COMPLAINTS
# =========================================================

@complaints_bp.route("/customer/complaints")
@role_required("customer")
def customer_complaints():

    complaints = Complaint.query.filter_by(
        customer_id=current_user.id
    ).order_by(
        Complaint.created_at.desc()
    ).all()

    return render_template(
        "complaints/list.html",
        complaints=complaints,
        page_title="My Complaints"
    )


# =========================================================
# CUSTOMER - VIEW SINGLE COMPLAINT
# =========================================================

@complaints_bp.route("/customer/complaints/<int:complaint_id>")
@role_required("customer")
def customer_view_complaint(complaint_id):

    complaint = Complaint.query.filter_by(
        id=complaint_id,
        customer_id=current_user.id
    ).first_or_404()

    return render_template(
        "complaints/view.html",
        complaint=complaint,
        customer_view=True
    )


# =========================================================
# CUSTOMER - DELETE COMPLAINT
# =========================================================

@complaints_bp.route(
    "/customer/complaints/<int:complaint_id>/delete",
    methods=["POST"]
)
@role_required("customer")
def customer_delete_complaint(complaint_id):

    # Only allow the logged-in customer to delete
    # their own complaint.
    complaint = Complaint.query.filter_by(
        id=complaint_id,
        customer_id=current_user.id
    ).first_or_404()

    # Allow deletion only when complaint is still New.
    if complaint.status != "New":
        flash(
            "Only new complaints can be deleted.",
            "danger"
        )

        return redirect(
            url_for("complaints.customer_complaints")
        )

    db.session.delete(complaint)
    db.session.commit()

    flash(
        "Complaint deleted successfully.",
        "success"
    )

    return redirect(
        url_for("complaints.customer_complaints")
    )


# =========================================================
# ADMIN - VIEW ALL COMPLAINTS
# =========================================================

@complaints_bp.route("/admin/complaints")
@role_required("admin")
def admin_complaints():

    complaints = Complaint.query.order_by(
        Complaint.created_at.desc()
    ).all()

    return render_template(
        "complaints/list.html",
        complaints=complaints,
        page_title="All Complaints",
        admin_view=True
    )


# =========================================================
# ADMIN - ASSIGN COMPLAINT TO STAFF
# =========================================================

@complaints_bp.route(
    "/admin/complaints/<int:complaint_id>/assign",
    methods=["GET", "POST"]
)
@role_required("admin")
def assign_complaint(complaint_id):

    complaint = Complaint.query.get_or_404(complaint_id)

    staff_members = User.query.filter_by(
        role="staff"
    ).order_by(
        User.name
    ).all()

    if request.method == "POST":

        staff_id = request.form.get("staff_id")

        if not staff_id:

            flash(
                "Please select a staff member.",
                "danger"
            )

            return render_template(
                "complaints/assign.html",
                complaint=complaint,
                staff_members=staff_members
            )

        staff = User.query.filter_by(
            id=int(staff_id),
            role="staff"
        ).first()

        if not staff:

            flash(
                "Invalid staff member.",
                "danger"
            )

            return render_template(
                "complaints/assign.html",
                complaint=complaint,
                staff_members=staff_members
            )

        complaint.assigned_to = staff.id
        complaint.status = "Assigned"

        db.session.commit()

        flash(
            f"Complaint assigned to {staff.name}.",
            "success"
        )

        return redirect(
            url_for("complaints.admin_complaints")
        )

    return render_template(
        "complaints/assign.html",
        complaint=complaint,
        staff_members=staff_members
    )


# =========================================================
# ADMIN - VIEW SINGLE COMPLAINT
# =========================================================

@complaints_bp.route(
    "/admin/complaints/<int:complaint_id>"
)
@role_required("admin")
def admin_view_complaint(complaint_id):

    complaint = Complaint.query.get_or_404(
        complaint_id
    )

    return render_template(
        "complaints/view.html",
        complaint=complaint,
        admin_view=True
    )


# =========================================================
# STAFF - VIEW ASSIGNED COMPLAINTS
# =========================================================

@complaints_bp.route("/staff/complaints")
@role_required("staff")
def staff_complaints():

    complaints = Complaint.query.filter_by(
        assigned_to=current_user.id
    ).order_by(
        Complaint.created_at.desc()
    ).all()

    return render_template(
        "complaints/list.html",
        complaints=complaints,
        page_title="Assigned Complaints",
        staff_view=True
    )


# =========================================================
# STAFF - VIEW SINGLE COMPLAINT
# =========================================================

@complaints_bp.route(
    "/staff/complaints/<int:complaint_id>"
)
@role_required("staff")
def staff_view_complaint(complaint_id):

    complaint = Complaint.query.filter_by(
        id=complaint_id,
        assigned_to=current_user.id
    ).first_or_404()

    return render_template(
        "complaints/view.html",
        complaint=complaint,
        staff_view=True
    )


# =========================================================
# STAFF - UPDATE COMPLAINT
# =========================================================

@complaints_bp.route(
    "/staff/complaints/<int:complaint_id>/update",
    methods=["GET", "POST"]
)
@role_required("staff")
def update_complaint(complaint_id):

    complaint = Complaint.query.filter_by(
        id=complaint_id,
        assigned_to=current_user.id
    ).first_or_404()

    if request.method == "POST":

        status = request.form.get(
            "status",
            "In Progress"
        )

        resolution = request.form.get(
            "resolution",
            ""
        ).strip()

        allowed_statuses = [
            "Assigned",
            "In Progress",
            "Resolved"
        ]

        if status not in allowed_statuses:

            flash(
                "Invalid status.",
                "danger"
            )

            return redirect(
                url_for(
                    "complaints.staff_view_complaint",
                    complaint_id=complaint.id
                )
            )

        if status == "Resolved" and not resolution:

            flash(
                "Please enter the resolution before marking it resolved.",
                "danger"
            )

            return render_template(
                "complaints/edit.html",
                complaint=complaint,
                staff_view=True
            )

        complaint.status = status
        complaint.resolution = resolution

        db.session.commit()

        flash(
            "Complaint updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "complaints.staff_view_complaint",
                complaint_id=complaint.id
            )
        )

    return render_template(
        "complaints/edit.html",
        complaint=complaint,
        staff_view=True
    )