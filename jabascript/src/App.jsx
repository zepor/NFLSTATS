"use Client";
import React, { Suspense } from "react";
import { useRoutes } from "react-router-dom";
import { Provider } from "react-redux";
import { HelmetProvider, Helmet } from "react-helmet-async";
import { store } from "./redux/store";

import "./i18n";
import routes from "./routes";

import Loader from "./components/Loader";
//import Code from "./components/Code";
//import { ErrorBoundary } from "react-error-boundary";

import ThemeProvider from "./contexts/ThemeProvider";
import SidebarProvider from "./contexts/SidebarProvider";
import LayoutProvider from "./contexts/LayoutProvider";
import ChartJsDefaults from "./utils/ChartJsDefaults";

import AuthProvider from "./contexts/JWTContext";
// import AuthProvider from "./contexts/FirebaseAuthProvider";
// import AuthProvider from "./contexts/Auth0Provider";
// import AuthProvider from "./contexts/CognitoProvider";

const App = () => {
  const content = useRoutes(routes);

  return (
    <HelmetProvider>
      <Helmet titleTemplate="%s | Love of Football - NFL Statistical Analytics Dashboard"
        defaultTitle="Love of Football - NFL Statistical Analytics Dashboard"/>
      <Suspense fallback={<Loader />}>
        <Provider store={store}>
          <ThemeProvider>
            <SidebarProvider>
              <LayoutProvider>
                <ChartJsDefaults />
                <AuthProvider>{content}</AuthProvider>
              </LayoutProvider>
            </SidebarProvider>
          </ThemeProvider>
        </Provider>
      </Suspense>
    </HelmetProvider>
  );
};

export default App;