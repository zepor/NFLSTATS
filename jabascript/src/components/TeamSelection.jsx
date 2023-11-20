import React, { useContext, useState } from "react";
import ThemeContext from "../contexts/ThemeContext";
import * as Constants from "../constants";
import TeamOption from "./TeamOption";

const TeamSelector = () => {
  const { theme, setTheme } = useContext(ThemeContext);
  const [selectedTeam, setSelectedTeam] = useState(null);

  const handleTeamSelect = (teamName) => {
    setSelectedTeam(teamName);
    setTheme(teamName); // Set the selected team in the context

    // Set the theme colors
    document.documentElement.style.setProperty(
      "--primary-color",
      Constants[teamName]["primary-dark"]
    );
    document.documentElement.style.setProperty(
      "--secondary-color",
      Constants[teamName]["primary-light"]
    );
  };

  // Additional logic to handle different styles for dev and prod environments
  useEffect(() => {
    const stylesheet = document.querySelector(".js-stylesheet");
    if (stylesheet) {
      if (import.meta.env.PROD) {
        stylesheet.setAttribute("href", `/assets/${theme}.css`);
      } else {
        stylesheet.setAttribute("href", `/src/assets/scss/${theme}.scss`);
      }
    }
  }, [theme]);

  return (
    <div>
      <h3>Select Your NFL Team</h3>
      <div className="custom-dropdown">
        {Object.keys(Constants)
          .filter(
            (key) =>
              key !== "THEME_PALETTE_LIGHT" && key !== "THEME_PALETTE_DARK"
          )
          .map((teamName) => (
            <TeamOption
              key={teamName}
              teamName={teamName}
              logoPath={`/assets/img/teamlogos/${teamName
                .toLowerCase()
                .replace(/ /g, "-")}.png`}
              onSelect={() => handleTeamSelect(teamName)}
            />
          ))}
      </div>

      {/* Display selected team's colors */}
      {selectedTeam && (
        <div style={{backgroundColor: Constants[selectedTeam]["primary-dark"],
            color: Constants[selectedTeam]["primary-light"],
          }}><h4>Selected Team:{selectedTeam}</h4>Team Colors</div>)}</div>
  );
};

export default TeamSelector;
