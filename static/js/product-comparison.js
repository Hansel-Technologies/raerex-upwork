function addToCompare(productId, productName) {
    let compareList = JSON.parse(localStorage.getItem('compareList')) || [];
    if (compareList.length >= 3) {
        alert('You can compare up to 3 products. Please remove a product before adding a new one.');
        return;
    }
    if (!compareList.some(item => item.id === productId)) {
        compareList.push({id: productId, name: productName});
        localStorage.setItem('compareList', JSON.stringify(compareList));
        alert(`${productName} has been added to your comparison list.`);
    } else {
        alert('This product is already in your comparison list.');
    }
    updateCompareButton();
}

function updateCompareButton() {
    let compareList = JSON.parse(localStorage.getItem('compareList')) || [];
    let compareButton = document.getElementById('compare-button');
    let compareCount = document.getElementById('compare-count');
    let clearCompareButton = document.getElementById('clear-compare-button');
    let floatingCompareButton = document.getElementById('floating-compare-button');
    
    if (compareButton && compareCount && clearCompareButton && floatingCompareButton) {
        floatingCompareButton.style.display = compareList.length > 0 ? 'flex' : 'none';
        compareCount.textContent = compareList.length;
        clearCompareButton.style.display = compareList.length > 0 ? 'block' : 'none';
    }
}

function clearComparison() {
    localStorage.removeItem('compareList');
    updateCompareButton();
    alert('Comparison list has been cleared.');
}

function goToComparePage() {
    let compareList = JSON.parse(localStorage.getItem('compareList')) || [];
    let productIds = compareList.map(item => item.id).join(',');
    window.location.href = `/compare/?product_id=${productIds}`;
}

function initializeCompareFeature() {
    updateCompareButton();
}

document.addEventListener('DOMContentLoaded', function() {
    initializeCompareFeature();

    // Quantity buttons functionality
    const minusButtons = document.querySelectorAll('.minus');
    const plusButtons = document.querySelectorAll('.plus');

    minusButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentNode.querySelector('input[type="number"]');
            let count = parseInt(input.value) - 1;
            count = count < 1 ? 1 : count;
            input.value = count;
            input.dispatchEvent(new Event('change'));
        });
    });

    plusButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentNode.querySelector('input[type="number"]');
            input.value = parseInt(input.value) + 1;
            input.dispatchEvent(new Event('change'));
        });
    });
});