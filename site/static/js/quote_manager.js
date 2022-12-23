function ready() {
    let button = document.getElementById('quote_modal_form');
    button.addEventListener('click', ()=>{
        let text = document.getSelection().toString();
        let hidden = document.getElementById('hidden_quote');
        let nohidden = document.getElementById('nohidden_quote');
        hidden.value = text;
        nohidden.innerText = text;
    });
}

document.addEventListener("DOMContentLoaded", ready);
