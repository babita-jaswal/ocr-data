from flask import Blueprint, request, jsonify, make_response
from functools import wraps
from .database import fetch_all_data, fetch_paginated_data, fetch_applicant_by_id
from .auth import require_auth

main_bp = Blueprint('main', __name__)

@main_bp.route('/api/applicant', methods=['GET'])
@require_auth
def get_all_data():
    data = fetch_all_data()
    if not data:
        return jsonify({"error": "No data found"}), 404
    return jsonify(data)

@main_bp.route('/api/applicant/page', methods=['GET'])
@require_auth
def get_paginated_data():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    data = fetch_paginated_data(page, per_page)
    if not data:
        return jsonify({"error": "No data found"}), 404

    total_items = len(fetch_all_data())
    total_pages = (total_items + per_page - 1) // per_page

    return jsonify({
        "data": data,
        "total": total_items,
        "pages": total_pages,
        "current_page": page
    })

@main_bp.route('/api/applicant/<int:doc_id>', methods=['GET'])
@require_auth
def get_applicant(doc_id):
    applicant_data = fetch_applicant_by_id(doc_id)
    if applicant_data:
        return jsonify(applicant_data), 200
    else:
        return jsonify({"error": f"No applicant found with ID {doc_id}"}), 404
