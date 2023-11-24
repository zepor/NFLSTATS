import { useState, useEffect } from "react";
import * as Constants from "../constants";
import useTheme from "./useTheme";

const usePalette = () => {
  const { theme } = useTheme();
  const [palette, setPalette] = useState(Constants.THEME_PALETTE_LIGHT);

  useEffect(() => {
    if (theme === Constants.THEME.DARK) {
      setPalette(Constants.THEME_PALETTE_DARK);
    } else if (Constants.TEAMS && Constants.TEAMS[theme]) {
      // Use team-specific colors
      const teamColors = Constants.TEAMS[theme];
      setPalette({
        ...Constants.THEME_PALETTE_LIGHT, // Assuming light theme as base
        primary: teamColors.primary,
        secondary: teamColors.secondary
      });
    } else {
      setPalette(Constants.THEME_PALETTE_LIGHT);
    }
  }, [theme]);

  return palette;
};

export default usePalette;
