import { Amplify } from "aws-amplify";
import { useAuthenticator } from "@aws-amplify/ui-react";
import { Authenticator } from "@aws-amplify/ui-react";
import "@aws-amplify/ui-react/reset.layer.css";
import "@fontsource/inter/variable.css";
import awsExports from "./aws-exports";

Amplify.configure(awsExports);

function App() {
  return (
    <Authenticator socialProviders={["amazon", "apple", "facebook", "google"]}>
      {({ signOut, user }) => (
        <main>
          <h1>Hello {user.username}</h1>
          <button onClick={signOut}>Sign out</button>
        </main>
      )}
    </Authenticator>
  );
}

export default App;
