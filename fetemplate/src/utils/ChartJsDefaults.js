import { useEffect } from "react";
import { Chart, defaults, registerables } from "chart.js";

import usePalette from "../hooks/usePalette";

Chart.register(...registerables);

const ChartJsDefaults = () => {
  const palette = usePalette();

  useEffect(() => {
    defaults.color = palette["gray-600"];
    defaults.font.family =
      "'Poppins', 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif";
  }, [palette]);

  return null;
};

export default ChartJsDefaults;
