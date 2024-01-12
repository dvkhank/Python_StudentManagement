document.addEventListener("DOMContentLoaded", function () {
    var checkboxes = document.querySelectorAll('.fee-checkbox');
    var totalAmountInput = document.getElementById('totalAmount');

    checkboxes.forEach(function (checkbox) {
        if (checkbox.name === 'selected_fees[]') {
            console.log('Checkbox name is correct');
        } else {
            console.log('Checkbox name is incorrect');
        }

        checkbox.addEventListener('change', updateTotalAmount);
    });

    updateTotalAmount();

    function updateTotalAmount() {
        var totalAmount = 0;

        checkboxes.forEach(function (checkbox) {
            if (checkbox.checked) {
                var feeAmount = parseFloat(checkbox.parentNode.nextElementSibling.nextElementSibling.textContent);
                if (!isNaN(feeAmount)) {
                    totalAmount += feeAmount;
                }
            }
        });

        // Chuyển đổi totalAmount sang số nguyên
        totalAmountInput.value = parseInt(totalAmount);
    }
});

function getSelectedFees() {
    var checkboxes = document.querySelectorAll('input[name="selected_fees[]"]:checked');
    var selectedFeeIds = Array.from(checkboxes).map(function (checkbox) {
        return checkbox.value;
    });

    if (selectedFeeIds.length > 0) {
        window.location.href = 'payment?selected_fee_ids=' + selectedFeeIds.join(',');
    } else {
        alert('Please select at least one fee to pay.');
    }
}

function getSelectedFees() {
    var checkboxes = document.querySelectorAll('input[name="selected_fees[]"]:checked');
    var selectedFeeIds = Array.from(checkboxes).map(function (checkbox) {
        return checkbox.value;
    });

    if (selectedFeeIds.length > 0) {
        window.location.href = 'payment?selected_fee_ids=' + selectedFeeIds.join(',');
    } else {
        alert('Please select at least one fee to pay.');
    }
}
