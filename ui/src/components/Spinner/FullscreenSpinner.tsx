import { Spinner } from "@shopify/polaris";
import React from "react";
import "./fullscreen.css";

type Props = {
  accessibilityLabel: string;
};

export const FullscreenSpinner: React.FC<Props> = ({ accessibilityLabel }) => (
  <div className="fullscreen-spinner">
    <Spinner accessibilityLabel={accessibilityLabel} size="large" />
  </div>
);
