import React from "react";
import { Button } from "react-bootstrap";
import { useAuth0 } from "@auth0/auth0-react";

function SignUp() {
  const { loginWithRedirect } = useAuth0();

  return (
    <>
      {/* Auth0 Sign In Button */}
      <div className="text-center mt-3">
        <Button onClick={() => loginWithRedirect()} variant="primary" size="lg">
          Sign up with Auth0
        </Button>
      </div>
    </>
  );
}

export default SignUp;
