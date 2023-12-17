import React from "react";
import { Helmet } from "react-helmet-async";
import { Card } from "react-bootstrap";
import { Link } from "react-router-dom";

import SignUp from "../../components/auth/SignUp";

const SignUpPage = () => (
  <React.Fragment>
    <Helmet title="Sign Up" />
    <div className="text-center mt-4">
      <h1 className="h2">Get started</h1>
      <p className="lead">
        Start creating the best possible user experience for you customers.
      </p>
    </div>

    <Card>
      <Card.Body>
        <div className="m-sm-3">
          <SignUp />
        </div>
      </Card.Body>
    </Card>
    <div className="text-center mb-3">
      Already have account? <Link to="/auth/sign-in">Log in</Link>
    </div>
  </React.Fragment>
);

export default SignUpPage;
