const counter = function () {
    const btns = document.querySelectorAll('.counter__btn');

    btns.forEach(btn => {
        btn.addEventListener('click', function () {
            const direction = this.dataset.direction;
            const inp = this.parentElement.querySelector('.counter__value');
            const currentValue = +inp.value;
            let newValue;

            if (direction === 'plus') {
                newValue = currentValue + 1 <= 10 ? currentValue + 1 : 10;
            } else if (direction === 'minus-adults') {
                newValue = currentValue - 1 > 0 ? currentValue - 1 : 1;
            } else {
                newValue = currentValue - 1 > 0 ? currentValue - 1 : 0;
            }

            inp.value = newValue;
        })
    })

}

counter();