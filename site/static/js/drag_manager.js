console.log(`Drag'n'Drop`);


function register_drag() {
const tasksListElement = document.querySelector(`.tasks__list`);
const taskElements = tasksListElement.getElementsByClassName(`tasks__item`);

for (const task of taskElements) {
  task.draggable = true;
}

tasksListElement.addEventListener(`dragstart`, (evt) => {
    if(evt.target.classList.contains(`tasks__item`)) {
        evt.target.classList.add(`selected`);
    }
});

tasksListElement.addEventListener(`dragend`, (evt) => {
    if(evt.target.classList.contains(`tasks__item`)) {
        evt.target.classList.remove(`selected`);
    }
});

const getNextElement = (cursorPosition, currentElement) => {
  const currentElementCoord = currentElement.getBoundingClientRect();
  const currentElementCenter = currentElementCoord.y + currentElementCoord.height / 2;
  
  const nextElement = (cursorPosition < currentElementCenter) ?
    currentElement :
    currentElement.nextElementSibling;
  
  return nextElement;
};

tasksListElement.addEventListener(`dragover`, (evt) => {
  evt.preventDefault();

  
  const activeElement = tasksListElement.querySelector(`.selected`);
  const currentElement = evt.target;
  const isMoveable = activeElement !== currentElement &&
    currentElement.classList.contains(`tasks__item`);
    
  if (!isMoveable) {
    return;
  }
  
  const nextElement = getNextElement(evt.clientY, currentElement);
  
  if (
    nextElement && 
    activeElement === nextElement.previousElementSibling ||
    activeElement === nextElement
  ) {
    return;
  }
    try {		
	    tasksListElement.insertBefore(activeElement, nextElement);
    } catch {
        
    }
    });
}

function get_chapter_order() {
    let chapters = document.getElementById('chapters').getElementsByClassName('tasks__item');
    let order = [];
    for(let i = 0; i < chapters.length; i++) {
        order.push(Number(chapters[i].dataset.id));
    }
    return order;
}

function save_chapter_order(order) {
    const formData  = new FormData();
    for(let i = 0; i < order.length; i++) {
        formData.append('chapter', order[i]);
    }
    formData.append('csrfmiddlewaretoken', document.getElementsByName('csrfmiddlewaretoken')[0].value);
    fetch('.', {
        credentials: 'include',
        method: 'POST', // or 'PUT'
        body: formData
    })
    .then(resp=>resp.text())
    .then(text=>console.log(text));
}

function register_save_button() {
    let button = document.getElementById('save_chapter_order');
    if(!button) return;
    button.addEventListener(`click`,() => {
        let order = get_chapter_order();
        save_chapter_order(order);
    });
}

function ready() {
    register_drag();
    register_save_button();
}

document.addEventListener("DOMContentLoaded", ready);
