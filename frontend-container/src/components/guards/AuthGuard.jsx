import * as React from "react";
import { Navigate } from "react-router-dom";

import { useAuthenticator } from "@aws-amplify/ui-react";

// For routes that can only be accessed by authenticated users
function AuthGuard({ children }) {
  const { isAuthenticated, isInitialized } = useAuthenticator((context) => [
    context.user,
  ]);

  if (isInitialized && !isAuthenticated) {
    return <Navigate to="/auth/sign-in" />;
  }

  return <React.Fragment>{children}</React.Fragment>;
}

export default AuthGuard;
