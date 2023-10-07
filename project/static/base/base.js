
document.addEventListener('click', (e)=>{

    let navMenu =  document.getElementById('nav-menu');
    let navFieldToggle = document.getElementById('nav-empty-field-toggle');

    if (e.target.classList[0] === 'btn-dropdown-toggle'){

        if (navMenu.style.display === 'grid') {
            navMenu.style.cssText = 'display: none;';
            // navFieldToggle.style.cssText = 'display: none;';
        }

        else {
            navMenu.style.cssText = 'display: grid;';
            // navFieldToggle.style.cssText = 'display: block;';
        };
    }

    else if (navMenu !== e.target && navMenu !== e.target.offsetParent){
        if (navMenu.style.display === 'grid'){
            navMenu.style.cssText = 'display: none;';
            navFieldToggle.style.cssText = 'display: none;';
        }
    }
});
