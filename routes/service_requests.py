from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user

from models import db
from models.service_request import ServiceRequest
from models.user import User
from utils.validators import role_required


service_requests_bp = Blueprint(
    "service_requests",
    __name__
)


# =========================================================
# CUSTOMER - ADD SERVICE REQUEST
# =========================================================

@service_requests_bp.route(
    "/customer/service-requests/add",
    methods=["GET", "POST"]
)
@role_required("customer")
def customer_add_service_request():

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get(
            "priority",
            "Medium"
        )

        if not title or not description:

            flash(
                "Title and description are required.",
                "danger"
            )

            return render_template(
                "service_requests/add.html"
            )

        service_request = ServiceRequest(
            title=title,
            description=description,
            priority=priority,
            status="New",
            customer_id=current_user.id
        )

        db.session.add(service_request)
        db.session.commit()

        flash(
            "Service request submitted successfully!",
            "success"
        )

        return redirect(
            url_for(
                "service_requests.customer_service_requests"
            )
        )

    return render_template(
        "service_requests/add.html"
    )


# =========================================================
# CUSTOMER - VIEW OWN SERVICE REQUESTS
# =========================================================

@service_requests_bp.route(
    "/customer/service-requests"
)
@role_required("customer")
def customer_service_requests():

    service_requests = ServiceRequest.query.filter_by(
        customer_id=current_user.id
    ).order_by(
        ServiceRequest.created_at.desc()
    ).all()

    return render_template(
        "service_requests/list.html",
        service_requests=service_requests,
        page_title="My Service Requests"
    )


# =========================================================
# CUSTOMER - VIEW SINGLE SERVICE REQUEST
# =========================================================

@service_requests_bp.route(
    "/customer/service-requests/<int:request_id>"
)
@role_required("customer")
def customer_view_service_request(request_id):

    service_request = ServiceRequest.query.filter_by(
        id=request_id,
        customer_id=current_user.id
    ).first_or_404()

    return render_template(
        "service_requests/view.html",
        service_request=service_request,
        customer_view=True
    )


# =========================================================
# CUSTOMER - DELETE SERVICE REQUEST
# =========================================================

@service_requests_bp.route(
    "/customer/service-requests/<int:request_id>/delete",
    methods=["POST"]
)
@role_required("customer")
def customer_delete_service_request(request_id):

    # Make sure the request belongs to the
    # currently logged-in customer.
    service_request = ServiceRequest.query.filter_by(
        id=request_id,
        customer_id=current_user.id
    ).first_or_404()

    # Allow deletion only when the request
    # is still New.
    if service_request.status != "New":

        flash(
            "Only new service requests can be deleted.",
            "danger"
        )

        return redirect(
            url_for(
                "service_requests.customer_service_requests"
            )
        )

    db.session.delete(service_request)
    db.session.commit()

    flash(
        "Service request deleted successfully.",
        "success"
    )

    return redirect(
        url_for(
            "service_requests.customer_service_requests"
        )
    )


# =========================================================
# ADMIN - VIEW ALL SERVICE REQUESTS
# =========================================================

@service_requests_bp.route(
    "/admin/service-requests"
)
@role_required("admin")
def admin_service_requests():

    service_requests = ServiceRequest.query.order_by(
        ServiceRequest.created_at.desc()
    ).all()

    return render_template(
        "service_requests/list.html",
        service_requests=service_requests,
        page_title="All Service Requests",
        admin_view=True
    )


# =========================================================
# ADMIN - VIEW SINGLE SERVICE REQUEST
# =========================================================

@service_requests_bp.route(
    "/admin/service-requests/<int:request_id>"
)
@role_required("admin")
def admin_view_service_request(request_id):

    service_request = ServiceRequest.query.get_or_404(
        request_id
    )

    return render_template(
        "service_requests/view.html",
        service_request=service_request,
        admin_view=True
    )


# =========================================================
# ADMIN - ASSIGN SERVICE REQUEST
# =========================================================

@service_requests_bp.route(
    "/admin/service-requests/<int:request_id>/assign",
    methods=["GET", "POST"]
)
@role_required("admin")
def assign_service_request(request_id):

    service_request = ServiceRequest.query.get_or_404(
        request_id
    )

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
                "service_requests/assign.html",
                service_request=service_request,
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
                "service_requests/assign.html",
                service_request=service_request,
                staff_members=staff_members
            )

        service_request.assigned_to = staff.id
        service_request.status = "Assigned"

        db.session.commit()

        flash(
            f"Service request assigned to {staff.name}.",
            "success"
        )

        return redirect(
            url_for(
                "service_requests.admin_service_requests"
            )
        )

    return render_template(
        "service_requests/assign.html",
        service_request=service_request,
        staff_members=staff_members
    )


# =========================================================
# STAFF - VIEW ASSIGNED SERVICE REQUESTS
# =========================================================

@service_requests_bp.route(
    "/staff/service-requests"
)
@role_required("staff")
def staff_service_requests():

    service_requests = ServiceRequest.query.filter_by(
        assigned_to=current_user.id
    ).order_by(
        ServiceRequest.created_at.desc()
    ).all()

    return render_template(
        "service_requests/list.html",
        service_requests=service_requests,
        page_title="Assigned Service Requests",
        staff_view=True
    )


# =========================================================
# STAFF - VIEW SINGLE SERVICE REQUEST
# =========================================================

@service_requests_bp.route(
    "/staff/service-requests/<int:request_id>"
)
@role_required("staff")
def staff_view_service_request(request_id):

    service_request = ServiceRequest.query.filter_by(
        id=request_id,
        assigned_to=current_user.id
    ).first_or_404()

    return render_template(
        "service_requests/view.html",
        service_request=service_request,
        staff_view=True
    )


# =========================================================
# STAFF - UPDATE SERVICE REQUEST
# =========================================================

@service_requests_bp.route(
    "/staff/service-requests/<int:request_id>/update",
    methods=["GET", "POST"]
)
@role_required("staff")
def update_service_request(request_id):

    service_request = ServiceRequest.query.filter_by(
        id=request_id,
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
                    "service_requests.staff_view_service_request",
                    request_id=service_request.id
                )
            )

        if status == "Resolved" and not resolution:

            flash(
                "Please enter the resolution before marking it resolved.",
                "danger"
            )

            return render_template(
                "service_requests/edit.html",
                service_request=service_request,
                staff_view=True
            )

        service_request.status = status
        service_request.resolution = resolution

        db.session.commit()

        flash(
            "Service request updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "service_requests.staff_view_service_request",
                request_id=service_request.id
            )
        )

    return render_template(
        "service_requests/edit.html",
        service_request=service_request,
        staff_view=True
    )