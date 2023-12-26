// SignInPage.js
import React, { useState } from "react";
import { Helmet } from "react-helmet-async";
import { Card, Button } from "react-bootstrap";
import SignInModal from "./SignInModal"; // Import the SignInModal component

const SignInPage = () => {
  const [showSignInModal, setShowSignInModal] = useState(false);

  const handleSignInClick = () => setShowSignInModal(true);
  const handleCloseSignInModal = () => setShowSignInModal(false);

  return (
    <React.Fragment>
      <Helmet title="Sign In" />
      <div className="text-center mt-4">
        <h2>Welcome back!</h2>
        <p className="lead">Sign in to your account to continue</p>
      </div>

      <Card>
        <Card.Body>
          <div className="m-sm-3">
            <Button onClick={handleSignInClick}>Sign In</Button>
            <SignInModal
              show={showSignInModal}
              onHide={handleCloseSignInModal}
            />
          </div>
        </Card.Body>
      </Card>
    </React.Fragment>
  );
};

export default SignInPage;
