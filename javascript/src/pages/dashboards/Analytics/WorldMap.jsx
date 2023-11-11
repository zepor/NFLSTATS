import React, { useEffect, useState } from "react";
import jsVectorMap from "jsvectormap";
import { Card, Dropdown } from "react-bootstrap";
import { MoreHorizontal } from "react-feather";

import usePalette from "../../../hooks/usePalette";

function WorldMap() {
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
        selector: "#analytics_world",
        map: "world",
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
            coords: [31.230391, 121.473701],
            name: "Shanghai",
          },
          {
            coords: [39.904202, 116.407394],
            name: "Beijing",
          },
          {
            coords: [28.70406, 77.102493],
            name: "Delhi",
          },
          {
            coords: [6.524379, 3.379206],
            name: "Lagos",
          },
          {
            coords: [39.343357, 117.361649],
            name: "Tianjin",
          },
          {
            coords: [24.860735, 67.001137],
            name: "Karachi",
          },
          {
            coords: [41.00824, 28.978359],
            name: "Istanbul",
          },
          {
            coords: [35.689487, 139.691711],
            name: "Tokyo",
          },
          {
            coords: [23.12911, 113.264381],
            name: "Guangzhou",
          },
          {
            coords: [19.075983, 72.877655],
            name: "Mumbai",
          },
          {
            coords: [40.7127837, -74.0059413],
            name: "New York",
          },
          {
            coords: [34.052235, -118.243683],
            name: "Los Angeles",
          },
          {
            coords: [41.878113, -87.629799],
            name: "Chicago",
          },
          {
            coords: [29.760427, -95.369804],
            name: "Houston",
          },
          {
            coords: [33.448376, -112.074036],
            name: "Phoenix",
          },
          {
            coords: [51.507351, -0.127758],
            name: "London",
          },
          {
            coords: [48.856613, 2.352222],
            name: "Paris",
          },
          {
            coords: [55.755825, 37.617298],
            name: "Moscow",
          },
          {
            coords: [40.416775, -3.70379],
            name: "Madrid",
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
        <Card.Title className="mb-0">Real-Time</Card.Title>
      </Card.Header>
      <Card.Body className="p-2">
        <div className="map-container" style={{ height: 279 }}>
          <div id="analytics_world" />
        </div>
      </Card.Body>
    </Card>
  );
}

export default WorldMap;
