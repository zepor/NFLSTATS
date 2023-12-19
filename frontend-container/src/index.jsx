import React from "react";
import { BrowserRouter } from "react-router-dom";
import { createRoot } from "react-dom/client";
import App from "./App";
import ErrorBoundary from "./components/ErrorBoundary";
import { ApolloProvider } from "@apollo/client";
import client from "./apolloClient";

const container = document.getElementById("root");
const root = createRoot(container);

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
