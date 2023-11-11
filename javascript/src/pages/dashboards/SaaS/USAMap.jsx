import React, { useEffect, useState } from "react";
import jsVectorMap from "jsvectormap";
import { Card, Dropdown } from "react-bootstrap";
import { MoreHorizontal } from "react-feather";

import usePalette from "../../../hooks/usePalette";

function USAMap() {
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
        selector: "#saas_usa",
        map: "us_aea_en",
        zoomOnScroll: false,
        regionStyle: {
          initial: {
            fill: palette["gray-200"],
          },
        },
        markerStyle: {
          initial: {
            r: 9,
            fill: palette.primary,
            "fill-opacity": 0.9,
            stroke: palette.white,
            "stroke-width": 7,
            "stroke-opacity": 0.4,
          },
          hover: {
            fill: palette.primary,
            "fill-opacity": 0.9,
            stroke: palette.primary,
            "stroke-width": 7,
            "stroke-opacity": 0.4,
          },
        },
        backgroundColor: "transparent",
        markers: [
          {
            coords: [37.77, -122.41],
            name: "San Francisco: 375",
          },
          {
            coords: [40.71, -74.0],
            name: "New York: 350",
          },
          {
            coords: [39.09, -94.57],
            name: "Kansas City: 250",
          },
          {
            coords: [36.16, -115.13],
            name: "Las Vegas: 275",
          },
          {
            coords: [32.77, -96.79],
            name: "Dallas: 225",
          },
        ],
      });
    }
  }, [debounced, palette]);

  return (
    <Card className="flex-fill w-100">
      <Card.Header>
        <div className="card-actions float-end">
          <Dropdown align="end">
            <Dropdown.Toggle as="a" bsPrefix="-">
              <MoreHorizontal />
            </Dropdown.Toggle>
            <Dropdown.Menu>
              <Dropdown.Item>Action</Dropdown.Item>
              <Dropdown.Item>Another Action</Dropdown.Item>
              <Dropdown.Item>Something else here</Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>
        </div>
        <Card.Title className="mb-0">Sales by State</Card.Title>
      </Card.Header>
      <Card.Body>
        <div className="map-container" style={{ height: 294 }}>
          <div id="saas_usa" />
        </div>
      </Card.Body>
    </Card>
  );
}

export default USAMap;
