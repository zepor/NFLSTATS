import React from "react";
import { Helmet } from "react-helmet-async";
import { Card } from "react-bootstrap";
import { Link } from "react-router-dom";

import ResetPassword from "../../components/auth/ResetPassword";

const ResetPasswordPage = () => (
  <React.Fragment>
    <Helmet title="Reset Password" />
    <div className="text-center mt-4">
      <h1 className="h2">Reset password</h1>
      <p className="lead">Enter your email to reset your password.</p>
    </div>

    <Card>
      <Card.Body>
        <div className="m-sm-3">
          <ResetPassword />
        </div>
      </Card.Body>
    </Card>
    <div className="text-center mb-3">
      Don't have an account? <Link to="/auth/sign-up">Sign up</Link>
    </div>
  </React.Fragment>
);

export default ResetPasswordPage;
