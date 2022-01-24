import React from "react";
import { Link as ReactRouterLink } from "react-router-dom";

const IS_EXTERNAL_LINK_REGEX = /^(?:[a-z][a-z\d+.-]*:|\/\/)/;

export const Link: React.FC<any> = ({
  children,
  url = "",
  external,
  ref,
  ...rest
}) => {
  // use <a> tag if link is external
  if (external || IS_EXTERNAL_LINK_REGEX.test(url)) {
    rest.target = "_blank";
    rest.rel = "noopener noreferrer";
    return (
      <a href={url} {...rest}>
        {children}
      </a>
    );
  }

  return (
    <ReactRouterLink to={url} {...rest}>
      {children}
    </ReactRouterLink>
  );
};
