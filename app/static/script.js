// static/script.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const fileInput = document.getElementById('file-input');
        if (!fileInput.files.length) {
            resultDiv.innerHTML = '<div class="error">Пожалуйста, выберите файл.</div>';
            return;
        }

        const formData = new FormData(form);
        resultDiv.innerHTML = 'Загрузка и обработка...';

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultDiv.innerHTML = `<div class="error">${data.error}</div>`;
            } else if (data.html) {
                resultDiv.innerHTML = data.html;
                // Автоматическая привязка кнопки печати (она уже есть в HTML)
            } else {
                resultDiv.innerHTML = '<div class="error">Неизвестная ошибка</div>';
            }
        })
        .catch(error => {
            resultDiv.innerHTML = `<div class="error">Ошибка соединения: ${error.message}</div>`;
        });
    });
});