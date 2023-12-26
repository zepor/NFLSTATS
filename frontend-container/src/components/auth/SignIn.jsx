import React from "react";
import { Link } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import { Button } from "react-bootstrap";

function SignIn() {
  const { loginWithRedirect } = useAuth0();

  return (
    <>
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
