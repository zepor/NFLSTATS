// Mock implementation of lazy function to return component paths as strings
const lazy = (pathFunc) => {
    return pathFunc().then(mod => mod);
};

const React = {
    createElement: (component) => ({ type: { name: component } })
};
const Landing = lazy(() => Promise.resolve("./pages/landing/Landing"));
const Default = lazy(() =>  Promise.resolve("./pages/dashboards/Default"));
const Analytics = lazy(() => Promise.resolve("./pages/dashboards/Analytics"));
const SaaS = lazy(() => Promise.resolve("./pages/dashboards/SaaS"));
const Social = lazy(() =>  Promise.resolve("./pages/dashboards/Social"));
const Crypto = lazy(() =>  Promise.resolve("./pages/dashboards/Crypto"));
const Profile = lazy(() =>  Promise.resolve("./pages/pages/Profile"));
const Settings = lazy(() =>  Promise.resolve("./pages/pages/Settings"));
const Clients = lazy(() =>  Promise.resolve("./pages/pages/Clients"));
const Projects = lazy(() =>  Promise.resolve("./pages/pages/Projects"));
const Invoice = lazy(() =>  Promise.resolve("./pages/pages/Invoice"));
const Pricing = lazy(() =>  Promise.resolve("./pages/pages/Pricing"));
const Tasks = lazy(() =>  Promise.resolve("./pages/pages/Tasks"));
const Chat = lazy(() =>  Promise.resolve("./pages/pages/Chat"));
const Blank = lazy(() =>  Promise.resolve("./pages/pages/Blank"));
const Page500 = lazy(() =>  Promise.resolve("./pages/auth/Page500"));
const Page404 = lazy(() =>  Promise.resolve("./pages/auth/Page404"));
const SignIn = lazy(() =>  Promise.resolve("./pages/auth/SignIn"));
const SignUp = lazy(() =>  Promise.resolve("./pages/auth/SignUp"));
const ResetPassword = lazy(() =>  Promise.resolve("./pages/auth/ResetPassword"));
const Alerts = lazy(() =>  Promise.resolve("./pages/ui/Alerts"));
const Buttons = lazy(() =>  Promise.resolve("./pages/ui/Buttons"));
const Cards = lazy(() =>  Promise.resolve("./pages/ui/Cards"));
const Carousel = lazy(() =>  Promise.resolve("./pages/ui/Carousel"));
const EmbedVideo = lazy(() =>  Promise.resolve("./pages/ui/EmbedVideo"));
const General = lazy(() =>  Promise.resolve("./pages/ui/General"));
const Grid = lazy(() =>  Promise.resolve("./pages/ui/Grid"));
const Modals = lazy(() =>  Promise.resolve("./pages/ui/Modals"));
const Offcanvas = lazy(() =>  Promise.resolve("./pages/ui/Offcanvas"));
const Tabs = lazy(() =>  Promise.resolve("./pages/ui/Tabs"));
const Typography = lazy(() =>  Promise.resolve("./pages/ui/Typography"));
const Feather = lazy(() =>  Promise.resolve("./pages/icons/Feather"));
const FontAwesome = lazy(() =>  Promise.resolve("./pages/icons/FontAwesome"));
const Layouts = lazy(() =>  Promise.resolve("./pages/forms/Layouts"));
const BasicInputs = lazy(() =>  Promise.resolve("./pages/forms/BasicInputs"));
const InputGroups = lazy(() =>  Promise.resolve("./pages/forms/InputGroups"));
const FloatingLabels = lazy(() =>  Promise.resolve("./pages/forms/FloatingLabels"));
const AdvancedInputs = lazy(() =>  Promise.resolve("./pages/forms/AdvancedInputs"));
const Formik = lazy(() =>  Promise.resolve("./pages/forms/Formik"));
const Editors = lazy(() =>  Promise.resolve("./pages/forms/Editors"));
const Tables = lazy(() =>  Promise.resolve("./pages/tables/Tables"));
const Pagination = lazy(() =>  Promise.resolve("./pages/tables/Pagination"));
const ColumnSorting = lazy(() =>  Promise.resolve("./pages/tables/ColumnSorting"));
const ColumnFiltering = lazy(() =>  Promise.resolve("./pages/tables/ColumnFiltering"));
const RowExpanding = lazy(() =>  Promise.resolve("./pages/tables/RowExpanding"));
const RowSelection = lazy(() =>  Promise.resolve("./pages/tables/RowSelection"));
const Chartjs = lazy(() =>  Promise.resolve("./pages/charts/Chartjs"));
const ApexCharts = lazy(() =>  Promise.resolve("./pages/charts/ApexCharts"));
const Notifications = lazy(() =>  Promise.resolve("./pages/notifications/Notifications"));
const GoogleMaps = lazy(() =>  Promise.resolve("./pages/maps/GoogleMaps"));
const VectorMaps = lazy(() =>  Promise.resolve("./pages/maps/VectorMaps"));
const Calendar = lazy(() =>  Promise.resolve("./pages/calendar/Calendar"));
const Introduction = lazy(() =>  Promise.resolve("./pages/docs/Introduction"));
const GettingStarted = lazy(() =>  Promise.resolve("./pages/docs/GettingStarted"));
const Routing = lazy(() =>  Promise.resolve("./pages/docs/Routing"));
const Auth0 = lazy(() =>  Promise.resolve("./pages/docs/auth/Auth0"));
const Cognito = lazy(() =>  Promise.resolve("./pages/docs/auth/Cognito"));
const Firebase = lazy(() =>  Promise.resolve("./pages/docs/auth/Firebase"));
const JWT = lazy(() =>  Promise.resolve("./pages/docs/auth/JWT"));
const Guards = lazy(() =>  Promise.resolve("./pages/docs/Guards"));
const APICalls = lazy(() =>  Promise.resolve("./pages/docs/APICalls"));
const Redux = lazy(() =>  Promise.resolve("./pages/docs/Redux"));
const Internationalization = lazy(() =>
   Promise.resolve("./pages/docs/Internationalization")
);
const EnvironmentVariables = lazy(() =>
   Promise.resolve("./pages/docs/EnvironmentVariables")
);
const ESLintAndPrettier = lazy(() =>  Promise.resolve("./pages/docs/ESLintAndPrettier"));
const Deployment = lazy(() =>  Promise.resolve("./pages/docs/Deployment"));
const MigratingToNextJS = lazy(() =>  Promise.resolve("./pages/docs/MigratingToNextJS"));
const Support = lazy(() =>  Promise.resolve("./pages/docs/Support"));
const Changelog = lazy(() =>  Promise.resolve("./pages/docs/Changelog"));
const ProtectedPage = lazy(() =>  Promise.resolve("./pages/protected/ProtectedPage"));

const AuthLayout = Promise.resolve("./layouts/Auth");
const DashboardLayout = Promise.resolve("./layouts/Dashboard");
const DocLayout = Promise.resolve("./layouts/Doc");
const LandingLayout = Promise.resolve("./layouts/Landing");
const AuthGuard = Promise.resolve("./components/guards/AuthGuard");
const routes = [
  {
    path: "/",
    element: React.createElement(LandingLayout),
    children: [
      {
        path: "",
        element: React.createElement(Landing),
      },
    ],
  },
  {
    path: "dashboard",
    element: React.createElement(DashboardLayout),
    children: [
      {
        path: "default",
        element: React.createElement(Default),
      },
      {
        path: "analytics",
        element: React.createElement(Analytics),
      },
      {
        path: "saas",
        element: React.createElement(SaaS),
      },
      {
        path: "social",
        element: React.createElement(Social),
      },
      {
        path: "crypto",
        element: React.createElement(Crypto),
      },
    ],
  },
  {
    path: "pages",
    element: React.createElement(DashboardLayout),
    children: [
      {
        path: "profile",
        element: React.createElement(Profile),
      },
      {
        path: "settings",
        element: React.createElement(Settings),
      },
      {
        path: "clients",
        element: React.createElement(Clients),
      },
      {
        path: "projects",
        element: React.createElement(Projects),
      },
      {
        path: "invoice",
        element: React.createElement(Invoice),
      },
      {
        path: "pricing",
        element: React.createElement(Pricing),
      },
      {
        path: "tasks",
        element: React.createElement(Tasks),
      },
      {
        path: "chat",
        element: React.createElement(Chat),
      },
      {
        path: "blank",
        element: React.createElement(Blank),
      },
    ],
  },
  {
    path: "auth",
    element: React.createElement(AuthLayout),
    children: [
      {
        path: "sign-in",
        element: React.createElement(SignIn),
      },
      {
        path: "sign-up",
        element: React.createElement(SignUp),
      },
      {
        path: "reset-password",
        element: React.createElement(ResetPassword),
      },
      {
        path: "404",
        element: React.createElement(Page404),
      },
      {
        path: "500",
        element: React.createElement(Page500),
      },
    ],
  },
  {
    path: "ui",
    element: React.createElement(DashboardLayout),
    children: [
      {
        path: "alerts",
        element: React.createElement(Alerts),
      },
      {
        path: "buttons",
        element: React.createElement(Buttons),
      },
      {
        path: "cards",
        element: React.createElement(Cards),
      },
      {
        path: "carousel",
        element: React.createElement(Carousel),
      },
      {
        path: "embed-video",
        element: React.createElement(EmbedVideo),
      },
      {
        path: "general",
        element: React.createElement(General),
      },
      {
        path: "grid",
        element: React.createElement(Grid),
      },
      {
        path: "modals",
        element: React.createElement(Modals),
      },
      {
        path: "tabs",
        element: React.createElement(Tabs),
      },
      {
        path: "offcanvas",
        element: React.createElement(Offcanvas),
      },
      {
        path: "typography",
        element: React.createElement(Typography),
      },
    ],
  },
  {
    path: "icons",
    element: React.createElement(DashboardLayout),
    children: [
      {
        path: "feather",
        element: React.createElement(Feather),
      },
      {
        path: "font-awesome",
        element: React.createElement(FontAwesome),
      },
    ],
  },
  {
    path: "forms",
    element: React.createElement(DashboardLayout),
    children: [
      {
        path: "layouts",
        element: React.createElement(Layouts),
      },
      {
        path: "basic-inputs",
        element: React.createElement(BasicInputs),
      },
      {
        path: "input-groups",
        element: React.createElement(InputGroups),
      },
      {
        path: "floating-labels",
        element: React.createElement(FloatingLabels),
      },
    ],
  },
  {
    path: "tables",
    element: React.createElement(DashboardLayout),
    children: [
      {
        path: "",
        element: React.createElement(Tables),
      },
    ],
  },
  {
    path: "form-plugins",
    element: React.createElement(DashboardLayout),
    children: [
      {
        path: "advanced-inputs",
        element: React.createElement(AdvancedInputs),
      },
      {
        path: "formik",
        element: React.createElement(Formik),
      },
      {
        path: "editors",
        element: React.createElement(Editors),
      },
    ],
  },
  {
    path: "advanced-tables",
    element: React.createElement(DashboardLayout),
    children: [
      {
        path: "pagination",
        element: React.createElement(Pagination),
      },
      {
        path: "column-sorting",
        element: React.createElement(ColumnSorting),
      },
      {
        path: "column-filtering",
        element: React.createElement(ColumnFiltering),
      },
      {
        path: "row-expanding",
        element: React.createElement(RowExpanding),
      },
      {
        path: "row-selection",
        element: React.createElement(RowSelection),
      },
    ],
  },
  {
    path: "charts",
    element: React.createElement(DashboardLayout),
    children: [
      {
        path: "chartjs",
        element: React.createElement(Chartjs),
      },
      {
        path: "apexcharts",
        element: React.createElement(ApexCharts),
      },
    ],
  },
  {
    path: "notifications",
    element: React.createElement(DashboardLayout),
    children: [
      {
        path: "",
        element: React.createElement(Notifications),
      },
    ],
  },
  {
    path: "maps",
    element: React.createElement(DashboardLayout),
    children: [
      {
        path: "google-maps",
        element: React.createElement(GoogleMaps),
      },
      {
        path: "vector-maps",
        element: React.createElement(VectorMaps),
      },
    ],
  },
  {
    path: "calendar",
    element: React.createElement(DashboardLayout),
    children: [
      {
        path: "",
        element: React.createElement(Calendar),
      },
    ],
  },
  {
    path: "docs",
    element: React.createElement(DocLayout),
    children: [
      {
        path: "introduction",
        element: React.createElement(Introduction),
      },
      {
        path: "getting-started",
        element: React.createElement(GettingStarted),
      },
      {
        path: "routing",
        element: React.createElement(Routing),
      },
      {
        path: "auth/auth0",
        element: React.createElement(Auth0),
      },
      {
        path: "auth/cognito",
        element: React.createElement(Cognito),
      },
      {
        path: "auth/firebase",
        element: React.createElement(Firebase),
      },
      {
        path: "auth/jwt",
        element: React.createElement(JWT),
      },
      {
        path: "guards",
        element: React.createElement(Guards),
      },
      {
        path: "api-calls",
        element: React.createElement(APICalls),
      },
      {
        path: "redux",
        element: React.createElement(Redux),
      },
      {
        path: "internationalization",
        element: React.createElement(Internationalization),
      },
      {
        path: "environment-variables",
        element: React.createElement(EnvironmentVariables),
      },
      {
        path: "eslint-and-prettier",
        element: React.createElement(ESLintAndPrettier),
      },
      {
        path: "deployment",
        element: React.createElement(Deployment),
      },
      {
        path: "migrating-to-next-js",
        element: React.createElement(MigratingToNextJS),
      },
      {
        path: "support",
        element: React.createElement(Support),
      },
      {
        path: "changelog",
        element: React.createElement(Changelog),
      },
    ],
  },
  {
    path: "private",
    element: React.createElement(AuthGuard, {}, React.createElement(DashboardLayout)),
    children: [
      {
        path: "",
        element: React.createElement(ProtectedPage),
      },
    ],
  },


  {
    path: "*",
    element: React.createElement(AuthLayout),
    children: [
      {
        path: "*",
        element: React.createElement(Page404),
      },
    ],
  },
];

export default routes;
