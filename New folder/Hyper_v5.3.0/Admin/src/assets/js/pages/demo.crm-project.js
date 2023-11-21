/**
 * Theme: Hyper - Responsive Bootstrap 5 Admin Dashboard
 * Author: Coderthemes
 * Module/App: CRM Project
 */



//
// Campaign Sent Chart

! function ($) {
    "use strict";

    var CrmProject = function () {
        this.$body = $("body"),
            this.charts = []
    };

    CrmProject.prototype.init = function () {
        this.initCharts();
    }

    CrmProject.prototype.initCharts = function () {
        // Project Statistics
        var colors = ["#727cf5", "#0acf97"];
        var dataColors = $("#crm-project-statistics").data('colors');

        if (dataColors) {
            colors = dataColors.split(",");
        }
        var options = {
            chart: {
                height: 326,
                type: 'bar',
                toolbar: {
                    show: false
                }
            },
            plotOptions: {
                bar: {
                    horizontal: false,
                    endingShape: 'rounded',
                    columnWidth: '25%',
                },
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                show: true,
                width: 0,
                colors: ['transparent']
            },
            colors: colors,
            series: [{
                name: 'Projects',
                data: [56, 38, 85, 72, 28, 69, 55, 52, 69]
            }, {
                name: 'Working Hours',
                data: [176, 185, 256, 240, 187, 205, 191, 114, 194]
            }],
            xaxis: {
                categories: ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
            },
            legend: {
                offsetY: 7,
            },
            fill: {
                opacity: 1

            },
            // legend: {
            //     floating: true
            // },
            grid: {
                row: {
                    colors: ['transparent', 'transparent'], // takes an array which will be repeated on columns
                    opacity: 0.2
                },
                borderColor: '#f1f3fa',
                padding: {
                    bottom: 5
                }
            }
        }

        var chart = new ApexCharts(
            document.querySelector("#crm-project-statistics"),
            options
        );

        chart.render();


        // Monthly Target

        var colors = ["#727cf5", "#0acf97"];
        var dataColors = $("#monthly-target").data('colors');
        if (dataColors) {
            colors = dataColors.split(",");
        }
        var options = {
            chart: {
                height: 256,
                type: 'donut',
            },
            legend: {
                show: false
            },
            stroke: {
                width: 0,
                colors: ['transparent']
            },
            series: [82, 37],
            labels: ["Done Projects", "Pending Projects"],
            colors: colors,
            responsive: [{
                breakpoint: 480,
                options: {
                    chart: {
                        width: 200
                    },
                    legend: {
                        position: 'bottom'
                    }
                }
            }]
        }

        var chart = new ApexCharts(
            document.querySelector("#monthly-target"),
            options
        );

        chart.render();
    },
        //init flotchart
        $.CrmProject = new CrmProject, $.CrmProject.Constructor = CrmProject
}(window.jQuery),

    //initializing CrmProject
    function ($) {
        "use strict";
        $(document).ready(function (e) {
            $.CrmProject.init();
        });
    }(window.jQuery);



//
// project-overview CHART
//
var colors = ["#727cf5", "#0acf97", "#fa5c7c", "#ffbc00"];
var dataColors = $("#project-overview-chart").data('colors');
if (dataColors) {
    colors = dataColors.split(",");
}
var options = {
    chart: {
        height: 326,
        type: 'radialBar'
    },
    colors: colors,
    series: [85, 70, 80, 65],
    labels: ['Product Design', 'Web Development', 'Illustration Design', 'UI/UX Design'],
    plotOptions: {
        radialBar: {
            track: {
                margin: 5,
            }
        }
    }
}

var chart = new ApexCharts(
    document.querySelector("#project-overview-chart"),
    options
);

chart.render();
