document.addEventListener('DOMContentLoaded', function () {
    const addFormBtn = document.getElementById('add-form');
    const formContainer = document.getElementById('form-container');
    const totalForms = document.getElementById('id_items-TOTAL_FORMS');

    if (addFormBtn && formContainer && totalForms) {
        addFormBtn.addEventListener('click', function (e) {
            e.preventDefault();

            const currentFormCount = parseInt(totalForms.value);
            const emptyFormHtml = formContainer.dataset.emptyForm;
            const newFormHtml = emptyFormHtml.replace(/__prefix__/g, currentFormCount);

            const newFormDiv = document.createElement('div');
            newFormDiv.classList.add('item-form', 'border-b', 'border-gray-200', 'pb-4', 'mb-4');
            newFormDiv.innerHTML = newFormHtml;

            formContainer.appendChild(newFormDiv);
            totalForms.value = currentFormCount + 1;

            attachEvents(newFormDiv);
        });
    }

    function attachEvents(container) {
        const quantityInput = container.querySelector('.quantity-input');
        const priceInput = container.querySelector('.price-input');
        const taxInput = container.querySelector('.tax-input');

        if (quantityInput && priceInput) {
            [quantityInput, priceInput, taxInput].forEach(input => {
                if (input) {
                    input.addEventListener('input', calculateTotal);
                }
            });
        }
    }

    function calculateTotal() {
        // Logic to update totals on client side (optional but good UX)
        // For now, we rely on server-side calculation, but we could add it here.
    }

    // Attach events to existing forms
    document.querySelectorAll('.item-form').forEach(attachEvents);
});
