// Travel Explorer Interactive Scripts

document.addEventListener('DOMContentLoaded', () => {
    // 1. Auto dismissal of flash alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s ease';
            setTimeout(() => alert.remove(), 500);
        }, 4500);
    });

    // 2. Dynamic price calculation on guest count change
    const guestInput = document.getElementById('guests');
    const pricePerPersonEl = document.getElementById('price-per-person');
    const totalPriceEl = document.getElementById('total-price-display');

    if (guestInput && pricePerPersonEl && totalPriceEl) {
        const unitPrice = parseFloat(pricePerPersonEl.dataset.price || 0);

        function updatePrice() {
            const count = parseInt(guestInput.value) || 1;
            const total = count * unitPrice;
            totalPriceEl.textContent = '₹' + total.toLocaleString('en-IN');
        }

        guestInput.addEventListener('input', updatePrice);
        guestInput.addEventListener('change', updatePrice);
        updatePrice();
    }

    // 3. Interactive Star Rating selector in Review Form
    const starContainer = document.getElementById('star-rating-select');
    if (starContainer) {
        const stars = starContainer.querySelectorAll('span');
        const ratingInput = document.getElementById('rating-value-input');

        stars.forEach((star, index) => {
            star.addEventListener('click', () => {
                const val = index + 1;
                ratingInput.value = val;
                stars.forEach((s, idx) => {
                    s.style.color = idx < val ? '#f59e0b' : '#cbd5e1';
                });
            });
        });
    }
});
