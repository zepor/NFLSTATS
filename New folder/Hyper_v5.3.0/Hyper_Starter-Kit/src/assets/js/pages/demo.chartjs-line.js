/**
 * Theme: Hyper - Responsive Bootstrap 5 Admin Dashboard
 * Author: Coderthemes
 * Module/App: Chartjs
 */

!function ($) {
    "use strict";

    var LineChart = function () {
        this.$body = $("body");
        this.charts = [];

        this.defaultColors = ["#727cf5", "#0acf97", "#fa5c7c", "#ffbc00"];


    };

    LineChart.prototype.interpolationExample = function () {
        var chartElement = document.getElementById('interpolation-example');
        var dataColors = chartElement.getAttribute('data-colors');
        var colors = dataColors ? dataColors.split(",") : this.defaultColors;
        var ctx = chartElement.getContext('2d');
        var datapoints = [0, 20, 20, 60, 60, 120, NaN, 180, 120, 125, 105, 110, 170];

        var chart = new Chart(ctx, {
            type: 'line', data: {
                labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'], datasets: [{
                    label: 'Fully Rounded',
                    data: datapoints,
                    borderColor: colors[0],
                    fill: false,
                    cubicInterpolationMode: 'monotone',
                    tension: 0.4
                }, {
                    label: 'Small Radius', data: datapoints, borderColor: colors[1], fill: false, tension: 0.4
                }, {
                    label: 'Small Radius', data: datapoints, borderColor: colors[2], fill: false,
                },]
            }, options: {
                responsive: true, maintainAspectRatio: false, interaction: {
                    intersect: false,
                }, plugins: {
                    legend: {
                        display: false,

                        position: 'top',
                    },

                }, scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    }, y: {
                        grid: {
                            display: false
                        }, suggestedMin: -10, suggestedMax: 200
                    },
                }
            },
        });

        this.charts.push(chart);
    }


    LineChart.prototype.lineExample = function () {
        var chartElement = document.getElementById('line-example');
        var dataColors = chartElement.getAttribute('data-colors');
        var colors = dataColors ? dataColors.split(",") : this.defaultColors
        var ctx = chartElement.getContext('2d');
        var chart = new Chart(ctx, {
            type: 'line', data: {
                labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], datasets: [{
                    label: 'Fully Rounded',
                    data: [32, 42, 42, 62, 52, 75, 62],
                    borderColor: colors[0],
                    fill: true,
                    backgroundColor: hexToRGB(colors[0], 0.3),

                }, {
                    label: 'Small Radius',
                    data: [42, 58, 66, 93, 82, 105, 92],
                    fill: true,
                    backgroundColor: 'transparent',
                    borderColor: colors[1],
                    borderDash: [5, 5],
                }]
            }, options: {
                responsive: true, maintainAspectRatio: false,

                plugins: {
                    legend: {
                        display: false,

                        position: 'top',
                    },

                }, tension: 0.3, scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    }, y: {
                        grid: {
                            display: false
                        }
                    },
                }
            },
        });

        this.charts.push(chart)
    }

    LineChart.prototype.multiAxesExample = function () {
        var chartElement = document.getElementById('multi-axes-example');
        var dataColors = chartElement.getAttribute('data-colors');
        var colors = dataColors ? dataColors.split(",") : this.defaultColors
        var ctx = chartElement.getContext('2d');
        var chart = new Chart(ctx, {
            type: 'line', data: {
                labels: ['Jan', 'Feb', 'March', 'April', "May", "June", "July"], datasets: [{
                    label: 'Fully Rounded',
                    data: [12, -19, 14, -15, 18, -14, -7],
                    borderColor: colors[0],
                    backgroundColor: hexToRGB(colors[0], 0.3),
                    borderWidth: 1.5,
                    yAxisID: 'y',

                }, {
                    label: 'Small Radius',
                    data: [-10, 19, -15, -8, -17, 12, 8],
                    backgroundColor: hexToRGB(colors[1], 0.3),
                    borderColor: colors[1],
                    borderWidth: 1.5,
                    yAxisID: 'y1',

                }]
            }, options: {
                interaction: {
                    mode: 'index', intersect: false,
                }, responsive: true, maintainAspectRatio: false, plugins: {
                    legend: {
                        display: false,

                        position: 'top',
                    },

                }, tension: 0.2, scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    }, y: {
                        type: 'linear', display: true, position: 'left', grid: {
                            display: false
                        }
                    }, y1: {
                        type: 'linear', display: true, position: 'right', grid: {
                            drawOnChartArea: false, // only want the grid lines for one axis to show up
                        },
                    },
                }
            },
        });
        this.charts.push(chart)

    }

    LineChart.prototype.pointStylingExample = function () {
        var chartElement = document.getElementById('point-styling-example');
        var dataColors = chartElement.getAttribute('data-colors');
        var colors = dataColors ? dataColors.split(",") : this.defaultColors
        var ctx = chartElement.getContext('2d');
        var chart = new Chart(ctx, {
            type: 'line', data: {
                labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6'], datasets: [{
                    label: 'Dataset 1',
                    data: [12, -19, 14, -15, 14, -8],
                    borderColor: colors[0],
                    pointStyle: 'circle',
                    pointRadius: 10,
                    pointHoverRadius: 15
                },]
            }, options: {
                responsive: true, maintainAspectRatio: false, plugins: {
                    legend: {
                        display: false,
                    },

                }, scales: {
                    x: {
                        stacked: true,

                        grid: {
                            display: false
                        }
                    }, y: {
                        stacked: true,

                        grid: {
                            display: false
                        }
                    },
                }
            },
        });
        this.charts.push(chart)
    }

    LineChart.prototype.lineSegmentExample = function () {
        var chartElement = document.getElementById('line-segment-example');
        var dataColors = chartElement.getAttribute('data-colors');
        var colors = dataColors ? dataColors.split(",") : this.defaultColors
        var ctx = chartElement.getContext('2d');
        var chart = new Chart(ctx, {
            type: 'line', data: {
                labels: ['Jan', 'Feb', 'March', 'April', "May", "June", "July"], datasets: [{
                    label: 'Dataset 1',
                    data: [65, 59, NaN, 48, 56, 57, 40],
                    borderColor: colors[0],
                    spanGaps: true,
                    segment: {
                        borderColor: function (ctx){ return skipped(ctx, 'rgb(0,0,0,0.2)') || down(ctx, 'rgb(192,75,75)')},
                        borderDash: function (ctx){ return  skipped(ctx, [6, 6])},
                    },

                }]
            }, options: {
                responsive: true, maintainAspectRatio: false, plugins: {
                    legend: {
                        display: false,

                        position: 'top',
                    },

                }, scales: {
                    x: {
                        stacked: true,

                        grid: {
                            display: false
                        }
                    }, y: {
                        stacked: true,

                        grid: {
                            display: false
                        }
                    },
                }
            },
        });
        this.charts.push(chart)
    }

    LineChart.prototype.steppedExample = function () {
        var chartElement = document.getElementById('stepped-example');
        var dataColors = chartElement.getAttribute('data-colors');
        var colors = dataColors ? dataColors.split(",") : this.defaultColors
        var ctx = chartElement.getContext('2d');
        var chart = new Chart(ctx, {
            type: 'line', data: {
                labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6'], datasets: [{
                    label: 'Dataset 1', data: [12, -19, 14, -15, 14, -8], borderColor: colors[0],  fill: false,
                    stepped: true,

                }, ]
            }, options: {
                responsive: true, maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    axis: 'x'
                },
                plugins: {
                    legend: {
                        display: false,

                        position: 'top',
                    },

                }, scales: {
                    x: {

                        grid: {
                            display: false
                        }
                    }, y: {

                        grid: {
                            display: false
                        }
                    },
                }
            },
        });
        this.charts.push(chart)
    }


    //initializing various components and plugins
    LineChart.prototype.init = function () {
        var $this = this;
        Chart.defaults.font.family = '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen-Sans,Ubuntu,Cantarell,"Helvetica Neue",sans-serif';

        Chart.defaults.color = "#8391a2";
        Chart.defaults.borderColor = "rgba(133, 141, 152, 0.1)";
        // init charts
        this.interpolationExample();
        this.lineExample();
        this.multiAxesExample();
        this.pointStylingExample();
        this.lineSegmentExample();
        this.steppedExample();

        // enable resizing matter


        $(window).on('resizeEnd', function (e) {
            $.each($this.charts, function (index, chart) {
                try {
                    chart.destroy();
                } catch (err) {
                }
            });
            $this.interpolationExample();
            $this.lineExample();
            $this.multiAxesExample();
            $this.pointStylingExample();
            $this.lineSegmentExample();
            $this.steppedExample();
        });

        $(window).resize(function () {
            if (this.resizeTO) clearTimeout(this.resizeTO);
            this.resizeTO = setTimeout(function () {
                $(this).trigger('resizeEnd');
            }, 500);
        });
    };

    //init chart
    $.ChartJs = new LineChart;
    $.ChartJs.Constructor = LineChart
}(window.jQuery),

    //initializing ChartJs
    function ($) {
        "use strict";
        $.ChartJs.init()
    }(window.jQuery);

/* utility function */

function hexToRGB(hex, alpha) {
    var r = parseInt(hex.slice(1, 3), 16), g = parseInt(hex.slice(3, 5), 16), b = parseInt(hex.slice(5, 7), 16);

    if (alpha) {
        return "rgba(" + r + ", " + g + ", " + b + ", " + alpha + ")";
    } else {
        return "rgb(" + r + ", " + g + ", " + b + ")";
    }
}

function skipped(ctx, value) {
    return ctx.p0.skip || ctx.p1.skip ? value : undefined;
}

function down(ctx, value) {
    return ctx.p0.parsed.y > ctx.p1.parsed.y ? value : undefined;
}


