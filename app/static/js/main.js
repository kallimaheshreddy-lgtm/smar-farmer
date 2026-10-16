// Client-side interactions for Smart Farmer AI

document.addEventListener('DOMContentLoaded', function () {
    // 1. Image Upload Preview
    const imageInput = document.getElementById('plantImageInput');
    const imagePreview = document.getElementById('imagePreview');
    const previewContainer = document.getElementById('previewContainer');

    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                // Check file size (8MB max)
                if (file.size > 8 * 1024 * 1024) {
                    alert('File size exceeds the 8MB limit. Please choose a smaller photo.');
                    imageInput.value = '';
                    if (previewContainer) previewContainer.style.display = 'none';
                    return;
                }
                const reader = new FileReader();
                reader.onload = function (event) {
                    imagePreview.src = event.target.result;
                    if (previewContainer) previewContainer.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // 2. Weather Geolocation Helper
    const geoBtn = document.getElementById('btnGetLocation');
    if (geoBtn) {
        geoBtn.addEventListener('click', function () {
            if (!navigator.geolocation) {
                alert('Geolocation is not supported by your current browser.');
                return;
            }
            geoBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Locating...';
            geoBtn.disabled = true;

            navigator.geolocation.getCurrentPosition(
                function (position) {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    window.location.href = `/weather/?lat=${lat}&lon=${lon}`;
                },
                function (error) {
                    geoBtn.innerHTML = '📍 Use My Exact Location';
                    geoBtn.disabled = false;
                    alert('Location access was denied or unavailable. Please select your district manually from the list.');
                },
                { timeout: 10000 }
            );
        });
    }

    // 3. Animal Triage Danger Sign Visual Alert
    const symptomCheckboxes = document.querySelectorAll('.triage-symptom-check');
    const dangerAlertBox = document.getElementById('liveDangerNotice');

    if (symptomCheckboxes.length > 0 && dangerAlertBox) {
        const dangerKeywords = ['unable to stand', 'downer', 'bloat', 'choking', 'convulsions', 'bleeding', 'foaming'];
        symptomCheckboxes.forEach(cb => {
            cb.addEventListener('change', function () {
                let hasDanger = false;
                symptomCheckboxes.forEach(item => {
                    if (item.checked) {
                        const val = item.value.toLowerCase();
                        if (dangerKeywords.some(kw => val.includes(kw))) {
                            hasDanger = true;
                        }
                    }
                });
                dangerAlertBox.style.display = hasDanger ? 'block' : 'none';
            });
        });
    }
});
