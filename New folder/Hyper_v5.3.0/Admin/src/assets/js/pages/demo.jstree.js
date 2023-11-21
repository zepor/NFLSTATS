/**
 * Theme: Hyper - Responsive Bootstrap 5 Admin Dashboard
 * Author: Coderthemes
 * Module/App: Chartjs 
 */

! function ($) {
    "use strict";

    var JSTree = function () {
        this.$body = $("body")
    };

        //initializing various components and plugins
        JSTree.prototype.init = function () {

            // jstree-1
            $("#jstree-1").jstree({
                "core": {
                    "themes": {
                        "responsive": false
                    }
                },
                "types": {
                    "default": {
                        "icon": "ri-folder-line"
                    },
                    "file": {
                        "icon": "ri-article-line"
                    }
                },
                "plugins": ["types"]
            });

            // handle link clicks in tree nodes(support target="_blank" as well)
            $('#jstree-1').on('select_node.jstree', function(e, data) {
                var link = $('#' + data.selected).find('a');
                if (link.attr("href") != "#" && link.attr("href") != "javascript:;" && link.attr("href") != "") {
                    if (link.attr("target") == "_blank") {
                        link.attr("href").target = "_blank";
                    }
                    document.location.href = link.attr("href");
                    return false;
                }
            });


            // jstree-2
            $('#jstree-2').jstree({
                "core": {
                    "themes": {
                        "responsive": false
                    }
                },
                "types": {
                    "default": {
                        "icon": "ri-folder-line text-warning"
                    },
                    "file": {
                        "icon": "ri-article-line  text-warning"
                    }
                },
                "plugins": ["types"]
            });

            $('#jstree-2').on('select_node.jstree', function(e, data) {
                var link = $('#' + data.selected).find('a');
                if (link.attr("href") != "#" && link.attr("href") != "javascript:;" && link.attr("href") != "") {
                    if (link.attr("target") == "_blank") {
                        link.attr("href").target = "_blank";
                    }
                    document.location.href = link.attr("href");
                    return false;
                }
            });


            // jstree-3
            $('#jstree-3').jstree({
                "plugins": ["wholerow", "checkbox", "types"],
                "core": {
                    "themes": {
                        "responsive": false
                    },
                    "data": [{
                           "text": "Same but with checkboxes",
                            "children": [{
                                "text": "initially selected",
                                "state": {
                                    "selected": true
                                }
                            }, {
                                "text": "custom icon",
                                "icon": "ri-feedback-line text-danger"
                            }, {
                                "text": "initially open",
                                "icon": "ri-folder-line text-default",
                                "state": {
                                    "opened": true
                                },
                                "children": ["Another node"]
                            }, {
                                "text": "custom icon",
                                "icon": "ri-article-line text-warning"
                            }, {
                                "text": "disabled node",
                                "icon": "ri-close-circle-line text-success",
                                "state": {
                                    "disabled": true
                                }
                            }]
                        },
                        "And wholerow selection"
                    ]
                },
                "types": {
                    "default": {
                        "icon": "ri-folder-line text-warning"
                    },
                    "file": {
                        "icon": "ri-article-line  text-warning"
                    }
                },
            });



            // jstree-4
            $("#jstree-4").jstree({
                "core": {
                    "themes": {
                        "responsive": false
                    },
                    // so that create works
                    "check_callback": true,
                    "data": [{
                            "text": "Parent Node",
                            "children": [{
                                "text": "Initially selected",
                                "state": {
                                    "selected": true
                                }
                            }, {
                                "text": "Custom Icon",
                                "icon": "ri-feedback-line text-danger"
                            }, {
                                "text": "Initially open",
                                "icon": "ri-folder-line text-success",
                                "state": {
                                    "opened": true
                                },
                                "children": [{
                                    "text": "Another node",
                                    "icon": "ri-article-line text-warning"
                                }]
                            }, {
                                "text": "Another Custom Icon",
                                "icon": "ri-article-line text-warning"
                            }, {
                                "text": "Disabled Node",
                                "icon": "ri-close-circle-line text-success",
                                "state": {
                                    "disabled": true
                                }
                            }, {
                                "text": "Sub Nodes",
                                "icon": "ri-folder-line text-danger",
                                "children": [{
                                        "text": "Item 1",
                                        "icon": "ri-article-line text-warning"
                                    },
                                    {
                                        "text": "Item 2",
                                        "icon": "ri-article-line text-success"
                                    },
                                    {
                                        "text": "Item 3",
                                        "icon": "ri-article-line text-default"
                                    },
                                    {
                                        "text": "Item 4",
                                        "icon": "ri-article-line text-danger"
                                    },
                                    {
                                        "text": "Item 5",
                                        "icon": "ri-article-line text-info"
                                    }
                                ]
                            }]
                        },
                        "Another Node"
                    ]
                },
                "types": {
                    "default": {
                        "icon": "ri-folder-line text-primary"
                    },
                    "file": {
                        "icon": "ri-article-line  text-primary"
                    }
                },
                "state": {
                    "key": "demo2"
                },
                "plugins": ["contextmenu", "state", "types"]
            });



            // jstree-5
            $("#jstree-5").jstree({
                "core": {
                    "themes": {
                        "responsive": false
                    },
                    // so that create works
                    "check_callback": true,
                    "data": [{
                            "text": "Parent Node",
                            "children": [{
                                "text": "Initially selected",
                                "state": {
                                    "selected": true
                                }
                            }, {
                                "text": "Custom Icon",
                                "icon": "ri-article-line text-danger"
                            }, {
                                "text": "Initially open",
                                "icon": "ri-folder-line text-success",
                                "state": {
                                    "opened": true
                                },
                                "children": [{
                                    "text": "Another node",
                                    "icon": "ri-article-line text-warning"
                                }]
                            }, {
                                "text": "Another Custom Icon",
                                "icon": "ri-line-chart-line text-warning"
                            }, {
                                "text": "Disabled Node",
                                "icon": "ri-close-circle-line text-success",
                                "state": {
                                    "disabled": true
                                }
                            }, {
                                "text": "Sub Nodes",
                                "icon": "ri-folder-line text-danger",
                                "children": [{
                                        "text": "Item 1",
                                        "icon": "ri-article-line text-warning"
                                    },
                                    {
                                        "text": "Item 2",
                                        "icon": "ri-article-line text-success"
                                    },
                                    {
                                        "text": "Item 3",
                                        "icon": "ri-article-line text-default"
                                    },
                                    {
                                        "text": "Item 4",
                                        "icon": "ri-article-line text-danger"
                                    },
                                    {
                                        "text": "Item 5",
                                        "icon": "ri-article-line text-info"
                                    }
                                ]
                            }]
                        },
                        "Another Node"
                    ]
                },
                "types": {
                    "default": {
                        "icon": "ri-folder-line text-success"
                    },
                    "file": {
                        "icon": "ri-article-line  text-success"
                    }
                },
                "state": {
                    "key": "demo2"
                },
                "plugins": ["dnd", "state", "types"]
            });




            // jstree-6
            $("#jstree-6").jstree({
                "core": {
                    "themes": {
                        "responsive": false
                    },
                    // so that create works
                    "check_callback": true,
                    'data' : {
                        'url' : function (node) {
                          return node.id === '#' ?
                            'assets/data/ajax_demo_children.json' : 'assets/data/ajax_demo_children.json';
                        },
                        'data' : function (node) {
                          return { 'id' : node.id };
                        }
                      }
                },
                "types": {
                    "default": {
                        "icon": "ri-folder-line text-primary"
                    },
                    "file": {
                        "icon": "ri-article-line  text-primary"
                    }
                },
                "state": {
                    "key": "demo3"
                },
                "plugins": ["dnd", "state", "types"]
            });

        },

        //init flotchart
        $.JSTree = new JSTree, $.JSTree.Constructor = JSTree
}(window.jQuery),

    //initializing ChartJs
    function ($) {
        "use strict";
        $.JSTree.init()
    }(window.jQuery);
    