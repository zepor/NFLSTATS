import React from "react";
import { useTheme } from "../hooks/useTheme";
import { THEME } from "../constants";

const ThemeSelector = () => {
  const { setTheme } = useTheme();

  const handleThemeChange = (newTheme) => {
    setTheme(newTheme);
  };

  return (
    <div>
      <button onClick={() => handleThemeChange(THEME.LIGHT)}>Light Theme</button>
      <button onClick={() => handleThemeChange(THEME.DARK)}>Dark Theme</button>
      <button onClick={() => handleThemeChange(THEME.TEAM_COLOR)}>Team Colors</button>
    </div>
  );
};

export default ThemeSelector;
