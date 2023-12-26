// SignUpPage.js
import React, { useState } from "react";
import { Helmet } from "react-helmet-async";
import { Card, Button } from "react-bootstrap";
import SignUpModal from "./SignUpModal"; // Import the SignUpModal component

const SignUpPage = () => {
  const [showSignUpModal, setShowSignUpModal] = useState(false);

  const handleSignUpClick = () => setShowSignUpModal(true);
  const handleCloseSignUpModal = () => setShowSignUpModal(false);

  return (
    <React.Fragment>
      <Helmet title="Sign Up" />
      <div className="text-center mt-4">
        <h1 className="h2">Get started</h1>
        <p className="lead">
          Start creating the best possible user experience for your customers.
        </p>
      </div>

      <Card>
        <Card.Body>
          <div className="m-sm-3">
            <Button onClick={handleSignUpClick}>Sign Up</Button>
            <SignUpModal
              show={showSignUpModal}
              onHide={handleCloseSignUpModal}
            />
          </div>
        </Card.Body>
      </Card>
    </React.Fragment>
  );
};

export default SignUpPage;
