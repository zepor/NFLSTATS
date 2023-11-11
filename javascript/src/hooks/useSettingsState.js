import { useEffect } from "react";
import useLocalStorage from "./useLocalStorage";

function useSettingsState(key, initialValue) {
  const [value, setValue] = useLocalStorage(key, initialValue);

  useEffect(() => {
    // Set data attribute on body element
    document.body.dataset[key] = value;

    // Replace stylesheet if dark theme gets toggled
    if (key === "theme") {
      const theme = value === "dark" ? "dark" : "light";

      const stylesheet = document.querySelector(".js-stylesheet");
      if (stylesheet) {
        if (import.meta.env.PROD) {
          // Use precompiled css files while in production mode
          stylesheet.setAttribute("href", `/assets/${theme}.css`);
        } else {
          // Use sass files while in development mode, so we can watch changes while developing
          stylesheet.setAttribute("href", `/src/assets/scss/${theme}.scss`);
        }
      }
    }
  }, [value, key]);

  return [value, setValue];
}

export default useSettingsState;
