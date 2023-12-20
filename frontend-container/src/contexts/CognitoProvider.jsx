import React, {
  useCallback,
  useEffect,
  useReducer,
  useState,
  useMemo,
} from "react";
import {
  AuthenticationDetails,
  CognitoUser,
  CognitoUserAttribute,
  CognitoUserPool,
} from "amazon-cognito-identity-js";
import axios from "../utils/axios";
import AuthContext from "./CognitoContext";
import Loader from "../components/Loader";

const INITIALIZE = "INITIALIZE";
const SIGN_OUT = "SIGN_OUT";

const initialState = {
  isAuthenticated: false,
  isInitialized: false,
  user: null,
};

const reducer = (state, action) => {
  switch (action.type) {
    case INITIALIZE:
      return {
        ...state,
        isAuthenticated: action.payload.isAuthenticated,
        isInitialized: true,
        user: action.payload.user,
      };
    case SIGN_OUT:
      return {
        ...state,
        isAuthenticated: false,
        user: null,
      };
    default:
      return state;
  }
};

function AuthProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, initialState);
  const [cognitoConfig, setCognitoConfig] = useState(null);

  useEffect(() => {
    const loadConfig = async () => {
      if (process.env.NODE_ENV === "development") {
        const configModule = await import("../config");
        setCognitoConfig(configModule.cognitoConfig);
      } else {
        setCognitoConfig({
          userPoolId: process.env.VITE_COGNITO_USER_POOL_ID,
          clientId: process.env.VITE_COGNITO_CLIENT_ID,
        });
      }
    };
    loadConfig();
  }, []);

  const UserPool = useMemo(() => {
    if (cognitoConfig && cognitoConfig.userPoolId && cognitoConfig.clientId) {
      return new CognitoUserPool({
        UserPoolId: cognitoConfig.userPoolId,
        ClientId: cognitoConfig.clientId,
      });
    }
    return null;
  }, [cognitoConfig]);

  const getUserAttributes = useCallback(
    (currentUser) =>
      new Promise((resolve, reject) => {
        currentUser.getUserAttributes((err, attributes) => {
          if (err) {
            reject(err);
          } else {
            const results = {};
            for (const attribute of attributes) {
              results[attribute.Name] = attribute.Value;
            }
            resolve(results);
          }
        });
      }),
    [],
  );

  const getSession = useCallback(
    () =>
      new Promise((resolve, reject) => {
        const user = UserPool ? UserPool.getCurrentUser() : null;
        if (user) {
          user.getSession(async (err, session) => {
            if (err) {
              reject(err);
            } else {
              const attributes = await getUserAttributes(user);
              const token = session.getIdToken().getJwtToken();
              axios.defaults.headers.common.Authorization = token;
              dispatch({
                type: INITIALIZE,
                payload: { isAuthenticated: true, user: attributes },
              });
              resolve({ user, session, headers: { Authorization: token } });
            }
          });
        } else {
          dispatch({
            type: INITIALIZE,
            payload: { isAuthenticated: false, user: null },
          });
        }
      }),
    [UserPool, getUserAttributes],
  );

  useEffect(() => {
    if (cognitoConfig) {
      getSession();
    }
  }, [getSession, cognitoConfig]);

  const signIn = useCallback(
    (email, password) =>
      new Promise((resolve, reject) => {
        if (!UserPool) {
          return reject(new Error("Cognito User Pool not available"));
        }
        const user = new CognitoUser({ Username: email, Pool: UserPool });
        const authDetails = new AuthenticationDetails({
          Username: email,
          Password: password,
        });

        user.authenticateUser(authDetails, {
          onSuccess: (data) => {
            getSession().then(() => resolve(data));
          },
          onFailure: (err) => {
            reject(err);
          },
          newPasswordRequired: () => {
            resolve({ message: "New password required" });
          },
        });
      }),
    [UserPool, getSession],
  );

  const signOut = useCallback(() => {
    const user = UserPool ? UserPool.getCurrentUser() : null;
    if (user) {
      user.signOut();
      dispatch({ type: SIGN_OUT });
    }
  }, [UserPool]);

  const signUp = useCallback(
    (email, password, firstName, lastName) =>
      new Promise((resolve, reject) => {
        UserPool.signUp(
          email,
          password,
          [
            new CognitoUserAttribute({ Name: "email", Value: email }),
            new CognitoUserAttribute({
              Name: "name",
              Value: `${firstName} ${lastName}`,
            }),
          ],
          null,
          (err) => {
            if (err) {
              reject(err);
              return;
            }
            resolve();
          },
        );
      }),
    [],
  );

  const resetPassword = useCallback((email) => {
    console.log(email);
    // Add password reset logic here
  }, []);

  if (!cognitoConfig) {
    return <Loader />;
  }

  return (
    <AuthContext.Provider
      value={{
        ...state,
        method: "cognito",
        user: {
          displayName: state.user?.name || "Undefined",
          role: "user",
        },
        signIn,
        signUp,
        signOut,
        resetPassword,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export default AuthProvider;
