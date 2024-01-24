import React from "react";
import { Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";

function SignUp() {
  const { loginWithRedirect } = useAuth0();

  return (
    <>
      {/* Auth0 Sign Up Button */}
      <div className="text-center mt-3">
        <Button onClick={() => loginWithRedirect()} variant="primary" size="lg">
          Sign up with Auth0
        </Button>
      </div>

      {/* Terms of Service and Privacy Policy Links */}
      <div className="text-center mt-3">
        <Link to="/auth/termsofservice">Terms of Service</Link> |{" "}
        <Link to="/auth/privacypolicy">Privacy Policy</Link>
      </div>
    </>
  );
}

export default SignUp;
