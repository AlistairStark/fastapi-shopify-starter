import { useAppBridge } from "@shopify/app-bridge-react";
import { Redirect } from "@shopify/app-bridge/actions";
import React, { useState } from "react";
import { Route, Routes } from "react-router-dom";
import { FullscreenSpinner, AppFrame } from "../components";
import { useApi } from "../hooks";
import { AccountPage, HomePage } from "../pages";
import { ApiRoutes } from "../types";

enum AppState {
  Valid = "valid",
  Pending = "pending",
  Invalid = "invalid",
}

function getAppState(valid: boolean): AppState {
  if (valid) {
    return AppState.Valid;
  }
  return AppState.Invalid;
}

export const Routing = () => {
  const [appState, setAppState] = useState<AppState>(AppState.Pending);
  const { data, error } = useApi<{ valid: boolean; redirect?: string }>(
    ApiRoutes.CheckPlan
  );
  const app = useAppBridge();

  if (data?.redirect) {
    const redirect = Redirect.create(app);
    const url = data.redirect.split("myshopify.com/admin")[1];
    console.log(url);
    redirect.dispatch(Redirect.Action.ADMIN_PATH, url);
  }

  if (appState !== AppState.Valid && data && data.valid) {
    setAppState(getAppState(data.valid));
  }

  if (error) {
    console.error(error);
    return <div>Uh oh, something went wrong. Try reloading the page.</div>;
  }

  if (appState === AppState.Pending) {
    return <FullscreenSpinner accessibilityLabel="App loading" />;
  }

  if (appState === AppState.Invalid) {
    return <div>it's invalid, do something</div>;
  }

  return (
    <AppFrame>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/account" element={<AccountPage />} />
      </Routes>
    </AppFrame>
  );
};
