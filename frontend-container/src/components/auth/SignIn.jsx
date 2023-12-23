import React from "react";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faFacebookF, faGoogle } from "@fortawesome/free-brands-svg-icons";
import { useAuth0 } from "@auth0/auth0-react";
import { Button } from "react-bootstrap";

function SignIn() {
  const { loginWithRedirect } = useAuth0();

  return (
    <>
      <div className="d-grid gap-2 mb-3">
        <Link to="/dashboard/default" className="btn btn-google btn-lg">
          <FontAwesomeIcon icon={faGoogle} /> Sign in with Google
        </Link>
        <Link to="/dashboard/default" className="btn btn-facebook btn-lg">
          <FontAwesomeIcon icon={faFacebookF} /> Sign in with Facebook
        </Link>
      </div>
      <div className="row">
        <div className="col">
          <hr />
        </div>
        <div className="col-auto text-uppercase d-flex align-items-center">
          Or
        </div>
        <div className="col">
          <hr />
        </div>
      </div>

      {/* Auth0 Sign In Button */}
      <div className="text-center mt-3">
        <Button onClick={() => loginWithRedirect()} variant="primary" size="lg">
          Sign in with Auth0
        </Button>
      </div>

      <small>
        <Link to="/auth/reset-password">Forgot password?</Link>
      </small>
    </>
  );
}

export default SignIn;
