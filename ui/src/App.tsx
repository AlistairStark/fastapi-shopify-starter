import React from "react";
import "./App.css";
import { config } from "./services";
import enTranslations from "@shopify/polaris/locales/en.json";

import { AppProvider } from "@shopify/polaris";

import "@shopify/polaris/build/esm/styles.css";
import { HomePage } from "./pages/HomePage";
import { Route, Routes } from "react-router-dom";
import { AccountPage } from "./pages/AccountPage";
import { Footer, AppFrame, Link } from "./components";
import { Provider } from "@shopify/app-bridge-react";

function App() {
  console.log(config);
  return (
    <Provider config={config}>
      <AppProvider i18n={enTranslations} linkComponent={Link}>
        <AppFrame>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/account" element={<AccountPage />} />
          </Routes>
        </AppFrame>
        <Footer />
      </AppProvider>
    </Provider>
  );
}

export default App;
