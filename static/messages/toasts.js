
const toastTemplate = document.querySelector('[data-toast-template]')
const toastContainer = document.querySelector('[data-toast-container]')
const closeMsgBtn = document.querySelectorAll('.close-msg-btn')



function createToast(message){

    const element = toastTemplate.cloneNode(true)
    delete element.dataset.toastTemplate
    toastContainer.appendChild(element)
    element.className += ` ${ message.tags }`
    element.querySelector('[data-toast-body]').innerText = message.message
    setTimeout(dismissMsg, 2000, element);
}

function dismissMsg (elt){
    $(elt).fadeOut(300, function() {
        $(this).remove();
    })
}


htmx.on("messages", (e)=> {
    e.detail.value.forEach(createToast)
})

const toastElements = document.querySelectorAll(
    '.toast:not([data-toast-template])'
)

for (const element of toastElements){
    const toast = new bootstrap.Toast(element, {delay:2000})

    toast.dispose()
}

document.addEventListener('click', (e)=>{

    if(e.target.hasAttribute('close-msg-btn')){
        e.target.parentElement.remove()
    }
})
