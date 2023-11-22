

const refreshBtn = document.getElementById('refreshBtn');
const socket = new WebSocket(`ws://${window.location.host}/ws/dashboard/users/`);
console.log('DJAJ-')
socket.onmessage = function(e) {

    console.log(`Server: ${e.data}`);
    const {sender, message} = JSON.parse(e.data)
}

socket.onopen = function(e) {
    socket.send(JSON.stringify({
        'message': 'Hello Users',
        'sender': 'CustomUser',
        })
    );
}

refreshBtn.addEventListener('click', ()=> {
    updateChart()
})


const fetchCharData = async() => {
    const response = await fetch(`${window.location.href}chart/`);
    const data = await response.json()
    return data
}


const statusCtx = document.getElementById('statusChart');
let statusChart;
const drawStatusChart = async() => {

    const data = await fetchCharData()
    const {statusChartLabels, statusChartData} = data

    statusChart = new Chart(statusCtx, {
        type: 'pie',
        data: {
            labels: statusChartLabels,
            datasets: [{
                    label: '% of contribution',
                    data: statusChartData,
                    borderWidth: 1
                }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero:true
                }
            }
        }
    })
}

const rolesCtx = document.getElementById('rolesChart');
let rolesChart;
const drawRolesChart = async() => {

    const data = await fetchCharData()
    const {rolesChartLabels, rolesChartData} = data

    rolesChart = new Chart(rolesCtx, {
        type: 'doughnut',
        data: {
            labels: rolesChartLabels,
            datasets: [{
                    label: '% of contribution',
                    data: rolesChartData,
                    borderWidth: 1
                }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero:true
                }
            }
        }
    })

    // rolesChart = new Chart(rolesCtx, {
    //     type: 'line',
    //     data: {
    //       datasets: [{
    //         data: [{x: '2016-12-25', y: 20}, {x: '2016-12-26', y: 10}]
    //       }]
    //     }
    // })


}

const updateChart = async() => {
    if (statusChart){
        statusChart.destroy()
    }if (rolesChart){
        rolesChart.destroy()
    }
    await drawStatusChart(), drawRolesChart()
}

drawStatusChart()
drawRolesChart()