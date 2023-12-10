import React, { useEffect } from "react";
import { useAuthenticator } from "@aws-amplify/ui-react";
import { useNavigate } from "react-router-dom";
import { Outlet } from "react-router-dom";

import Main from "../components/Main";

const Landing = ({ children }) => {
  const { user } = useAuthenticator((context) => [context.user]);
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      // User is authenticated, redirect to dashboard
      navigate("/dashboard/default");
    }
  }, [user, navigate]);

  return (
    <Main>
      {children}
      <Outlet />
    </Main>
  );
};

export default Landing;
