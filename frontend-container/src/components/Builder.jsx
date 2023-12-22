import React, { useEffect, useState } from "react";
import { BuilderComponent, builder, useIsPreviewing } from "@builder.io/react";\
import Page404 from "./Page404";
import ErrorBoundary from "./ErrorBoundary";

builder.init(process.env.BUILDERAPI);

export default function CatchAllRoute() {
  const isPreviewingInBuilder = useIsPreviewing();
  const [notFound, setNotFound] = useState(false);
  const [content, setContent] = useState(null);
  const [error, setError] = useState(null); // Error state

  useEffect(() => {
    async function fetchContent() {
      try {
        const content = await builder
          .get("page", {
            url: window.location.pathname,
          })
          .promise();

        setContent(content);
        setNotFound(!content);

        if (content?.data.title) {
          document.title = content.data.title;
        }
      } catch (err) {
        console.error("Error fetching Builder.io content:", error);
      }
    }

    fetchContent();
  }, [window.location.pathname]);

  if (notFound && !isPreviewingInBuilder) {
    return <Page404 />;
  }

  // return the page when found
  return (
    <ErrorBoundary>
      <BuilderComponent model="page" content={content} />
    </ErrorBoundary>
  );
}
