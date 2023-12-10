import * as React from "react";
import { Navigate } from "react-router-dom";

import { useAuthenticator } from "@aws-amplify/ui-react";

// For routes that can only be accessed by unauthenticated users
function GuestGuard({ children }) {
  const { isAuthenticated, isInitialized } = useAuthenticator((context) => [
    context.user,
  ]);

  if (isInitialized && isAuthenticated) {
    return <Navigate to="/" />;
  }

  return <React.Fragment>{children}</React.Fragment>;
}

export default GuestGuard;
