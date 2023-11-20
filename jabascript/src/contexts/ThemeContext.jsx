import React from "react";

import { THEME } from "../constants";

const initialState = {
  theme: THEME.DEFAULT,
};

const ThemeContext = React.createContext(initialState);

export default ThemeContext;
