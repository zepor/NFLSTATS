import React, { useEffect, useState } from "react";
import jsVectorMap from "jsvectormap";
import { Card } from "react-bootstrap";

import usePalette from "../../../hooks/usePalette";

function World() {
  const palette = usePalette();
  const [debounced, setDebounced] = useState(false);

  // Workaround, so vector maps work properly in dark mode
  useEffect(() => {
    setTimeout(() => {
      setDebounced(true);
    }, 100);
  }, []);

  useEffect(() => {
    if (debounced) {
      new jsVectorMap({
        selector: "#maps_world",
        map: "world",
        regionStyle: {
          initial: {
            fill: palette["gray-200"],
          },
        },
        backgroundColor: "transparent",
        containerStyle: {
          width: "100%",
          height: "100%",
        },
        zoomOnScroll: false,
      });
    }
  }, [debounced, palette]);

  return (
    <Card>
      <Card.Header>
        <Card.Title className="mb-0">World Map</Card.Title>
      </Card.Header>
      <Card.Body>
        <div className="map-container" style={{ height: 300 }}>
          <div id="maps_world" />
        </div>
      </Card.Body>
    </Card>
  );
}

export default World;
