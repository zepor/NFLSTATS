module.exports = {
  overwrite: true,
  schema: "backend-container/src/Schema/NFL_v7/",
  documents: "frontend-container/src/**/*.jsx",
  generates: {
    "frontend-container/src/gql": {
      preset: "client",
      plugins: []
    },
    "./graphql.schema.json": {
      plugins: [
        "introspection"
      ]
    }
  }
};
