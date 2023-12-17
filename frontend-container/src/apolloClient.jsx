// src/apolloClient.js
import { ApolloClient, HttpLink, InMemoryCache } from "@apollo/client";
import * as Realm from "realm-web";

const graphqlUri = `https://realm.mongodb.com/api/client/v2.0/app/devicesync-lsank/graphql`;
const app = new Realm.App({ id: "devicesync-lsank" }); // Replace with your Realm app ID

async function getValidAccessToken() {
  if (!app.currentUser) {
    await app.logIn(Realm.Credentials.anonymous());
  } else {
    await app.currentUser.refreshAccessToken();
  }
  return app.currentUser.accessToken;
}

const client = new ApolloClient({
  link: new HttpLink({
    uri: graphqlUri,
    fetch: async (uri, options) => {
      const accessToken = await getValidAccessToken();
      options.headers.Authorization = `Bearer ${accessToken}`;
      return fetch(uri, options);
    },
  }),
  cache: new InMemoryCache(),
});

export default client;
