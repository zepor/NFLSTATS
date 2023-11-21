/**
 * Theme: Hyper - Responsive Bootstrap 5 Admin Dashboard
 * Author: Coderthemes
 * Module/App: Chartjs
 */

!function ($) {
    "use strict";

    var BarChart = function () {
        this.$body = $("body");
        this.charts = [];

        this.defaultColors = ["#727cf5", "#0acf97", "#fa5c7c", "#ffbc00"];


    };

    BarChart.prototype.borderRadiusExample = function () {
        var chartElement = document.getElementById('border-radius-example');
        var dataColors = chartElement.getAttribute('data-colors');
        var colors = dataColors ? dataColors.split(",") : this.defaultColors;
        var ctx = chartElement.getContext('2d');
        var chart = new Chart(ctx, {
            type: 'bar', data: {
                labels: ['Jan', 'Feb', 'March', 'April', 'May', 'June'], datasets: [{
                    label: 'Fully Rounded',
                    data: [12, -19, 14, -15, 12, -14],
                    borderColor: colors[0],
                    backgroundColor: hexToRGB(colors[0], .3),
                    borderWidth: 2,
                    borderRadius: Number.MAX_VALUE,
                    borderSkipped: false,
                }, {
                    label: 'Small Radius',
                    data: [-10, 19, -15, -8, 12, -7],
                    backgroundColor: hexToRGB(colors[1], .3),
                    borderColor: colors[1],
                    borderWidth: 2,
                    borderRadius: 5,
                    borderSkipped: false,
                }]
            }, options: {
                responsive: true, maintainAspectRatio: false,

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

        this.charts.push(chart);
    }


    BarChart.prototype.floatingBarExample = function () {
        var chartElement = document.getElementById('floating-example');
        var dataColors = chartElement.getAttribute('data-colors');
        var colors = dataColors ? dataColors.split(",") : this.defaultColors
        var ctx = chartElement.getContext('2d');
        var chart = new Chart(ctx, {
            type: 'bar', data: {
                labels: ['Jan', 'Feb', 'March', 'April', 'May', 'June'], datasets: [{
                    label: 'Fully Rounded', data: [12, -19, 14, -15, 12, -14], backgroundColor: colors[0],
                }, {
                    label: 'Small Radius', data: [-10, 19, -15, -8, 12, -7], backgroundColor: colors[1],
                }]
            }, options: {
                responsive: true, maintainAspectRatio: false,

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

    BarChart.prototype.horizontalExample = function () {
        var chartElement = document.getElementById('horizontal-example');
        var dataColors = chartElement.getAttribute('data-colors');
        var colors = dataColors ? dataColors.split(",") : this.defaultColors
        var ctx = chartElement.getContext('2d');
        var chart = new Chart(ctx, {
            type: 'bar', data: {
                labels: ['Jan', 'Feb', 'March', 'April'], datasets: [{
                    label: 'Fully Rounded',
                    data: [12, -19, 14, -15],
                    borderColor: colors[0],
                    backgroundColor: hexToRGB(colors[0], 0.3),
                    borderWidth: 1,
                }, {
                    label: 'Small Radius',
                    data: [-10, 19, -15, -8],
                    backgroundColor: hexToRGB(colors[1], 0.3),
                    borderColor: colors[1],
                    borderWidth: 1,
                }]
            }, options: {
                indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: {
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

    BarChart.prototype.stackedExample = function () {
        var chartElement = document.getElementById('stacked-example');
        var dataColors = chartElement.getAttribute('data-colors');
        var colors = dataColors ? dataColors.split(",") : this.defaultColors
        var ctx = chartElement.getContext('2d');
        var chart = new Chart(ctx, {
            type: 'bar', data: {
                labels: ['Jan', 'Feb', 'March', 'April'], datasets: [{
                    label: 'Dataset 1', data: [12, -19, 14, -15], backgroundColor: colors[0],
                }, {
                    label: 'Dataset 2', data: [-10, 19, -15, -8], backgroundColor: colors[1],
                }, {
                    label: 'Dataset 3', data: [-10, 19, -15, -8], backgroundColor: colors[2],
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

    BarChart.prototype.groupStackedExample = function () {
        var chartElement = document.getElementById('group-stack-example');
        var dataColors = chartElement.getAttribute('data-colors');
        var colors = dataColors ? dataColors.split(",") : this.defaultColors
        var ctx = chartElement.getContext('2d');
        var chart = new Chart(ctx, {
            type: 'bar', data: {
                labels: ['Jan', 'Feb', 'March', 'April'], datasets: [{
                    label: 'Dataset 1', data: [12, -19, 14, -15], backgroundColor: colors[0], stack: 'Stack 0',

                }, {
                    label: 'Dataset 2', data: [-10, 19, -15, -8], backgroundColor: colors[1], stack: 'Stack 0',

                }, {
                    label: 'Dataset 3', data: [-10, 19, -15, -8], backgroundColor: colors[2], stack: 'Stack 1',

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

    BarChart.prototype.verticalExample = function () {
        var chartElement = document.getElementById('vertical-example');
        var dataColors = chartElement.getAttribute('data-colors');
        var colors = dataColors ? dataColors.split(",") : this.defaultColors
        var ctx = chartElement.getContext('2d');
        var chart = new Chart(ctx, {
            type: 'bar', data: {
                labels: ['Jan', 'Feb', 'March', 'April'], datasets: [{
                    label: 'Dataset 1', data: [12, -19, 14, -15], backgroundColor: colors[0],

                }, {
                    label: 'Dataset 2', data: [-10, 19, -15, -8], backgroundColor: colors[1],

                }]
            }, options: {
                responsive: true, maintainAspectRatio: false, plugins: {
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
    BarChart.prototype.init = function () {
        var $this = this;
        Chart.defaults.font.family = '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen-Sans,Ubuntu,Cantarell,"Helvetica Neue",sans-serif';

        Chart.defaults.color = "#8391a2";
        Chart.defaults.borderColor = "rgba(133, 141, 152, 0.1)";
        // init charts
        this.borderRadiusExample();
        this.floatingBarExample();
        this.horizontalExample();
        this.stackedExample();
        this.groupStackedExample();
        this.verticalExample();

        // enable resizing matter


        $(window).on('resizeEnd', function (e) {
            $.each($this.charts, function (index, chart) {
                try {
                    chart.destroy();
                } catch (err) {
                }
            });
            $this.borderRadiusExample();
            $this.floatingBarExample();
            $this.horizontalExample();
            $this.stackedExample();
            $this.groupStackedExample();
            $this.verticalExample();
        });

        $(window).resize(function () {
            if (this.resizeTO) clearTimeout(this.resizeTO);
            this.resizeTO = setTimeout(function () {
                $(this).trigger('resizeEnd');
            }, 500);
        });
    };

    //init chart
    $.ChartJs = new BarChart;
    $.ChartJs.Constructor = BarChart
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


