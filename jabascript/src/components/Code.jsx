import React from "react";

import { Light as SyntaxHighlighter } from "react-syntax-highlighter";

import js from "react-syntax-highlighter/dist/esm/languages/hljs/javascript";
import { vs2015 } from "react-syntax-highlighter/dist/esm/styles/hljs";

SyntaxHighlighter.registerLanguage("javascript", js);

const Code = ({ children }) => {
  return (
    <SyntaxHighlighter className="rounded p-3 bg-dark"
      language="javascript"
      style={vs2015}>{children}</SyntaxHighlighter>
  );
};

export default Code;
