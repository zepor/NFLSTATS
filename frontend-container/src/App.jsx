"use Client";
import React, { StrictMode, Suspense, useEffect, useState } from "react";
import { useRoutes, useLocation } from "react-router-dom";
import { Provider } from "react-redux";
import { HelmetProvider, Helmet } from "react-helmet-async";
import { useAuthenticator } from "@aws-amplify/ui-react";
import { BuilderComponent, builder } from "@builder.io/react";
import { store } from "./redux/store";

import "./i18n";
import routes from "./routes";
import Loader from "./components/Loader";
import ThemeProvider from "./contexts/ThemeProvider";
import SidebarProvider from "./contexts/SidebarProvider";
import LayoutProvider from "./contexts/LayoutProvider";
import ChartJsDefaults from "./utils/ChartJsDefaults";

// Import Amplify and configure it
import { Amplify } from "aws-amplify";
import amplifyconfig from "./amplifyconfiguration.json";
Amplify.configure(amplifyconfig);

if (process.env.NODE_ENV === "development") {
  builder.init("8a4223d4ab674935a2a0bbd81ffed92b");
}

const isDevelopment = process.env.NODE_ENV === "development";

const App = () => {
  const location = useLocation();
  const routeContent = useRoutes(routes);
  const { user, signOut } = useAuthenticator((context) => [context.user]);
  const [builderContent, setBuilderContent] = useState(null);

  // Fetch Builder.io content only in development
  useEffect(() => {
    if (isDevelopment) {
      async function fetchBuilderContent() {
        const content = await builder
          .get("page", { url: location.pathname })
          .promise();
        setBuilderContent(content);
      }

      fetchBuilderContent();
    }
  }, [location.pathname]);

  return (
    <StrictMode>
      <HelmetProvider>
        <Helmet
          titleTemplate="%s | Love of Football - NFL Statistical Analytics Dashboard"
          defaultTitle="Love of Football - NFL Statistical Analytics Dashboard"
        />
        <Suspense fallback={<Loader />}>
          <Provider store={store}>
            <ThemeProvider>
              <SidebarProvider>
                <LayoutProvider>
                  <ChartJsDefaults />
                  {isDevelopment && builderContent ? (
                    <BuilderComponent model="page" content={builderContent} />
                  ) : (
                    <main>
                      <h1>{user ? user.username : "Guest"}</h1>
                      {user && <button onClick={signOut}>Sign out</button>}
                      {routeContent}
                    </main>
                  )}
                </LayoutProvider>
              </SidebarProvider>
            </ThemeProvider>
          </Provider>
        </Suspense>
      </HelmetProvider>
    </StrictMode>
  );
};

export default App;
