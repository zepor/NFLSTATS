import React, { Suspense } from "react";
import { useRoutes } from "react-router-dom";
import { Provider as ReduxProvider } from "react-redux";
import { HelmetProvider, Helmet } from "react-helmet-async";
import { store } from "./redux/store";
import "./i18n";
import routes from "./routes";
import Loader from "./components/Loader";
import ThemeProvider from "./contexts/ThemeProvider";
import SidebarProvider from "./contexts/SidebarProvider";
import LayoutProvider from "./contexts/LayoutProvider";
import ChartJsDefaults from "./utils/ChartJsDefaults";
import AuthProvider from "./contexts/CognitoProvider";
import "./builder-components.js";

const App = () => {
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
                <AuthProvider>
                  <builder-component
                    model="page"
                    api-key="2c87660801bc48878f989ed5ac733863"
                  >
                    {routeContent}
                  </builder-component>
                </AuthProvider>
              </LayoutProvider>
            </SidebarProvider>
          </ThemeProvider>
        </ReduxProvider>
      </Suspense>
    </HelmetProvider>
  );
};

export default App;
