
const dataUrl = document.getElementById('pivot-table-container');

let jsonData = JSON.stringify({
    data: dataUrl.dataset,
});

console.log(jsonData)