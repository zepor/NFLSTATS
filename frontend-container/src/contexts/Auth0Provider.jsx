import { useEffect, useReducer } from "react";
import { Auth0Client } from "@auth0/auth0-spa-js";
import AuthContext from "./Auth0Context";

const INITIALIZE = "INITIALIZE";
const SIGN_IN = "SIGN_IN";
const SIGN_OUT = "SIGN_OUT";

const initialState = {
  isAuthenticated: false,
  isInitialized: false,
  user: null,
};

const reducer = (state, action) => {
  if (action.type === INITIALIZE) {
    const { isAuthenticated, user } = action.payload;
    return {
      ...state,
      isAuthenticated,
      isInitialized: true,
      user,
    };
  }
  if (action.type === SIGN_IN) {
    const { user } = action.payload;
    return { ...state, isAuthenticated: true, user };
  }
  if (action.type === SIGN_OUT) {
    return {
      ...state,
      isAuthenticated: false,
      user: null,
    };
  }
  return state;
};

function AuthProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, initialState);

  useEffect(() => {
    const initializeAuth0 = async () => {
      const auth0Client = new Auth0Client({
        domain: process.env.VITE_APP_AUTH0_DOMAIN,
        client_id: process.env.VITE_APP_AUTH0_CLIENT_ID,
        audience: process.env.VITE_APP_AUTH0_AUDIENCE,
        redirect_uri: window.location.origin,
      });
      try {
        await auth0Client.checkSession();
        const isAuthenticated = await auth0Client.isAuthenticated();

        if (isAuthenticated) {
          const user = await auth0Client.getUser();
          dispatch({
            type: INITIALIZE,
            payload: { isAuthenticated, user: user || null },
          });
        } else {
          dispatch({
            type: INITIALIZE,
            payload: { isAuthenticated, user: null },
          });
        }
      } catch (err) {
        console.error(err);
        dispatch({
          type: INITIALIZE,
          payload: { isAuthenticated: false, user: null },
        });
      }
    };

    initializeAuth0();
  }, []);

  const signIn = async () => {
    await auth0Client?.loginWithPopup();
    const isAuthenticated = await auth0Client?.isAuthenticated();

    if (isAuthenticated) {
      const user = await auth0Client?.getUser();
      dispatch({ type: SIGN_IN, payload: { user: user || null } });
    }
  };

  const signOut = () => {
    auth0Client?.logout();
    dispatch({ type: SIGN_OUT });
  };

  const resetPassword = (email) => {};

  root.return (
    <AuthContext.Provider
      value={{
        ...state,
        method: "auth0",
        user: {
          id: state?.user?.sub,
          avatar: state?.user?.picture,
          email: state?.user?.email,
          displayName: "Lucy",
          role: "user",
        },
        signIn,
        signOut,
        resetPassword,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export default AuthProvider;
