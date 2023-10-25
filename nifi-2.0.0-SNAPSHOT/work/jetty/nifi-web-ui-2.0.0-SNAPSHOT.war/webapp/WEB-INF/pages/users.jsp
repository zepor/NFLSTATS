<%--
 Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
--%>
<%@ page contentType="text/html" pageEncoding="UTF-8" session="false" %>
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>NiFi Users</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <link rel="shortcut icon" href="images/nifi16.ico"/>
        <link rel="stylesheet" href="assets/reset.css/reset.css" type="text/css" />
        <link rel="stylesheet" href="css/nf-users-all.css?2.0.0-SNAPSHOT" type="text/css" />
<link rel="stylesheet" href="css/message-pane.css?2.0.0-SNAPSHOT" type="text/css" />
<link rel="stylesheet" href="css/nf-common-ui.css?2.0.0-SNAPSHOT" type="text/css" />
        <link rel="stylesheet" href="js/jquery/tabbs/jquery.tabbs.css?2.0.0-SNAPSHOT" type="text/css" />
        <link rel="stylesheet" href="js/jquery/combo/jquery.combo.css?2.0.0-SNAPSHOT" type="text/css" />
        <link rel="stylesheet" href="js/jquery/modal/jquery.modal.css?2.0.0-SNAPSHOT" type="text/css" />
        <link rel="stylesheet" href="assets/qtip2/dist/jquery.qtip.min.css?" type="text/css" />
        <link rel="stylesheet" href="assets/jquery-ui-dist/jquery-ui.min.css" type="text/css" />
        <link rel="stylesheet" href="assets/slickgrid/slick.grid.css" type="text/css" />
        <link rel="stylesheet" href="css/slick-nifi-theme.css" type="text/css" />
        <link rel="stylesheet" href="fonts/flowfont/flowfont.css" type="text/css" />
        <link rel="stylesheet" href="assets/font-awesome/css/font-awesome.min.css" type="text/css" />
        <script type="text/javascript" src="assets/d3/dist/d3.min.js"></script>
        <script type="text/javascript" src="assets/jquery/dist/jquery.min.js"></script>
        <script type="text/javascript" src="assets/jquery-ui-dist/jquery-ui.min.js"></script>
        <script type="text/javascript" src="js/jquery/jquery.base64.js"></script>
        <script type="text/javascript" src="js/jquery/jquery.center.js"></script>
        <script type="text/javascript" src="js/jquery/tabbs/jquery.tabbs.js?2.0.0-SNAPSHOT"></script>
        <script type="text/javascript" src="js/jquery/combo/jquery.combo.js?2.0.0-SNAPSHOT"></script>
        <script type="text/javascript" src="js/jquery/modal/jquery.modal.js?2.0.0-SNAPSHOT"></script>
        <script type="text/javascript" src="js/jquery/jquery.ellipsis.js"></script>
        <script type="text/javascript" src="js/jquery/jquery.each.js"></script>
        <script type="text/javascript" src="assets/lodash/lodash.min.js"></script>
        <script type="text/javascript" src="assets/moment/min/moment.min.js"></script>
        <script type="text/javascript" src="assets/qtip2/dist/jquery.qtip.min.js"></script>
        <script type="text/javascript" src="assets/slickgrid/lib/jquery.event.drag-2.3.0.js"></script>
        <script type="text/javascript" src="assets/slickgrid/plugins/slick.cellrangeselector.js"></script>
        <script type="text/javascript" src="assets/slickgrid/plugins/slick.cellselectionmodel.js"></script>
        <script type="text/javascript" src="assets/slickgrid/plugins/slick.rowselectionmodel.js"></script>
        <script type="text/javascript" src="assets/slickgrid/plugins/slick.autotooltips.js"></script>
        <script type="text/javascript" src="assets/slickgrid/slick.formatters.js"></script>
        <script type="text/javascript" src="assets/slickgrid/slick.editors.js"></script>
        <script type="text/javascript" src="assets/slickgrid/slick.dataview.js"></script>
        <script type="text/javascript" src="assets/slickgrid/slick.core.js"></script>
        <script type="text/javascript" src="assets/slickgrid/slick.grid.js"></script>
        <script type="text/javascript" src="js/nf/nf-namespace.js?2.0.0-SNAPSHOT"></script>
        <script type="text/javascript" src="js/nf/nf-ng-namespace.js?2.0.0-SNAPSHOT"></script>
        <script type="text/javascript" src="js/nf/users/nf-users-all.js?2.0.0-SNAPSHOT"></script>
        <script type="text/javascript" src="js/jquery/propertytable/jquery.propertytable.js?2.0.0-SNAPSHOT"></script>
        <script type="text/javascript" src="js/jquery/nfeditor/languages/nfel.js?2.0.0-SNAPSHOT"></script>
        <script type="text/javascript" src="js/jquery/nfeditor/languages/nfpr.js?2.0.0-SNAPSHOT"></script>
        <script type="text/javascript" src="js/jquery/nfeditor/jquery.nfeditor.js?2.0.0-SNAPSHOT"></script>
    </head>
    <body ng-controller="ngSummaryAppCtrl">
        <jsp:include page="/WEB-INF/partials/message-pane.jsp"/>
        <jsp:include page="/WEB-INF/partials/banners-utility.jsp"/>
        <jsp:include page="/WEB-INF/partials/ok-dialog.jsp"/>
        <jsp:include page="/WEB-INF/partials/users/user-dialog.jsp"/>
        <jsp:include page="/WEB-INF/partials/users/user-policies-dialog.jsp"/>
        <jsp:include page="/WEB-INF/partials/users/user-delete-dialog.jsp"/>
        <jsp:include page="/WEB-INF/partials/users/users-content.jsp"/>
    </body>
</html>
