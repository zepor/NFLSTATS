// PrivacyPolicyPage.jsx
import React from "react";
import { Link } from "react-router-dom";
import { Helmet } from "react-helmet-async";
import { Button } from "react-bootstrap";
import PrivacyPolicy from "../../components/auth/PrivacyPolicy";

const PrivacyPolicyPage = () => (
  <React.Fragment>
    <Helmet title="Privacy Policy" />
    <div className="text-center">
      <h1 className="display-1 fw-bold">Privacy Policy</h1>
      <p className="lead fw-normal mt-3 mb-4">
        Learn how LoveOfFootball.io protects and uses your data.
      </p>
      <PrivacyPolicy />
      <Link to="/dashboard/default">
        <Button variant="primary" size="lg">
          Return to website
        </Button>
      </Link>
    </div>
  </React.Fragment>
);

export default PrivacyPolicyPage;
