// Upload page specific functionality
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('input[type="file"]');
    const uploadArea = document.querySelector('.upload-area');
    const filePreview = document.querySelector('.file-upload-preview');
    const submitBtn = document.querySelector('button[type="submit"]');

    if (!fileInput || !uploadArea) return;

    // File upload handling
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop handling
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleFileDrop);

    function handleFileSelect(e) {
        const file = e.target.files;
        if (file) {
            updateUploadArea(file);
            showFilePreview(file);
        }
    }

    function handleDragOver(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    }

    function handleDragLeave(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    }

    function handleFileDrop(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            updateUploadArea(files);
            showFilePreview(files);
        }
    }

    function updateUploadArea(file) {
        const icon = uploadArea.querySelector('i');
        const text = uploadArea.querySelector('p');
        
        if (icon) icon.className = 'bi bi-check-circle display-4 text-success mb-3';
        if (text) text.innerHTML = `<strong>${file.name}</strong><br><small class="text-muted">${formatFileSize(file.size)}</small>`;
        
        uploadArea.style.borderColor = '#28a745';
        uploadArea.style.backgroundColor = '#121820';
    }

    function showFilePreview(file) {
        if (filePreview) {
            const fileName = filePreview.querySelector('.file-name');
            const fileSize = filePreview.querySelector('.file-size');
            
            if (fileName) fileName.textContent = file.name;
            if (fileSize) fileSize.textContent = formatFileSize(file.size);
            
            filePreview.classList.add('show');
        }
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Form submission with loading state
    if (submitBtn) {
        const form = submitBtn.closest('form');
        form.addEventListener('submit', function() {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="loading-spinner me-2"></span>Processing...';
        });
    }
});
