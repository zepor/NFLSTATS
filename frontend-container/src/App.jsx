import React, { StrictMode, Suspense } from "react";
import { useRoutes } from "react-router-dom";
import { Provider as ReduxProvider } from "react-redux";
import { HelmetProvider, Helmet } from "react-helmet-async";
import { store } from "./redux/store";
import routes from "./routes";
import Loader from "./components/Loader";
import ThemeProvider from "./contexts/ThemeProvider";
import SidebarProvider from "./contexts/SidebarProvider";
import LayoutProvider from "./contexts/LayoutProvider";
import ChartJsDefaults from "./utils/ChartJsDefaults";
import AuthProvider from "./contexts/CognitoContext";

const App = () => {
  const routeContent = useRoutes(routes);

  return (
    <StrictMode>
      <HelmetProvider>
        <Helmet
          titleTemplate="%s | NFL Dashboard"
          defaultTitle="NFL Dashboard"
        />
        <Suspense fallback={<Loader />}>
          <ReduxProvider store={store}>
            <ThemeProvider>
              <SidebarProvider>
                <LayoutProvider>
                  <ChartJsDefaults />
                  <AuthProvider>{routeContent}</AuthProvider>
                </LayoutProvider>
              </SidebarProvider>
            </ThemeProvider>
          </ReduxProvider>
        </Suspense>
      </HelmetProvider>
    </StrictMode>
  );
};

export default App;
