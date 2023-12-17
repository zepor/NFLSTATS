import React from "react";

const TeamOption = ({ teamName, onSelect, logoPath }) => {
  return (
    <div onClick={onSelect} className="team-option">
      <img src={logoPath} alt={teamName} />
      <span>{teamName}</span>
    </div>
  );
};

export default TeamOption;
