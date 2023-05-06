const veg=document.getElementById('veg');
const nonveg=document.getElementById('nonveg');


veg.addEventListener('change', () => {
    if (veg.checked) {
      nonveg.checked = false;
    }
  });
  
  nonveg.addEventListener('change', () => {
    if (nonveg.checked) {
      veg.checked = false;
    }
  });


  function clearOtherCheckbox(checkbox, otherCheckboxId) {
    if (checkbox.checked) {
      document.getElementById(otherCheckboxId).checked = false;
    }
  }
  

const counterValue = document.querySelector('.counter-value');
const minusBtn = document.querySelector('.minus');
const plusBtn = document.querySelector('.plus');

let count = 0;

minusBtn.addEventListener('click', () => {
    if(count > 0 ){
        count--;
    }
  
  updateCounter();
});

plusBtn.addEventListener('click', () => {
  count++;
  updateCounter();
});

function updateCounter() {
  counterValue.textContent = count;
}


const counterValue1 = document.querySelector('.counter-value1');
const minusBtn1 = document.querySelector('.minus1');
const plusBtn1 = document.querySelector('.plus1');

let count1 = 0;

minusBtn1.addEventListener('click', () => {
    if(count1 > 0 ){
        count1--;
    }
  
  updateCounter1();
});

plusBtn1.addEventListener('click', () => {
  count1++;
  updateCounter1();
});

function updateCounter1() {
  counterValue1.textContent = count1;
}





