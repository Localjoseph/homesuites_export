// Main JS file for HomeSuites Rental App

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Property Search Form Date Validation
    const checkInField = document.getElementById('check_in');
    const checkOutField = document.getElementById('check_out');
    
    if (checkInField && checkOutField) {
        // Set minimum date for check-in to today
        const today = new Date().toISOString().split('T')[0];
        checkInField.setAttribute('min', today);
        
        checkInField.addEventListener('change', function() {
            // Set minimum date for check-out to check-in date
            if (checkInField.value) {
                checkOutField.setAttribute('min', checkInField.value);
                
                // If check-out date is before check-in date, reset it
                if (checkOutField.value && checkOutField.value < checkInField.value) {
                    checkOutField.value = checkInField.value;
                }
            }
        });
    }

    // Property Price Range Calculation
    const calculatePrice = function() {
        const checkIn = document.getElementById('check_in');
        const checkOut = document.getElementById('check_out');
        const pricePerNight = document.getElementById('price_per_night');
        const totalPrice = document.getElementById('total_price');
        
        if (checkIn && checkOut && pricePerNight && totalPrice) {
            if (checkIn.value && checkOut.value) {
                const date1 = new Date(checkIn.value);
                const date2 = new Date(checkOut.value);
                const diffTime = Math.abs(date2 - date1);
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                
                if (diffDays > 0) {
                    const price = parseFloat(pricePerNight.dataset.price);
                    const total = price * diffDays;
                    totalPrice.textContent = `$${total.toFixed(2)}`;
                    document.getElementById('price_calculation').style.display = 'block';
                }
            }
        }
    };
    
    // Add event listeners for price calculation
    const checkInDateInput = document.getElementById('check_in');
    const checkOutDateInput = document.getElementById('check_out');
    
    if (checkInDateInput && checkOutDateInput) {
        checkInDateInput.addEventListener('change', calculatePrice);
        checkOutDateInput.addEventListener('change', calculatePrice);
    }

    // Booking confirmation modal
    const bookingModal = document.getElementById('bookingConfirmModal');
    if (bookingModal) {
        const modal = new bootstrap.Modal(bookingModal);
        
        document.getElementById('confirmBookingBtn').addEventListener('click', function(e) {
            e.preventDefault();
            modal.show();
        });
        
        document.getElementById('proceedBookingBtn').addEventListener('click', function() {
            document.getElementById('bookingForm').submit();
        });
    }

    // Image preview for property creation/update
    const propertyImageInput = document.querySelector('input[name="images"]');
    const previewContainer = document.getElementById('image-previews');
    
    if (propertyImageInput && previewContainer) {
        propertyImageInput.addEventListener('change', function() {
            previewContainer.innerHTML = '';
            
            if (this.files) {
                Array.from(this.files).forEach(file => {
                    if (file.type.match('image.*')) {
                        const reader = new FileReader();
                        
                        reader.onload = function(e) {
                            const preview = document.createElement('div');
                            preview.className = 'col-md-3 mb-3';
                            preview.innerHTML = `
                                <div class="card">
                                    <img src="${e.target.result}" class="card-img-top" alt="Preview" style="height: 150px; object-fit: cover;">
                                </div>
                            `;
                            previewContainer.appendChild(preview);
                        }
                        
                        reader.readAsDataURL(file);
                    }
                });
            }
        });
    }

    // Confirmation for property deletion
    const deleteForm = document.getElementById('delete-property-form');
    if (deleteForm) {
        deleteForm.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to delete this property? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    }

    // Confirmation for booking cancellation
    const cancelBookingBtn = document.querySelector('.cancel-booking-btn');
    if (cancelBookingBtn) {
        cancelBookingBtn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to cancel this booking?')) {
                e.preventDefault();
            }
        });
    }
});
