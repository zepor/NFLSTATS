import React, { useContext, useState } from "react";
import ThemeContext from "../contexts/ThemeContext";
import * as Constants from "../constants";
import { Carousel, Button, Card, Row, Col, Container } from "react-bootstrap";

import bearsFans from "../assets/img/fans/bearsfans.png";
import bengalsFans from "../assets/img/fans/bengalsfans.png";
import billsFans from "../assets/img/fans/billsfans.png";
import broncosFans from "../assets/img/fans/broncosfans.png";
import brownsFans from "../assets/img/fans/brownsfans.png";
import buccaneersFans from "../assets/img/fans/buccaneersfans.png";
import cardinalsFans from "../assets/img/fans/cardinalsfans.png";
import chargersFans from "../assets/img/fans/chargersfans.png";
import chiefsFans from "../assets/img/fans/chiefsfans.png";
import coltsFans from "../assets/img/fans/coltsfans.png";
import commandersFans from "../assets/img/fans/commandersfans.png";
import cowboysFans from "../assets/img/fans/cowboysfans.png";
import dolphinsFans from "../assets/img/fans/dolphinsfans.png";
import eaglesFans from "../assets/img/fans/eaglesfans.png";
import falconsFans from "../assets/img/fans/falconsfans.png";
import giantsFans from "../assets/img/fans/giantsfans.png";
import jaguarsFans from "../assets/img/fans/jaguarsfans.png";
import jetsFans from "../assets/img/fans/jetsfans.png";
import lionsFans from "../assets/img/fans/lionsfans.png";
import ninersFans from "../assets/img/fans/ninersfans.png";
import packersFans from "../assets/img/fans/packersfans.png";
import panthersFans from "../assets/img/fans/panthersfans.png";
import patriotsFans from "../assets/img/fans/patriotsfans.png";
import raidersFans from "../assets/img/fans/raidersfans.png";
import ramsFans from "../assets/img/fans/ramsfans.png";
import ravensFans from "../assets/img/fans/ravensfans.png";
import saintsFans from "../assets/img/fans/saintsfans.png";
import seahawksFans from "../assets/img/fans/seahawksfans.png";
import steelersFans from "../assets/img/fans/steelersfans.png";
import texansFans from "../assets/img/fans/texansfans.png";
import titansFans from "../assets/img/fans/titansfans.png";
import vikingsFans from "../assets/img/fans/vikingsfans.png";

import bearsLogo from "../assets/img/teamlogos/bears.png";
import bengalsLogo from "../assets/img/teamlogos/bengals.png";
import billsLogo from "../assets/img/teamlogos/bills.png";
import broncosLogo from "../assets/img/teamlogos/broncos.png";
import brownsLogo from "../assets/img/teamlogos/browns.png";
import buccaneersLogo from "../assets/img/teamlogos/buccaneers.png";
import cardinalsLogo from "../assets/img/teamlogos/cardinals.png";
import chargersLogo from "../assets/img/teamlogos/chargers.png";
import chiefsLogo from "../assets/img/teamlogos/chiefs.png";
import coltsLogo from "../assets/img/teamlogos/colts.png";
import commandersLogo from "../assets/img/teamlogos/commanders.png";
import cowboysLogo from "../assets/img/teamlogos/cowboys.png";
import dolphinsLogo from "../assets/img/teamlogos/dolphins.png";
import eaglesLogo from "../assets/img/teamlogos/eagles.png";
import falconsLogo from "../assets/img/teamlogos/falcons.png";
import giantsLogo from "../assets/img/teamlogos/giants.png";
import jaguarsLogo from "../assets/img/teamlogos/jaguars.png";
import jetsLogo from "../assets/img/teamlogos/jets.png";
import lionsLogo from "../assets/img/teamlogos/lions.png";
import ninersLogo from "../assets/img/teamlogos/niners.png";
import packersLogo from "../assets/img/teamlogos/packers.png";
import panthersLogo from "../assets/img/teamlogos/panthers.png";
import patriotsLogo from "../assets/img/teamlogos/patriots.png";
import raidersLogo from "../assets/img/teamlogos/raiders.png";
import ramsLogo from "../assets/img/teamlogos/rams.png";
import ravensLogo from "../assets/img/teamlogos/ravens.png";
import saintsLogo from "../assets/img/teamlogos/saints.png";
import seahawksLogo from "../assets/img/teamlogos/seahawks.png";
import steelersLogo from "../assets/img/teamlogos/steelers.png";
import texansLogo from "../assets/img/teamlogos/texans.png";
import titansLogo from "../assets/img/teamlogos/titans.png";
import vikingsLogo from "../assets/img/teamlogos/vikings.png";

const teamImages = {
  bears: { logo: bearsLogo, fans: bearsFans, alt: "Chicago Bears" },
  bengals: { logo: bengalsLogo, fans: bengalsFans, alt: "Cincinnati Bengals" },
  bills: { logo: billsLogo, fans: billsFans, alt: "Buffalo Bills" },
  broncos: { logo: broncosLogo, fans: broncosFans, alt: "Denver Broncos" },
  browns: { logo: brownsLogo, fans: brownsFans, alt: "Cleveland Browns" },
  buccaneers: {
    logo: buccaneersLogo,
    fans: buccaneersFans,
    alt: "Tampa Bay Buccaneers",
  },
  cardinals: {
    logo: cardinalsLogo,
    fans: cardinalsFans,
    alt: "Arizona Cardinals",
  },
  chargers: {
    logo: chargersLogo,
    fans: chargersFans,
    alt: "Los Angeles Chargers",
  },
  chiefs: { logo: chiefsLogo, fans: chiefsFans, alt: "Kansas City Chiefs" },
  colts: { logo: coltsLogo, fans: coltsFans, alt: "Indianapolis Colts" },
  commanders: {
    logo: commandersLogo,
    fans: commandersFans,
    alt: "Washington Commanders",
  },
  cowboys: { logo: cowboysLogo, fans: cowboysFans, alt: "Dallas Cowboys" },
  dolphins: { logo: dolphinsLogo, fans: dolphinsFans, alt: "Miami Dolphins" },
  eagles: { logo: eaglesLogo, fans: eaglesFans, alt: "Philadelphia Eagles" },
  falcons: { logo: falconsLogo, fans: falconsFans, alt: "Atlanta Falcons" },
  giants: { logo: giantsLogo, fans: giantsFans, alt: "New York Giants" },
  jaguars: {
    logo: jaguarsLogo,
    fans: jaguarsFans,
    alt: "Jacksonville Jaguars",
  },
  jets: { logo: jetsLogo, fans: jetsFans, alt: "New York Jets" },
  lions: { logo: lionsLogo, fans: lionsFans, alt: "Detroit Lions" },
  niners: { logo: ninersLogo, fans: ninersFans, alt: "San Francisco 49ers" },
  packers: { logo: packersLogo, fans: packersFans, alt: "Green Bay Packers" },
  panthers: {
    logo: panthersLogo,
    fans: panthersFans,
    alt: "Carolina Panthers",
  },
  patriots: {
    logo: patriotsLogo,
    fans: patriotsFans,
    alt: "New England Patriots",
  },
  raiders: { logo: raidersLogo, fans: raidersFans, alt: "Las Vegas Raiders" },
  rams: { logo: ramsLogo, fans: ramsFans, alt: "Los Angeles Rams" },
  ravens: { logo: ravensLogo, fans: ravensFans, alt: "Baltimore Ravens" },
  saints: { logo: saintsLogo, fans: saintsFans, alt: "New Orleans Saints" },
  seahawks: { logo: seahawksLogo, fans: seahawksFans, alt: "Seattle Seahawks" },
  steelers: {
    logo: steelersLogo,
    fans: steelersFans,
    alt: "Pittsburgh Steelers",
  },
  texans: { logo: texansLogo, fans: texansFans, alt: "Houston Texans" },
  titans: { logo: titansLogo, fans: titansFans, alt: "Tennessee Titans" },
  vikings: { logo: vikingsLogo, fans: vikingsFans, alt: "Minnesota Vikings" },
};

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
      document.documentElement.style.setProperty(
        "--primary-color",
        teamColors.primary,
      );
      document.documentElement.style.setProperty(
        "--secondary-color",
        teamColors.secondary,
      );
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
                {teamNames.map((teamName) => {
                  // Accessing the logo and fans images for each team
                  const { logo, fans } =
                    teamImages[teamName.toLowerCase()] || {};

                  return (
                    <Carousel.Item key={teamName}>
                      <Row className="align-items-center">
                        <Col md={6}>
                          <img
                            className="d-block w-100"
                            src={logo}
                            alt={`${teamName} logo`}
                          />
                        </Col>
                        <Col md={6}>
                          <img
                            className="d-block w-100"
                            src={fans}
                            alt={`${teamName} fans`}
                          />
                        </Col>
                      </Row>
                      <Carousel.Caption className="mt-4 text-center">
                        <Button
                          variant="primary"
                          onClick={() => confirmSelection(teamName)}
                        >
                          Select {teamName}
                        </Button>
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
