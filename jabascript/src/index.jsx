import React from "react";
import { BrowserRouter } from "react-router-dom";
import { createRoot } from "react-dom/client";

import App from "./App";
// Note: Remove the following line if you want to disable the API mocks.
import "./mocks";
import "jsvectormap";
import "./vendor/world.js";
import "./vendor/us_aea_en.js";

const container = document.getElementById("root");
const root = createRoot(container);

root.render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);
