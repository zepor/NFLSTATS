import React from "react";
import { BrowserRouter } from "react-router-dom";
import { createRoot } from "react-dom/client";
import App from "./App";
import ErrorBoundary from "./components/ErrorBoundary";
import { ApolloProvider } from "@apollo/client";
import client from "./apolloClient";
import { Auth0Provider } from "@auth0/auth0-react";

const root = createRoot(document.getElementById('root'));

const auth0Domain = process.env.VITE_AUTH0_DOMAIN; // Set these in your .env file
const auth0ClientId = process.env.VITE_AUTH0_CLIENT_ID;

root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Auth0Provider
        domain={auth0Domain}
        clientId={auth0ClientId}
        redirectUri={window.location.origin}
      >
        <ApolloProvider client={client}>
          <ErrorBoundary>
            <App />
          </ErrorBoundary>
        </ApolloProvider>
      </Auth0Provider>
    </BrowserRouter>
  </React.StrictMode>
);
