// src/contexts/LayoutProvider.jsx
import React from "react";
import { LAYOUT } from "../constants";
import useSettingsState from "../hooks/useSettingsState";

import LayoutContext from "./LayoutContext"; // Import the context

function LayoutProvider({ children }) {
  const [layout, setLayout] = useSettingsState("layout", LAYOUT.FLUID);

  return (
    <LayoutContext.Provider value={{ layout, setLayout }}>
      {children}
    </LayoutContext.Provider>
  );
}

export default LayoutProvider;
