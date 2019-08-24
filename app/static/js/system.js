var memChart;
var cpuChart;
var gpuChart;

var initSystem = function (memStats, cpuStats, gpuStats) {
    memChartNode = document.getElementById('mem-chart');
    createMemChart(memChartNode, memStats);

    cpuChartNode = document.getElementById('cpu-chart');
    createCpuChart(cpuChartNode, cpuStats);

    gpuChartNode = document.getElementById('gpu-chart');
    createGpuChart(gpuChartNode, gpuStats);

    setInterval(updateSystem, 1000);
};

var createMemChart = function (node, memStats) {
    chartData = buildMemChartData(memStats);

    memChart = new Chart(node, {
        type: 'line',
        data: chartData,
        options: {
            legend: {
                display: true
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    display: false,
                }],
                yAxes: [{
                    display: true,
                    gridLines: {
                        display: false
                    },
                    ticks: {
                        suggestedMax: 100,    // minimum will be 100, unless there is a higher value.
                        suggestedMin: 0,    // minimum will be 0, unless there is a lower value.
                        // OR //
                        beginAtZero: true   // minimum value will be 0.
                    }
                }, {
                    display: true,
                    position: 'right',
                    scaleLabel: {
                        display: true,
                        labelString: 'GBs'
                    },
                    gridLines: {
                        display: false
                    },
                    ticks: {
                        suggestedMax: 8,    // minimum will be 100, unless there is a higher value.
                        suggestedMin: 0,    // minimum will be 0, unless there is a lower value.
                        // OR //
                        beginAtZero: true   // minimum value will be 0.
                    }
                }]
            }
        }
    });
};

var buildMemChartData = function (memStats) {
    return {
        labels: memStats.map(function (d) {
            return moment(d[0]);
        }),

        datasets: [{
            label: 'RAM',
            data: memStats.map(function (d) {
                return d[1];
            }),
            backgroundColor: 'rgb(254, 212, 0)',
            fill: true,
            borderColor: 'rgb(254, 212, 0)'
        }]
    };
};

var createCpuChart = function (node, cpuStats) {
    chartData = buildCpuChartData(cpuStats);

    cpuChart = new Chart(node, {
        type: 'line',
        data: chartData,
        options: {
            legend: {
                display: true
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    display: false
                }],
                yAxes: [{
                    display: true,
                    gridLines: {
                        display: false
                    },
                    ticks: {
                        suggestedMax: 100,    // minimum will be 100, unless there is a higher value.
                        suggestedMin: 0,    // minimum will be 0, unless there is a lower value.
                        // OR //
                        beginAtZero: true   // minimum value will be 0.
                    }
                }]
            }
        }
    });
};

var buildCpuChartData = function (cpuStats) {
    return {
        labels: cpuStats.map(function (d) {
            return moment(d[0]);
        }),

        datasets: [
            {
                label: 'CPU1',
                data: cpuStats.map(function (d) {
                    return d[1];
                }),
                backgroundColor: 'rgb(255,99,71)',
                fill: false,
                borderColor: 'rgb(255,99,71)'
            },
            {
                label: 'CPU2',
                data: cpuStats.map(function (d) {
                    return d[2];
                }),
                backgroundColor: 'rgb(129,199,132)',
                fill: false,
                borderColor: 'rgb(129,199,132)'
            },
            {
                label: 'CPU3',
                data: cpuStats.map(function (d) {
                    return d[3];
                }),
                backgroundColor: 'rgb(255, 144, 0)',
                fill: false,
                borderColor: 'rgb(255, 144, 0)'
            },

            {
                label: 'CPU4',
                data: cpuStats.map(function (d) {
                    return d[4];
                }),
                backgroundColor: 'rgb(103,58,183)',
                fill: false,
                borderColor: 'rgb(103,58,183)'
            },
            {
                label: 'CPU5',
                data: cpuStats.map(function (d) {
                    return d[5];
                }),
                backgroundColor: 'rgb(83,109,254)',
                fill: false,
                borderColor: 'rgb(83,109,254)'
            },
            {
                label: 'CPU6',
                data: cpuStats.map(function (d) {
                    return d[6];
                }),
                backgroundColor: 'rgb(254, 212, 0)',
                fill: false,
                borderColor: 'rgb(254, 212, 0)'
            },

        ]
    };
};

var createGpuChart = function (node, gpuStats) {
    chartData = buildGpuChartData(gpuStats);

    gpuChart = new Chart(node, {
        type: 'line',
        data: chartData,
        options: {
            legend: {
                display: true
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    display: false
                }],
                yAxes: [{
                    display: true,
                    gridLines: {
                        display: false
                    },
                    ticks: {
                        suggestedMax: 100,    // minimum will be 100, unless there is a higher value.
                        suggestedMin: 0,    // minimum will be 0, unless there is a lower value.
                        // OR //
                        beginAtZero: true   // minimum value will be 0.
                    }
                }]
            }
        }
    });
};

var buildGpuChartData = function (gpuStats) {
    return {
        labels: gpuStats.map(function (d) {
            return moment(d[0]);
        }),

        datasets: [{
            label: 'GPU',
            data: gpuStats.map(function (d) {
                return d[1];
            }),
            backgroundColor: 'rgb(154,205,50)',
            fill: true,
            borderColor: 'rgb(154,205,50)',
            suggestedMax: 100,    // minimum will be 100, unless there is a higher value.
            suggestedMin: 0,    // minimum will be 0, unless there is a lower value.
        }]
    };
};

var updateSystem = function () {
    $.ajax({
        method: 'GET',
        url: '/system.json',
        success: function (response) {
            memData = buildMemChartData(response.memStats);
            memChart.data = memData;
            memChart.update(0);

            cpuData = buildCpuChartData(response.cpuStats);
            cpuChart.data = cpuData;
            cpuChart.update(0);

            gpuData = buildGpuChartData(response.gpuStats);
            gpuChart.data = gpuData;
            gpuChart.update(0);

            document.getElementById('uptime-para').innerText = response.uptime;
            document.getElementById('boot_time-para').innerText = response.boot_time;

            document.getElementById('model-name-text').innerText = response.model_name;
            document.getElementById('images-stored-text').innerText = response.number_of_images;
            document.getElementById('objects-stored-text').innerText = response.number_of_distinct_objects;
        }
    });
};

function isEmpty(obj) {
    for (var key in obj) {
        if (obj.hasOwnProperty(key))
            return false;
    }
    return true;
}