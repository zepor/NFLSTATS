import React, { useContext, useState } from "react";
import ThemeContext from "../contexts/ThemeContext";
import * as Constants from "../constants";
import { Carousel, Button, Card, Row, Col, Container } from 'react-bootstrap';

const TeamSelector = () => {
  const { setTheme } = useContext(ThemeContext);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [confirmTeam, setConfirmTeam] = useState(false);

  const handleTeamSelect = (teamName) => {
    setSelectedTeam(teamName);
    setConfirmTeam(false);
  };

  const confirmSelection = (teamName) => {
    if (teamName && Constants.TEAMS[teamName]) {
      const teamColors = Constants.TEAMS[teamName];
      document.documentElement.style.setProperty('--primary-color', teamColors.primary);
      document.documentElement.style.setProperty('--secondary-color', teamColors.secondary);
      setTheme(teamName);
      setSelectedTeam(teamName);
      setConfirmTeam(true);
    }
  };

  const teamNames = Object.keys(Constants.TEAMS).sort();

  return (
    <Container className="py-5">
      <Row className="justify-content-center">
        <Col lg={8}>
          <h2 className="text-center mb-4">Select Your Favorite NFL Team</h2>
          <Card>
            <Card.Body>
              <Carousel>
                {teamNames.map(teamName => {
                  const logoPath = `/src/assets/img/teamlogos/${teamName.toLowerCase().replace(/ /g, "-")}.png`;
                  const fanPath = `/src/assets/img/fans/${teamName.toLowerCase().replace(/ /g, "")}fans.png`;

                  return (
                    <Carousel.Item key={teamName}>
                      <Row className="align-items-center">
                        <Col md={6}>
                          <img className="d-block w-100" src={logoPath} alt={`${teamName} logo`} />
                        </Col>
                        <Col md={6}>
                          <img className="d-block w-100" src={fanPath} alt={`${teamName} fans`} />
                        </Col>
                      </Row>
                      <Carousel.Caption className="mt-4 text-center">
                        <Button variant="primary" onClick={() => confirmSelection(teamName)}>Select {teamName}</Button>
                      </Carousel.Caption>
                    </Carousel.Item>
                  );
                })}
              </Carousel>
            </Card.Body>
          </Card>
          {confirmTeam && (
            <div className="text-center mt-3">
              <h4>Selected Team: {selectedTeam}</h4>
            </div>
          )}
        </Col>
      </Row>
    </Container>
  );
};

export default TeamSelector;
