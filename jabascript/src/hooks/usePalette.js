import { useState, useEffect } from "react";

import { THEME, THEME_PALETTE_LIGHT, THEME_PALETTE_DARK } from "../constants";

import useTheme from "./useTheme";

const usePalette = () => {
  const { theme } = useTheme();

  const [palette, setPalette] = useState(THEME_PALETTE_LIGHT);

  useEffect(() => {
    if (theme === THEME.DARK) {
      setPalette(THEME_PALETTE_DARK);
      //}
      //else if (theme === THEME.TEAM_COLORS && TEAM_COLORS) {
      // Handle team color theme
      //setPalette(TEAM_COLORS);
    } else {
      setPalette(THEME_PALETTE_LIGHT);
    }
    //  }, [theme, team]);
  }, [theme]);

  return palette;
};

export default usePalette;
