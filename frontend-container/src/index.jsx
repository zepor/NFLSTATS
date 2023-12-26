import React from "react";
import { BrowserRouter } from "react-router-dom";
import { createRoot } from "react-dom/client";
import App from "./App";
import ErrorBoundary from "./components/ErrorBoundary";
import { ApolloProvider } from "@apollo/client";
import client from "./apolloClient";
import { Auth0Provider } from "@auth0/auth0-react";
const root = createRoot(document.getElementById("root"));
const viteauth0Domain = import.meta.env.VITE_AUTH0_DOMAIN;
const viteauth0ClientId = import.meta.env.VITE_AUTH0_CLIENT_ID;
const viteauth0Audience = import.meta.env.VITE_API_AUDIENCE;
const onRedirectCallback = (appState) => {
  window.history.replaceState(
    {},
    document.title,
    appState?.returnTo || "/dashboard/default",
  );
};

root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Auth0Provider
        domain={viteauth0Domain}
        clientId={viteauth0ClientId}
        authorizationParams={{
          redirect_uri: window.location.origin + "/dashboard/default",
          returnto: window.location.origin,
        }}
        onRedirectCallback={onRedirectCallback}
        audience={viteauth0Audience}
      >
        <ApolloProvider client={client}>
          <ErrorBoundary>
            <App />
          </ErrorBoundary>
        </ApolloProvider>
      </Auth0Provider>
    </BrowserRouter>
  </React.StrictMode>,
);
