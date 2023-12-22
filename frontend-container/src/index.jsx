import React from "react";
import { BrowserRouter } from "react-router-dom";
import { createRoot } from "react-dom/client";
import App from "./App";
import ErrorBoundary from "./components/ErrorBoundary";
import { ApolloProvider } from "@apollo/client";
import client from "./apolloClient";

const container = document.getElementById("root");
const root = createRoot(container);
const { auth } = require("express-openid-connect");

const config = {
  authRequired: false,
  auth0Logout: true,
  secret: process.env.AUTH0_SECRET,
  baseURL: process.env.AUTH0_BASE_URL,
  clientID: process.env.AUTH0_CLIENT_ID,
  issuerBaseURL: process.env.AUTH0_ISSUER_BASE_URL,
};
// auth router attaches /login, /logout, and /callback routes to the baseURL
App.use(auth(config));
// req.isAuthenticated is provided from the auth router
App.get("/", (req, res) => {
  res.send(req.oidc.isAuthenticated() ? "Logged in" : "Logged out");
});
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <ApolloProvider client={client}>
        <ErrorBoundary>
          <App />
        </ErrorBoundary>
      </ApolloProvider>
    </BrowserRouter>
  </React.StrictMode>,
);
