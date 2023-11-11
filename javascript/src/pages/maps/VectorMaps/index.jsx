import React from "react";
import { Helmet } from "react-helmet-async";
import { Col, Container, Row, Card } from "react-bootstrap";

import World from "./World";
import USA from "./USA";

const VectorMaps = () => (
  <React.Fragment>
    <Helmet title="Vector Maps" />
    <Container fluid className="p-0">
      <h1 className="h3 mb-3">Vector Maps</h1>

      <Card>
        <Card.Header>
          <Card.Title className="mb-0">Jsvectormap</Card.Title>
        </Card.Header>
        <Card.Body className="pt-0">
          <p className="mb-0">
            A JavaScript library for creating interactive maps.{" "}
            <a
              href="https://github.com/kadoshms/react-jvectormap"
              target="_blank"
              rel="nofollow noreferrer"
            >
              Documentation & map downloads
            </a>
            .
          </p>
        </Card.Body>
      </Card>
      <Row>
        <Col lg="6">
          <World />
        </Col>
        <Col lg="6">
          <USA />
        </Col>
      </Row>
    </Container>
  </React.Fragment>
);

export default VectorMaps;
