import React from "react";
import { Card, Dropdown } from "react-bootstrap";

import { MoreHorizontal } from "react-feather";

import DT from "react-datetime";

const DateTime = DT.default ? DT.default : DT;

const Calendar = () => (
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
      <Card.Title className="mb-0">Calendar</Card.Title>
    </Card.Header>
    <Card.Body className="d-flex">
      <div className="align-self-center w-100">
        <DateTime
          input={false}
          defaultValue={DateTime.moment()}
          dateFormat="L"
          timeFormat={false}
        />
      </div>
    </Card.Body>
  </Card>
);

export default Calendar;
