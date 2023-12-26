import React, { Suspense, useEffect } from "react";
import { useNavigate, useRoutes } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import { Provider as ReduxProvider } from "react-redux";
import { HelmetProvider, Helmet } from "react-helmet-async";
import { store } from "./redux/store";
import "./i18n";
import routes from "./routes"; // Your routes configuration
import Loader from "./components/Loader";
import ThemeProvider from "./contexts/ThemeProvider";
import SidebarProvider from "./contexts/SidebarProvider";
import LayoutProvider from "./contexts/LayoutProvider";
import ChartJsDefaults from "./utils/ChartJsDefaults";
import "./builder-components.js";

const App = () => {
  const { isAuthenticated, isLoading } = useAuth0();
  const navigate = useNavigate();

  useEffect(() => {
    if (isLoading) return;

    if (!isAuthenticated) {
      //navigate("/");
    }
  }, [isAuthenticated, isLoading, navigate]);

  const routeContent = useRoutes(routes);

  return (
    <HelmetProvider>
      <Helmet titleTemplate="%s | NFL Dashboard" defaultTitle="NFL Dashboard" />
      <Suspense fallback={<Loader />}>
        <ReduxProvider store={store}>
          <ThemeProvider>
            <SidebarProvider>
              <LayoutProvider>
                <ChartJsDefaults />
                <builder-component
                  model="page"
                  api-key="2c87660801bc48878f989ed5ac733863"
                >
                  {routeContent}
                </builder-component>
              </LayoutProvider>
            </SidebarProvider>
          </ThemeProvider>
        </ReduxProvider>
      </Suspense>
    </HelmetProvider>
  );
};

export default App;
