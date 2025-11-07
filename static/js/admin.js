// Admin panel JavaScript

// Sidebar toggle for mobile
const sidebarToggle = document.getElementById('sidebarToggle');
const adminSidebar = document.querySelector('.admin-sidebar');

sidebarToggle?.addEventListener('click', () => {
    adminSidebar.classList.toggle('open');
});

// Close sidebar on outside click (mobile)
document.addEventListener('click', (e) => {
    if (window.innerWidth <= 968) {
        if (!adminSidebar?.contains(e.target) && !sidebarToggle?.contains(e.target)) {
            adminSidebar?.classList.remove('open');
        }
    }
});

// Confirm delete
function confirmDelete(id) {
    if (confirm('Are you sure you want to delete this property? This action cannot be undone.')) {
        document.getElementById(`delete-form-${id}`)?.submit();
    }
}

// Image preview on file select
const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');

imageInputs.forEach(input => {
    input.addEventListener('change', function(e) {
        const files = e.target.files;
        const previewContainer = document.getElementById('imagePreview');
        
        if (previewContainer) {
            previewContainer.innerHTML = '';
            
            Array.from(files).forEach((file, index) => {
                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    
                    reader.onload = function(e) {
                        const preview = document.createElement('div');
                        preview.className = 'image-preview-item';
                        preview.innerHTML = `
                            <img src="${e.target.result}" alt="Preview ${index + 1}">
                            <button type="button" class="remove-preview" onclick="removePreview(this)">
                                <i class="fas fa-times"></i>
                            </button>
                        `;
                        previewContainer.appendChild(preview);
                    };
                    
                    reader.readAsDataURL(file);
                }
            });
        }
    });
});

// Remove image preview
function removePreview(button) {
    button.parentElement.remove();
}

// Delete image via AJAX
async function deleteImage(imageId) {
    if (!confirm('Are you sure you want to delete this image?')) {
        return;
    }
    
    try {
        const response = await fetch(`/admin/image/delete/${imageId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            location.reload();
        } else {
            alert('Error deleting image');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error deleting image');
    }
}

// Form validation
const propertyForms = document.querySelectorAll('.property-form');

propertyForms.forEach(form => {
    form.addEventListener('submit', function(e) {
        const title = form.querySelector('[name="title"]');
        const description = form.querySelector('[name="description"]');
        const price = form.querySelector('[name="price"]');
        const area = form.querySelector('[name="area"]');
        
        let isValid = true;
        let errors = [];
        
        if (title && title.value.trim().length < 5) {
            errors.push('Title must be at least 5 characters long');
            isValid = false;
        }
        
        if (description && description.value.trim().length < 20) {
            errors.push('Description must be at least 20 characters long');
            isValid = false;
        }
        
        if (price && parseFloat(price.value) <= 0) {
            errors.push('Price must be greater than 0');
            isValid = false;
        }
        
        if (area && parseFloat(area.value) <= 0) {
            errors.push('Area must be greater than 0');
            isValid = false;
        }
        
        if (!isValid) {
            e.preventDefault();
            alert('Please fix the following errors:\n\n' + errors.join('\n'));
        }
    });
});

// Auto-save draft (optional)
let autoSaveTimer;

function autoSaveDraft() {
    clearTimeout(autoSaveTimer);
    
    autoSaveTimer = setTimeout(() => {
        const formData = new FormData(document.querySelector('.property-form'));
        localStorage.setItem('propertyDraft', JSON.stringify(Object.fromEntries(formData)));
        console.log('Draft saved');
    }, 2000);
}

// Load draft on page load
window.addEventListener('DOMContentLoaded', () => {
    const draft = localStorage.getItem('propertyDraft');
    if (draft && confirm('Load saved draft?')) {
        const data = JSON.parse(draft);
        Object.keys(data).forEach(key => {
            const field = document.querySelector(`[name="${key}"]`);
            if (field) {
                field.value = data[key];
            }
        });
    }
});

// Clear draft after successful submission
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('submit', () => {
        localStorage.removeItem('propertyDraft');
    });
});

// Table sorting
const tableHeaders = document.querySelectorAll('.admin-table th');

tableHeaders.forEach((header, index) => {
    header.style.cursor = 'pointer';
    header.addEventListener('click', () => {
        sortTable(index);
    });
});

function sortTable(columnIndex) {
    const table = document.querySelector('.admin-table tbody');
    const rows = Array.from(table.querySelectorAll('tr'));
    
    rows.sort((a, b) => {
        const aText = a.cells[columnIndex].textContent.trim();
        const bText = b.cells[columnIndex].textContent.trim();
        return aText.localeCompare(bText);
    });
    
    rows.forEach(row => table.appendChild(row));
}

// Bulk actions (optional)
const selectAllCheckbox = document.getElementById('selectAll');
const rowCheckboxes = document.querySelectorAll('.row-checkbox');

selectAllCheckbox?.addEventListener('change', function() {
    rowCheckboxes.forEach(checkbox => {
        checkbox.checked = this.checked;
    });
    updateBulkActions();
});

rowCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', updateBulkActions);
});

function updateBulkActions() {
    const checkedCount = document.querySelectorAll('.row-checkbox:checked').length;
    const bulkActions = document.getElementById('bulkActions');
    
    if (bulkActions) {
        bulkActions.style.display = checkedCount > 0 ? 'block' : 'none';
        bulkActions.querySelector('.count')?.textContent = checkedCount;
    }
}

// Stats animation
function animateStats() {
    const statNumbers = document.querySelectorAll('.stat-details h3');
    
    statNumbers.forEach(stat => {
        const target = parseInt(stat.textContent);
        let current = 0;
        const increment = target / 50;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                stat.textContent = target;
                clearInterval(timer);
            } else {
                stat.textContent = Math.floor(current);
            }
        }, 20);
    });
}

// Run stats animation on page load
if (document.querySelector('.stat-details')) {
    animateStats();
}

// Chart.js integration (if you want to add charts)
// Uncomment and include Chart.js library
/*
const ctx = document.getElementById('salesChart');
if (ctx) {
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Properties Sold',
                data: [12, 19, 3, 5, 2, 3],
                borderColor: '#e74c3c',
                tension: 0.1
            }]
        }
    });
}
*/