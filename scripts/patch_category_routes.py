from pathlib import Path

path = Path(r'd:/kitetsu/Planora/app/routes/category_routes.py')
text = path.read_text(encoding='utf-8')

if 'def update_category' in text:
    print('update_category route already exists.')
else:
    marker = "@bp.route('/<category_id>', methods=['DELETE'])"
    idx = text.find(marker)
    if idx == -1:
        raise SystemExit('Could not find delete route marker')

    # Find end of delete_category function (first empty line after return)
    after = text.find('\n\n', idx)
    if after == -1:
        after = len(text)

    insert_pos = after
    new_block = "\n@bp.route('/<category_id>', methods=['PUT'])\n@jwt_required\ndef update_category(category_id):\n    try:\n        data = request.get_json()\n        result, status_code = CategoryService.update_category(\n            g.current_user.id,\n            category_id,\n            data\n        )\n        return jsonify(result), status_code\n    except Exception as e:\n        return jsonify({'error': str(e)}), 422\n"
    text = text[:insert_pos] + new_block + text[insert_pos:]
    path.write_text(text, encoding='utf-8')
    print('Inserted update_category route.')
