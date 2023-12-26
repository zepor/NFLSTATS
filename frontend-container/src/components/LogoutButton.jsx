import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { ListGroup, Row, Col } from "react-bootstrap";
import { LogOut } from "react-feather"; // Assuming you are using react-feather for icons

const LogoutButton = () => {
  const { logout } = useAuth0();

  return (
    <ListGroup.Item
      action
      onClick={() =>
        logout({ logoutParams: { returnTo: window.location.origin } })
      }
      className="d-flex align-items-center"
    >
      <Row className="align-items-center g-0 w-100">
        <Col xs={2}>
          <LogOut size={18} className="align-middle" /> {/* Icon */}
        </Col>
        <Col xs={10} className="pl-2">
          <div className="text-dark">Log Out</div> {/* Title */}
          {/* Add description or time if needed */}
        </Col>
      </Row>
    </ListGroup.Item>
  );
};

export default LogoutButton;
