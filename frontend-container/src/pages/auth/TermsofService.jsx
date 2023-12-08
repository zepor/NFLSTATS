// TermsOfServicePage.jsx
import React from "react";
import { Link } from "react-router-dom";
import { Helmet } from "react-helmet-async";
import { Button } from "react-bootstrap";
import TermsofService from "../../components/auth/TermsOfService"; // Import the TermsOfService component

const TermsofServicePage = () => (
  <React.Fragment>
    <Helmet title="Terms of Service" />
    <div className="text-center">
      <h1 className="display-1 fw-bold">Terms of Service</h1>
      <p className="lead fw-normal mt-3 mb-4">
        Read our terms and conditions for using LoveOfFootball.io.
      </p>
      <TermsofService />
      <Link to="/dashboard/default">
        <Button variant="primary" size="lg">
          Return to website
        </Button>
      </Link>
    </div>
  </React.Fragment>
);

export default TermsofServicePage;
