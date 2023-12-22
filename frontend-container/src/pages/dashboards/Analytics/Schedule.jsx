import React, { useState, useEffect } from "react";

function GamesSchedule(props) {
  const [graphql, setGraphql] = useState(null);

  useEffect(() => {
    fetch(
      "https://cdn.builder.codes/api/v1/proxy-api?url=https%3A%2F%2Fcurrent--loveofsports.apollographos.net%2Fgraphql",
    )
      .then((res) => res.json())
      .then((result) => {
        setGraphql(result);
      });
  }, []);

  return (
    <div>
      <header className="header">NFL Games Schedule</header>
      <section>
        <div
          css={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit,minmax(150px,1fr))",
            gap: "20px",
            marginTop: "20px",
          }}
          role="grid"
          aria-label="Games Schedule"
        ></div>
      </section>
    </div>
  );
}

export default GamesSchedule;
