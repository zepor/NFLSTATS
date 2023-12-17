import React, { useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import Main from "../components/Main";
import AuthContext from "../contexts/CognitoContext";

const Landing = ({ children }) => {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      navigate("/dashboard/default");
    }
  }, [user, navigate]);

  return <Main>{children}</Main>;
};

export default Landing;
