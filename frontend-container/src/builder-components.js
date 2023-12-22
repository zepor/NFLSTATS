import { Builder, builder } from "@builder.io/react";
import Alerts from "./pages/ui/Alerts";
import Buttons from "./pages/ui/Buttons";
import Carousel from "./pages/ui/Carousel";
import Cards from "./pages/ui/Cards";
import EmbedVideo from "./pages/ui/EmbedVideo";
import General from "./pages/ui/General";
import Grid from "./pages/ui/Grid";
import Modals from "./pages/ui/Modals";
import Offcanvas from "./pages/ui/Offcanvas";
import Tabs from "./pages/ui/Tabs";
import Typography from "./pages/ui/Typography";
import AuthLayout from "./layouts/Auth";
import DashboardLayout from "./layouts/Dashboard";
import DocLayout from "./layouts/Doc";
import LandingLayout from "./layouts/Landing";
import AuthGuard from "./components/guards/AuthGuard";
import Landing from "./pages/landing/Landing";
import BarChart from "./pages/dashboards/Analytics/BarChart";
import Header from "./pages/dashboards/Analytics/Header";
import Analytics from "./pages/dashboards/Analytics/index";
import Languages from "./pages/dashboards/Analytics/Languages";
import PieChart from "./pages/dashboards/Analytics/PieChart";
import RadarChart from "./pages/dashboards/Analytics/RadarChart";
import Statistics from "./pages/dashboards/Analytics/Statistics";
import Traffic from "./pages/dashboards/Analytics/Traffic";
import WorldMap from "./pages/dashboards/Analytics/WorldMap";
import GamesSchedule from "./pages/dashboards/Analytics/Schedule";
//import { accordionConfig } from "@builder.io/widgets/dist/lib/components/Accordion.config";
//import loadable from "@loadable/component";
const colors = ["primary", "secondary", "success", "danger", "warning", "info"];
const components = [
  {
    component: Alerts,
    name: "Alerts",
    inputs: [
      {
        name: "alertType",
        type: "enum",
        enum: [
          "default",
          "icon",
          "outline",
          "coloredOutline",
          "additionalContent",
          "withButtons",
        ],
        defaultValue: "default",
      },
      { name: "color", type: "enum", enum: colors, defaultValue: "primary" },
      {
        name: "content",
        type: "string",
        defaultValue: "Your alert message here",
      },
      { name: "icon", type: "string", defaultValue: "" }, // You can use file picker or a list of icon options
      { name: "dismissible", type: "boolean", defaultValue: true },
    ],
  },
  { component: Buttons, name: "Buttons", inputs: [] },
  { component: Carousel, name: "Carousel", inputs: [] },
  { component: Cards, name: "Cards", inputs: [] },
  { component: EmbedVideo, name: "EmbedVideo", inputs: [] },
  { component: General, name: "General", inputs: [] },
  { component: Grid, name: "Grid", inputs: [] },
  { component: Modals, name: "Modals", inputs: [] },
  { component: Offcanvas, name: "Offcanvas", inputs: [] },
  { component: Tabs, name: "Tabs", inputs: [] },
  { component: Typography, name: "Typography", inputs: [] },
  { component: AuthLayout, name: "AuthLayout", inputs: [] },
  { component: DashboardLayout, name: "DashboardLayout", inputs: [] },
  { component: DocLayout, name: "DocLayout", inputs: [] },
  { component: LandingLayout, name: "LandingLayout", inputs: [] },
  { component: AuthGuard, name: "AuthGuard", inputs: [] },
  { component: Landing, name: "Landing", inputs: [] },
  { component: BarChart, name: "BarChart", inputs: [] },
  { component: Header, name: "Header", inputs: [] },
  { component: Analytics, name: "Analytics", inputs: [] },
  { component: Languages, name: "Languages", inputs: [] },
  { component: PieChart, name: "PieChart", inputs: [] },
  { component: RadarChart, name: "RadarChart", inputs: [] },
  { component: Statistics, name: "Statistics", inputs: [] },
  { component: Traffic, name: "Traffic", inputs: [] },
  { component: WorldMap, name: "WorldMap", inputs: [] },
  { component: GamesSchedule, name: "GamesSchedule", inputs: [] },
];

//Builder.registerComponent(
  //loadable(() =>
    //import("@builder.io/widgets/dist/lib/components/Accordion").then(
    //  (mod) => mod.AccordionComponent,
   // ),
  //),
 // accordionConfig,
//);

components.forEach(({ component, name, inputs }) => {
  Builder.registerComponent(component, {
    name,
    inputs,
  });
});
