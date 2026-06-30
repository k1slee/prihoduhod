# routes/main.py
import io
import logging
from flask import Blueprint, request, jsonify, render_template
from services.excel_parser import parse_excel
from services.calendar_builder import build_calendar
from services.html_generator import generate_calendar_html

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/upload', methods=['POST'])
def upload():
    """
    Обработка загруженного файла
    """
    if 'file' not in request.files:
        return jsonify({'error': 'Файл не выбран'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Файл не выбран'}), 400

    if not file.filename.lower().endswith(('.xlsx', '.xls')):
        return jsonify({'error': 'Пожалуйста, загрузите файл .xlsx или .xls'}), 400

    try:
        file_stream = io.BytesIO(file.read())   # исправлено: file.read()
        parsed = parse_excel(file_stream)
        calendar_data = build_calendar(
            parsed['dates'],
            parsed['times'],
            parsed['employee_name']
        )

        html = generate_calendar_html(calendar_data)
        return jsonify({'html': html})

    except ValueError as e:
        logging.error(f"Ошибка формата: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logging.error(f"Внутренняя ошибка: {str(e)}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500