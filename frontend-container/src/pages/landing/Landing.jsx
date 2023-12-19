import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  Accordion,
  Badge,
  Button,
  Card,
  Col,
  Container,
  Nav,
  Navbar,
  Row,
  Tooltip,
  OverlayTrigger,
} from "react-bootstrap";
//import {
//  Code,
//  DownloadCloud,
//  Mail,
//  Sliders,
//  Smartphone,
//  Users,
//} from "react-feather";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faPalette,
  faStar,
  faChartLine,
  faFootballBall,
  faClipboardList,
  faHistory,
  faChartBar,
  faDesktop,
} from "@fortawesome/free-solid-svg-icons";

import {
  SIDEBAR_POSITION,
  SIDEBAR_BEHAVIOR,
  LAYOUT,
  THEME,
} from "../../constants";
import { useTheme } from "../../hooks/useTheme";
import useSidebar from "../../hooks/useSidebar";
import useLayout from "../../hooks/useLayout";

//import { ReactComponent as Logo } from "../../assets/img/logo.svg";
//import screenshotMixed from "../../assets/img/screenshots/mixed.jpg";
//import screenshotThemeDefault from "../../assets/img/screenshots/theme-default.jpg";
//import screenshotThemeDark from "../../assets/img/screenshots/theme-dark.jpg";
//import screenshotThemeColored from "../../assets/img/screenshots/theme-colored.jpg";
//import screenshotThemeLight from "../../assets/img/screenshots/theme-light.jpg";
//import screenshotSidebarCompact from "../../assets/img/screenshots/sidebar-compact.jpg";
//import screenshotSidebarRight from "../../assets/img/screenshots/sidebar-right.jpg";
import screenshotFootballAnalytics from "../../assets/img/photos/screenshot-football-analytics.png";
import nflDataLogo from "../../assets/img/photos/nfl-data-logo.png";
import userAvatar1 from "../../assets/img/avatars/avatar-1.jpg";
import screenshotPlayerStats from "../../assets/img/photos/screenshot-player-stats.png";
import screenshotTeamStats from "../../assets/img/photos/screenshot-team-stats.png";
import screenshotGameAnalysis from "../../assets/img/photos/screenshot-game-analysis.png";
import nflScreenshotDefault from "../../assets/img/photos/nfl-screenshot-default.png";
import nflScreenshotCompact from "../../assets/img/photos/nfl-screenshot-compact.png";
//import nflScreenshotDark from "../../assets/img/photos/nfl-screenshot-dark.png";
//import nflScreenshotColored from "../../assets/img/photos/nfl-screenshot-colored.png";
//import nflScreenshotLight from "../../assets/img/photos/nfl-screenshot-light.png";
//import nflScreenshotRightSidebar from "../../assets/img/photos/nfl-screenshot-right-sidebar.png";

//import screenshotDashboardDefault from "../../assets/img/screenshots/dashboard-default.jpg";
//import screenshotDashboardAnalytics from "../../assets/img/screenshots/dashboard-analytics.jpg";
//import screenshotDashboardSaaS from "../../assets/img/screenshots/dashboard-saas.jpg";
//import screenshotDashboardSocial from "../../assets/img/screenshots/dashboard-social.jpg";
//import screenshotDashboardCrypto from "../../assets/img/screenshots/dashboard-crypto.jpg";
//import screenshotPageProjects from "../../assets/img/screenshots/pages-projects-list.jpg";
import screenshotDashboard4 from "../../assets/img/photos/screenshot-dashboard-4.png";
import screenshotDashboard5 from "../../assets/img/photos/screenshot-dashboard-5.png";
import screenshotDashboard6 from "../../assets/img/photos/screenshot-dashboard-6.png";

//import brandBootstrap from "../../assets/img/brands/bootstrap.svg";
//import brandReact from "../../assets/img/brands/react.svg";
//import brandRedux from "../../assets/img/brands/redux.svg";
//import brandReactRouter from "../../assets/img/brands/react-router.svg";
//import brandFirebase from "../../assets/img/brands/firebase.svg";
//import brandCognito from "../../assets/img/brands/cognito.svg";
//import brandAuth0 from "../../assets/img/brands/auth0.svg";
//import brandJWT from "../../assets/img/brands/jwt.svg";
//import brandESLint from "../../assets/img/brands/eslint.svg";
//import brandJavaScript from "../../assets/img/brands/javascript.svg";
//import brandTypeScript from "../../assets/img/brands/typescript.svg";
import logo from "../../assets/img/logo.svg";
import FBIcon from "../../assets/img/brands/faFacebook.svg";
import INSTAIcon from "../../assets/img/brands/faInstagram.svg";
import TWIcon from "../../assets/img/brands/faTwitter.svg";
import LINKIcon from "../../assets/img/brands/faLinkedin.svg";

import TeamSelector from "../../components/TeamSelection";

const Navigation = () => {
  return (
    <Navbar expand="lg" bg="dark" variant="dark" className="py-3">
      <Container>
        <Navbar.Brand href="/">
          <img
            src={logo}
            width="30"
            height="30"
            className="d-inline-block align-top"
            alt="LoveofFootball.io Logo"
          />
          LoveofFootball.io
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto">
            <Nav.Link href="/analytics">Analytics</Nav.Link>
            <Nav.Link href="/fantasy-draft">Fantasy Draft</Nav.Link>
            <Nav.Link href="/predictions">Predictions</Nav.Link>
            <Nav.Link href="/player-comparison">Player Comparison</Nav.Link>
            <Nav.Link href="/about">About Us</Nav.Link>
            <Nav.Link href="mailto:support@loveoffootball.io">Support</Nav.Link>
          </Nav>
          <div className="auth-buttons ms-3">
            <Link to="/auth/sign-in" className="btn btn-outline-light me-2">
              Sign In
            </Link>
            <Link to="/auth/sign-up" className="btn btn-success">
              Get Started
            </Link>
          </div>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

const Intro = () => (
  <section className="landing-intro pt-5 pt-lg-6 pb-5 pb-lg-7">
    <Container className="landing-intro-content">
      <Row className="align-items-center">
        <Col lg="5" className="mx-auto text-center text-lg-start">
          <h1 className="display-4 font-weight-bold my-4">
            Elevate Your Game with{" "}
            <span className="text-primary">LoveofFootball.io</span>
          </h1>
          <p className="text-lg lead">
            Dive into the world of football analytics and unlock powerful
            insights for fantasy football success and strategic betting.
          </p>
          <p className="mb-4">
            Our platform brings you real-time data, in-depth player analysis,
            and predictive modeling to give you an unmatched advantage.
          </p>
          <div>
            <Link
              to="/features"
              className="btn btn-primary btn-pill btn-lg me-2"
            >
              Explore Features
            </Link>
            <Link to="/signup" className="btn btn-success btn-pill btn-lg">
              Start Winning Now
            </Link>
          </div>
        </Col>
        <Col lg="7" className="d-none d-lg-flex mx-auto text-center">
          {/* Replace with a relevant fantasy football analytics dashboard image */}
          <img
            src={screenshotFootballAnalytics}
            alt="Football Analytics Dashboard"
            className="img-fluid rounded shadow"
          />
        </Col>
      </Row>
    </Container>
  </section>
);

const ColorSchemesAndLayouts = () => (
  <section className="py-6 bg-white" id="design-options">
    <Container className="position-relative z-3">
      <Row>
        <Col md="12" className="mx-auto text-center">
          <Row>
            <div className="col-lg-10 col-xl-9 mx-auto">
              <div className="mb-4">
                <span className="text-uppercase text-primary text-sm fw-medium mb-1 d-block">
                  Design Options
                </span>
                <h2 className="h1 mb-3">
                  Choose Your Color Scheme &amp; Layout
                </h2>
                <p className="text-muted fs-lg">
                  Customize the look and feel of your NFL statistics platform
                  with various color schemes and layouts. You have the
                  flexibility to create a unique design that suits your
                  preferences.
                </p>
              </div>
            </div>
          </Row>

          <Row>
            <Col md="4" className="py-3">
              <Link
                className="d-block mb-3 mx-1"
                target="_blank"
                rel="noreferrer"
                to="/design/default?theme=default"
              >
                <div className="landing-feature">
                  <FontAwesomeIcon icon={faPalette} />
                </div>
                <img
                  src={nflScreenshotDefault}
                  className="img-fluid rounded-lg landing-img"
                  alt="Default Design Option"
                />
              </Link>
              <h4>Default</h4>
            </Col>
            <Col md="4" className="py-3">
              <Link
                className="d-block mb-3 mx-1"
                target="_blank"
                rel="noreferrer"
                to="/design/default?sidebarBehavior=compact"
              >
                <div className="landing-feature">
                  <FontAwesomeIcon icon={faPalette} />
                </div>
                <img
                  src={nflScreenshotCompact}
                  className="img-fluid rounded-lg landing-img"
                  alt="Compact Sidebar NFL Statistics Dashboard"
                />
              </Link>
              <h4>
                Compact sidebar{" "}
                <sup>
                  <Badge as="small" bg="primary">
                    New
                  </Badge>
                </sup>
              </h4>
            </Col>
            {/* Add more design options with relevant links and screenshots */}
            {/* ... */}
          </Row>
        </Col>
      </Row>
    </Container>
  </section>
);

const Integrations = () => (
  <section className="pt-6">
    <Container>
      <Row>
        <Col md="10" className="mx-auto text-center">
          <div className="mb-5">
            <span className="text-uppercase text-primary text-sm fw-medium mb-1 d-block">
              Integrations
            </span>
            <h2 className="h1">
              Launch faster with ready-to-deploy integrations
            </h2>
            <p className="text-muted fs-lg">
              Our NFL Statistics Analytics platform includes multiple
              ready-to-deploy integrations, making it easy for you to access
              real-time data, player statistics, and game insights.
            </p>

            <div className="my-4">
              {/* Replace with actual integration logos and tooltips */}
              <OverlayTrigger
                placement="bottom"
                overlay={<Tooltip>NFL Data API</Tooltip>}
              >
                <div className="landing-integration">
                  <img src={nflDataLogo} alt="NFL Data API" />
                </div>
              </OverlayTrigger>
              {/* Add more integrations here */}
            </div>

            <Button
              variant="primary"
              size="lg"
              as="a"
              href="/docs/integration"
              target="_blank"
              rel="noreferrer"
            >
              Explore Integrations
            </Button>
          </div>
        </Col>
      </Row>
    </Container>
  </section>
);

const Testimonials = () => (
  <section className="py-6">
    <Container>
      <div className="mb-5 text-center">
        <span className="text-uppercase text-primary text-sm fw-medium mb-1 d-block">
          Reviews
        </span>
        <h2 className="h1">Users love our NFL Statistics Analytics</h2>
        <p className="text-muted fs-lg">
          See what some of our satisfied users have to say about the valuable
          insights they've gained from our platform.
        </p>
      </div>
      <Row>
        <Col md="6" lg="4">
          <Card as="blockquote" className="landing-quote border">
            <Card.Body className="p-4">
              <div className="d-flex align-items-center mb-3">
                {/* Replace with user avatar */}
                <div>
                  <img src={userAvatar1} width="48" height="48" alt="User 1" />
                </div>
                <div className="ps-3">
                  <h5 className="mb-1 mt-2">John Doe</h5>
                  <small className="d-block text-muted h5 fw-normal">
                    NFL Analyst
                  </small>
                </div>
              </div>
              <p className="lead mb-2">
                "The NFL Statistics Analytics platform has revolutionized the
                way I analyze games. The in-depth player statistics and
                historical data are incredibly valuable for making informed
                predictions."
              </p>

              <div className="landing-stars">
                <FontAwesomeIcon icon={faStar} />
                <FontAwesomeIcon icon={faStar} />
                <FontAwesomeIcon icon={faStar} />
                <FontAwesomeIcon icon={faStar} />
                <FontAwesomeIcon icon={faStar} />
              </div>
            </Card.Body>
          </Card>
        </Col>
        {/* Add more testimonials here */}
      </Row>
    </Container>
  </section>
);

const DashboardsAndPages = () => (
  <section className="py-6 bg-white" id="demos">
    <Container className="position-relative z-3">
      <Row>
        <Col md="12" className="mx-auto text-center">
          <Row>
            <div className="col-lg-10 col-xl-9 mx-auto">
              <div className="mb-4">
                <span className="text-uppercase text-primary text-sm fw-medium mb-1 d-block">
                  Demos
                </span>
                <h2 className="h1 mb-3">
                  Explore our NFL Statistics Dashboards
                </h2>
                <p className="text-muted fs-lg">
                  Discover the power of our analytics with various NFL
                  statistics dashboards and pages. Dive deep into player
                  performance, team stats, and game analysis. Get real-time
                  insights to stay ahead in the game.
                </p>
              </div>
            </div>
          </Row>

          <Row>
            {/* NFL Player Stats Dashboard */}
            <Col md="4" className="py-3">
              <Link
                className="d-block mb-3 mx-1"
                target="_blank"
                rel="noreferrer"
                to="/dashboard/player-stats"
              >
                <img
                  src={screenshotPlayerStats}
                  className="img-fluid rounded-lg landing-img"
                  alt="NFL Player Stats Dashboard"
                />
              </Link>
              <h4>NFL Player Stats</h4>
              <p className="text-muted fs-lg">
                Dive into detailed player statistics, including performance
                metrics, historical data, and player comparisons. Stay informed
                about your favorite NFL players' performance.
              </p>
            </Col>

            {/* NFL Team Stats Dashboard */}
            <Col md="4" className="py-3">
              <Link
                className="d-block mb-3 mx-1"
                target="_blank"
                rel="noreferrer"
                to="/dashboard/team-stats"
              >
                <img
                  src={screenshotTeamStats}
                  className="img-fluid rounded-lg landing-img"
                  alt="NFL Team Stats Dashboard"
                />
              </Link>
              <h4>NFL Team Stats</h4>
              <p className="text-muted fs-lg">
                Explore comprehensive team statistics, including win-loss
                records, offensive and defensive performance, and more. Analyze
                team strategies and trends.
              </p>
            </Col>

            {/* NFL Game Analysis Dashboard */}
            <Col md="4" className="py-3">
              <Link
                className="d-block mb-3 mx-1"
                target="_blank"
                rel="noreferrer"
                to="/dashboard/game-analysis"
              >
                <img
                  src={screenshotGameAnalysis}
                  className="img-fluid rounded-lg landing-img"
                  alt="NFL Game Analysis Dashboard"
                />
              </Link>
              <h4>NFL Game Analysis</h4>
              <p className="text-muted fs-lg">
                Get in-depth game analysis with real-time data. Analyze game
                performance, key plays, and player contributions. Stay ahead
                with data-driven insights.
              </p>
            </Col>

            {/* Additional NFL Statistics Dashboards */}
            {/* Dashboard 4 */}
            <Col md="4" className="py-3">
              {/* Add Link and Image for Dashboard 4 */}
              <Link
                className="d-block mb-3 mx-1"
                target="_blank"
                rel="noreferrer"
                to="/dashboard/dashboard-4"
              >
                <img
                  src={screenshotDashboard4}
                  className="img-fluid rounded-lg landing-img"
                  alt="NFL Dashboard 4"
                />
              </Link>
              <h4>NFL Dashboard 4</h4>
              {/* Add Description for Dashboard 4 */}
              <p className="text-muted fs-lg">
                Description for NFL Dashboard 4. Customize this text.
              </p>
            </Col>

            {/* Dashboard 5 */}
            <Col md="4" className="py-3">
              {/* Add Link and Image for Dashboard 5 */}
              <Link
                className="d-block mb-3 mx-1"
                target="_blank"
                rel="noreferrer"
                to="/dashboard/dashboard-5"
              >
                <img
                  src={screenshotDashboard5}
                  className="img-fluid rounded-lg landing-img"
                  alt="NFL Dashboard 5"
                />
              </Link>
              <h4>NFL Dashboard 5</h4>
              {/* Add Description for Dashboard 5 */}
              <p className="text-muted fs-lg">
                Description for NFL Dashboard 5. Customize this text.
              </p>
            </Col>

            {/* Dashboard 6 */}
            <Col md="4" className="py-3">
              {/* Add Link and Image for Dashboard 6 */}
              <Link
                className="d-block mb-3 mx-1"
                target="_blank"
                rel="noreferrer"
                to="/dashboard/dashboard-6"
              >
                <img
                  src={screenshotDashboard6}
                  className="img-fluid rounded-lg landing-img"
                  alt="NFL Dashboard 6"
                />
              </Link>
              <h4>NFL Dashboard 6</h4>
              {/* Add Description for Dashboard 6 */}
              <p className="text-muted fs-lg">
                Description for NFL Dashboard 6. Customize this text.
              </p>
            </Col>
          </Row>
        </Col>
      </Row>
    </Container>
  </section>
);

const Features = () => (
  <section className="py-6" id="features">
    <Container>
      <Row>
        <Col md="10" className="mx-auto text-center">
          <div className="mb-5">
            <h2 className="h1">Powerful Analytics for Football Enthusiasts</h2>
            <p className="text-muted text-lg">
              From player statistics to advanced team analysis, our platform
              offers all the tools you need for a successful season.
            </p>
          </div>

          <Row className="text-start">
            {/* Advanced Performance Metrics */}
            <Col md="6">
              <div className="d-flex py-3">
                <div className="landing-feature">
                  <FontAwesomeIcon icon={faChartLine} />
                </div>
                <div className="flex-grow-1">
                  <h4 className="mt-0">Advanced Performance Metrics</h4>
                  <p className="fs-lg">
                    Dive into comprehensive player performance metrics and
                    utilize advanced stats to make smart decisions. Track player
                    progress throughout the season.
                  </p>
                </div>
              </div>
            </Col>

            {/* Team Analysis */}
            <Col md="6">
              <div className="d-flex py-3">
                <div className="landing-feature">
                  <FontAwesomeIcon icon={faFootballBall} />
                </div>
                <div className="flex-grow-1">
                  <h4 className="mt-0">Team Analysis Tools</h4>
                  <p className="fs-lg">
                    Analyze team strategies, strengths, and weaknesses with our
                    team-focused analytics. Gain insights into win-loss records,
                    offensive and defensive performance, and more.
                  </p>
                </div>
              </div>
            </Col>

            {/* Game Insights */}
            <Col md="6">
              <div className="d-flex py-3">
                <div className="landing-feature">
                  <FontAwesomeIcon icon={faClipboardList} />
                </div>
                <div className="flex-grow-1">
                  <h4 className="mt-0">In-Depth Game Insights</h4>
                  <p className="fs-lg">
                    Get real-time game analysis with key play breakdowns, player
                    contributions, and game-changing moments. Stay ahead with
                    data-driven insights during every match.
                  </p>
                </div>
              </div>
            </Col>

            {/* Historical Data */}
            <Col md="6">
              <div className="d-flex py-3">
                <div className="landing-feature">
                  <FontAwesomeIcon icon={faHistory} />
                </div>
                <div className="flex-grow-1">
                  <h4 className="mt-0">Historical Data Repository</h4>
                  <p className="fs-lg">
                    Access a rich historical data repository to compare past
                    seasons, players, and teams. Make informed decisions based
                    on historical trends.
                  </p>
                </div>
              </div>
            </Col>

            {/* Data Visualization */}
            <Col md="6">
              <div className="d-flex py-3">
                <div className="landing-feature">
                  <FontAwesomeIcon icon={faChartBar} />
                </div>
                <div className="flex-grow-1">
                  <h4 className="mt-0">Data Visualization</h4>
                  <p className="fs-lg">
                    Visualize complex statistics with interactive charts and
                    graphs. Understand data at a glance and share insights with
                    your team and fans.
                  </p>
                </div>
              </div>
            </Col>

            {/* User-Friendly Interface */}
            <Col md="6">
              <div className="d-flex py-3">
                <div className="landing-feature">
                  <FontAwesomeIcon icon={faDesktop} />
                </div>
                <div className="flex-grow-1">
                  <h4 className="mt-0">User-Friendly Interface</h4>
                  <p className="fs-lg">
                    Our intuitive and easy-to-use interface ensures that both
                    beginners and experts can navigate and utilize our analytics
                    tools effectively.
                  </p>
                </div>
              </div>
            </Col>
          </Row>
        </Col>
      </Row>
    </Container>
  </section>
);

const Faq = () => {
  const [activeKey, setActiveKey] = useState("0");

  return (
    <section className="bg-white py-6">
      <Container>
        <div className="mb-5 text-center">
          <span className="text-uppercase text-primary text-sm fw-medium mb-1 d-block">
            LoveofFootball.io
          </span>
          <h2 className="h1">Frequently Asked Questions</h2>
          <p className="text-muted fs-lg">
            Here are some of the answers you might be looking for regarding our
            NFL statistics platform.
          </p>
        </div>
        <Row>
          <Col md={9} lg={8} className="mx-auto">
            <Accordion activeKey={activeKey}>
              <Card className="border mb-3">
                <Card.Header
                  className="cursor-pointer"
                  onClick={() => setActiveKey("0")}
                >
                  <h6 className="mb-0">How do I access player statistics?</h6>
                </Card.Header>
                <Accordion.Collapse eventKey="0">
                  <Card.Body className="py-3">
                    You can access player statistics by navigating to the
                    "Player Stats" dashboard on our platform. There, you'll find
                    detailed information about individual players' performance.
                  </Card.Body>
                </Accordion.Collapse>
              </Card>
              <Card className="border mb-3">
                <Card.Header
                  className="cursor-pointer"
                  onClick={() => setActiveKey("1")}
                >
                  <h6 className="mb-0">What team statistics are available?</h6>
                </Card.Header>
                <Accordion.Collapse eventKey="1">
                  <Card.Body className="py-3">
                    Our platform provides comprehensive team statistics,
                    including offensive and defensive performance, win-loss
                    records, player rosters, and more. You can explore these
                    statistics in the "Team Stats" dashboard.
                  </Card.Body>
                </Accordion.Collapse>
              </Card>
              <Card className="border mb-3">
                <Card.Header
                  className="cursor-pointer"
                  onClick={() => setActiveKey("2")}
                >
                  <h6 className="mb-0">How can I analyze past games?</h6>
                </Card.Header>
                <Accordion.Collapse eventKey="2">
                  <Card.Body className="py-3">
                    To analyze past games, you can use our "Game Analysis"
                    dashboard. It provides in-depth insights into historical
                    games, key plays, and game-changing moments. You can review
                    game statistics, player performances, and more.
                  </Card.Body>
                </Accordion.Collapse>
              </Card>
              <Card className="border mb-3">
                <Card.Header
                  className="cursor-pointer"
                  onClick={() => setActiveKey("3")}
                >
                  <h6 className="mb-0">Can I compare player statistics?</h6>
                </Card.Header>
                <Accordion.Collapse eventKey="3">
                  <Card.Body className="py-3">
                    Yes, our platform allows you to compare player statistics.
                    You can select multiple players and view their performance
                    metrics side by side in the "Player Stats" dashboard. This
                    feature helps you make informed decisions and comparisons.
                  </Card.Body>
                </Accordion.Collapse>
              </Card>
              <Card className="border mb-3">
                <Card.Header
                  className="cursor-pointer"
                  onClick={() => setActiveKey("4")}
                >
                  <h6 className="mb-0">How often are statistics updated?</h6>
                </Card.Header>
                <Accordion.Collapse eventKey="4">
                  <Card.Body className="py-3">
                    Our statistics are updated regularly to provide you with the
                    most current data. Player statistics are typically updated
                    after each game, and team statistics are updated after each
                    match. We strive to ensure that you have access to the
                    latest insights.
                  </Card.Body>
                </Accordion.Collapse>
              </Card>
            </Accordion>

            {/* Add more football-related FAQ items */}
            {/* ... */}
          </Col>
        </Row>
      </Container>
    </section>
  );
};

const Footer = () => (
  <section className="landing-footer py-6">
    <Container className="text-center landing-footer-container">
      <Row>
        <Col md="9" lg="8" xl="6" className="mx-auto">
          <h2 className="h1 mb-3">Stay Connected with Us</h2>
          <p className="text-muted text-lg">
            Join the NFL analytics community and stay up-to-date with the latest
            insights, statistics, and news.
          </p>
          <Button
            variant="success"
            size="lg"
            href="/auth/signup"
            target="_blank"
            rel="noopener noreferrer"
            className="mt-n1 btn-pill"
          >
            Get LoveofFootball.io
          </Button>
          {/* Add social media links or newsletter signup here */}
          <div>
            <img src={FBIcon} alt="Facebook" width="30" height="30" />
            <img src={INSTAIcon} alt="Instagram" width="30" height="30" />
            <img src={TWIcon} alt="Twitter" width="30" height="30" />
            <img src={LINKIcon} alt="Linkedin" width="30" height="30" />
          </div>
        </Col>
      </Row>
    </Container>
  </section>
);

const Landing = () => {
  const { setTheme } = useTheme();
  const { setPosition, setBehavior } = useSidebar();
  const { setLayout } = useLayout();

  useEffect(() => {
    setTheme(THEME.DEFAULT);
    setPosition(SIDEBAR_POSITION.LEFT);
    setBehavior(SIDEBAR_BEHAVIOR.STICKY);
    setLayout(LAYOUT.FLUID);
  }, []);

  return (
    <React.Fragment>
      <Navigation />
      <Intro />
      <section className="team-selector-section">
        <TeamSelector />
      </section>
      <DashboardsAndPages />
      <Features />
      <ColorSchemesAndLayouts />
      <Integrations />
      <Testimonials />
      <Faq />
      <Footer />
    </React.Fragment>
  );
};
export default Landing;
