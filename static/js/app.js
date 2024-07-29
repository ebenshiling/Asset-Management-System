function confirmDelete() {
    if (confirm("Are you sure you want to delete this record?")) {
        document.getElementById('delete-form').submit();
    }
}

// timer for message

var message_timeout = document.getElementById('message-timer');

setTimeout(function() {

    message_timeout.style.display = 'none';
}, 3000)


function uploadExcelFile() {
    var fileInput = document.getElementById('excelFileInput');
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append('excel_file', file);
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    formData.append('csrfmiddlewaretoken', csrfToken);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', uploadUrl, true);
    xhr.onload = function() {
        if (xhr.status === 200) {
            alert('Excel file uploaded successfully!');
        } else {
            alert('Error uploading file.');
        }
    };
    xhr.send(formData);
}